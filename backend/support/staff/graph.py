import uuid

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import SystemMessage

from .schemas import IntentSchema
from .models import AgentTicket, UserBookInfo
from .knowledge import documents

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
checkpointer = InMemorySaver()
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


# Define the tools
def get_royality_timeline():
    """Get the timeline for royality of a book.
    """
    isbn = "978-0-306-406"
    book = UserBookInfo.objects.get(isbn=isbn)
    return book.r_timeline


def get_book_live_status():
    """Get a book current live status
    """
    from datetime import date

    isbn = "978-0-306-406"
    book = UserBookInfo.objects.get(isbn=isbn)
    return "Published" if book.book_live_date < date.today() else "Not published yet"


tools = [get_royality_timeline, get_book_live_status]
llm_with_tools = llm.bind_tools(tools)


def similarity_search(query):
    # get the info chunks
    chunks = documents

    # Create in-memory vector store (FAISS)
    vector_store = FAISS.from_documents(chunks, embeddings)

    # perform similarity search with score
    results = vector_store.similarity_search_with_score(query, k=1)

    # unpack result
    doc, dist = results[0]

    context = doc.page_content

    return {
        "context": context,
        "distance": float(dist)
    }


# Define Nodes
def start_graph(state: MessagesState) -> MessagesState:
    return state


from typing import Literal


def get_user_intent(state: MessagesState) -> Literal["info", "query"]:
    prompt = f"""Based on the user query, decide the intent
       It can only be either info or query. Info is general information regading the process and steps required for 
       getting book published or how to use get something done, like how to upload book cover. Query is when user wants information regarding their book.
       This requires seaching their book from database using SQL, so some data must already be in the database.
       Sample: 
           How to publish my book -> info
           When am I getting my royalty for my book? -> query
        query: {state["messages"][-1].content}       
    """
    structured_llm = llm.with_structured_output(IntentSchema)

    response = structured_llm.invoke(prompt)

    return response.intent


def assistant(state: MessagesState):
    # System message
    sys_msg = SystemMessage(
        content="You are a helpful assistant tasked with fetching relevant data for the user query.")
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


from langchain_core.messages import AIMessage
from langgraph.types import interrupt


def get_info(state: MessagesState) -> MessagesState:
    query = state["messages"][0].content
    response = similarity_search(query)
    print(response["distance"])
    if response["distance"] >= 0.8:

        # Save a ticket for Human agent in database
        ticket_id = uuid.uuid4()
        ticket = AgentTicket.objects.create(ticket_id=ticket_id, user_query=query)
        # Add Human in the loop
        response = interrupt(
            # This value will be sent to the Human Agent
            # as part of the interrupt information.
            f"({ticket_id}) Passing you query to a human agent...."
        )
    else:
        response = response["context"]

    prompt = f"""Return a nice response based on user's query.
    Response should not contain things like ##, **. But do not  remove icons ✍️ that are present. 
    Rather format the response like : <p>.....</p> <p>....</p>
    Query: {query}
    Resonse: {response}
    """
    llm_response = llm.invoke(prompt)
    return {
        "messages": [
            AIMessage(content=llm_response.content)
        ]
    }


def build_graph():
    from langgraph.prebuilt import tools_condition, ToolNode
    from langgraph.graph import START

    builder = StateGraph(MessagesState)

    builder.add_node("start_graph", start_graph)
    builder.add_node("get_info", get_info)

    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "start_graph")
    builder.add_conditional_edges(
        "start_graph",
        get_user_intent,
        {
            "info": "get_info",
            "query": "assistant"
        }
    )
    builder.add_conditional_edges(
        "assistant",
        # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
        # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    react_graph = builder.compile()

    return react_graph