from typing import Literal

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import SystemMessage, AIMessage
from django.contrib.auth.models import User

from .prompt import INTENT_PROMPT, INFO_PROMPT
from .schemas import IntentSchema
from author.models import Ticket, Book
from .knowledge import documents

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
checkpointer = InMemorySaver()
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


# Define the tools
def get_royality_earned(isbn):
    """Get the royality earning for a book."""
    book = Book.objects.get(isbn=isbn)
    return book.royality_earned

def get_royality_paid(isbn):
    """Get the royality pending for a book.."""
    book = Book.objects.get(isbn=isbn)
    return book.royality_earned

def get_royality_pending(isbn):
    """Get the royality pending for a book."""
    book = Book.objects.get(isbn=isbn)
    return book.royality_pending

def get_book_publish_status(isbn):
    """Get a book current live status
    """
    from datetime import date
    book = Book.objects.get(isbn=isbn)
    return f"Already published on {book.pub_date}" if book.pub_date < date.today() \
        else (f"Not published yet, "
              f"publication date: {book.pub_date}")


tools = [get_royality_earned, get_royality_paid,
         get_royality_pending, get_book_publish_status]
# Bind the tools
llm_with_tools = llm.bind_tools(tools)

# Define the graph state
class State(MessagesState):
    book: str
    username: str


def similarity_search(query):
    # get the info chunks
    chunks = documents

    # Create in-memory vector store (FAISS)
    vector_store = FAISS.from_documents(chunks, embeddings)

    # perform similarity search with score
    results = vector_store.similarity_search_with_score(query, k=5)

    # unpack result
    doc, dist = results[0]
    context = doc.page_content

    return {
        "context": context,
        "distance": float(dist)
    }


# Define Nodes
def start_graph(state: State) -> State:
    return state


def get_user_intent(state: State) -> Literal["info", "query", "complaint"]:
    prompt = INTENT_PROMPT
    prompt += f"""/n Query: {state["messages"][-1].content}"""
    print("Prompt: ", prompt)
    structured_llm = llm.with_structured_output(IntentSchema)
    response = structured_llm.invoke(prompt)
    print("User intent: ", response.intent)
    return response.intent


def assistant(state: State) -> State:
    # System message
    book = state.get("book", None)
    sys_msg = SystemMessage(
    content=f"You are a helpful assistant tasked with fetching relevant data for the user query. Book isbn: {book}")

    llm_response = llm_with_tools.invoke([sys_msg] + state["messages"])
    return {**state, "messages": [llm_response]}


def register_complaint(state: State) -> State:
    response = AIMessage(content='Sorry about that, we have registered your complaint.')
    return {**state, "messages": [response]}


def get_info(state: State) -> State:
    query = state["messages"][-1].content
    response = similarity_search(query)
    if response["distance"] >= 0.7:
        # Save a ticket for Human agent in database
        username = state["username"]
        user = User.objects.get(username=username)
        ticket = Ticket.objects.create(query=query, user=user, response=response["context"])
        response = f"Ticket has been generated with ID: {ticket.id}. Please check your tickets page in some time."
    else:
        response = response["context"]

    prompt = INFO_PROMPT

    prompt += f"""/n Query: {query}. 
               Context: {response}. 
               Answer strictly based on the context."""
    response = llm.invoke(prompt).content
    return {
        **state,
        "messages": [AIMessage(content=response)]
    }


def build_graph():
    from langgraph.prebuilt import tools_condition, ToolNode
    from langgraph.graph import START

    builder = StateGraph(State)

    builder.add_node("start_graph", start_graph)
    builder.add_node("get_info", get_info)

    builder.add_node("assistant", assistant)
    builder.add_node("register_complaint", register_complaint)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "start_graph")
    builder.add_conditional_edges(
        "start_graph",
        get_user_intent,
        {
            "info": "get_info",
            "query": "assistant",
            "complaint": "register_complaint"
        }
    )
    builder.add_conditional_edges(
        "assistant",
        # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
        # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    react_graph = builder.compile(checkpointer=checkpointer)

    return react_graph