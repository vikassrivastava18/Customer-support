from typing import Literal
from dotenv import load_dotenv

from langgraph.graph import StateGraph, MessagesState
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from django.contrib.auth.models import User

from staff.schemas import IntentSchema
from author.models import Ticket, Book
from utils.knowledge import similarity_search
from utils.prompt import INTENT_PROMPT, INFO_PROMPT
from utils.tools import Tools

load_dotenv()
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
checkpointer = InMemorySaver()

# Bind the tools
llm_with_tools = llm.bind_tools(Tools.get_tools())

# Define the graph state
class State(MessagesState):
    book: str
    username: str


class Graph:
    # Define Nodes
    @staticmethod
    def start_graph(state: State) -> State:
        return state

    @staticmethod
    def get_user_intent(state: State) -> Literal["info", "query", "complaint"]:
        prompt = INTENT_PROMPT
        prompt += f"""/n Query: {state["messages"][-1].content}"""
        structured_llm = llm.with_structured_output(IntentSchema)
        response = structured_llm.invoke(prompt)
        return response.intent

    @staticmethod
    def assistant(state: State) -> State:
        # System message
        book = state.get("book", None)
        sys_msg = SystemMessage(
        content=f"You are a helpful assistant tasked with fetching relevant data for the user query. Book isbn: {book}")

        llm_response = llm_with_tools.invoke([sys_msg] + state["messages"])
        return {**state, "messages": [llm_response]}

    @staticmethod
    def register_complaint(state: State) -> State:
        response = AIMessage(content='Sorry about that, we have registered your complaint.')
        return {**state, "messages": [response]}

    @staticmethod
    def get_info(state: State) -> State:
        query = state["messages"][-1].content
        response = similarity_search(query)
        if response["distance"] >= 0.7:
            print("No relevant document found")

            # Save a ticket for Human agent in database
            username = state["username"]
            user = User.objects.get(username=username)
            ticket = Ticket.objects.create(query=query, user=user, response=response["context"])
            response = (f"Could not find a suitable answer."
                        f"A ticket has been generated with ID: {ticket.id}. Please check your tickets page in some time.")
            return {
                **state,
                "messages": [AIMessage(content=response)]
            }
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

    @staticmethod
    def build_graph():
        from langgraph.prebuilt import tools_condition, ToolNode
        from langgraph.graph import START

        builder = StateGraph(State)

        builder.add_node("start_graph", Graph.start_graph)
        builder.add_node("get_info", Graph.get_info)
        builder.add_node("assistant", Graph.assistant)
        builder.add_node("register_complaint", Graph.register_complaint)
        builder.add_node("tools", ToolNode(Tools.get_tools()))

        builder.add_edge(START, "start_graph")
        builder.add_conditional_edges(
            "start_graph",
            Graph.get_user_intent,
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