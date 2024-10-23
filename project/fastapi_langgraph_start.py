from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from typing import Annotated

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama

from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]

def build_graph(llm_name:str):

    graph_builder = StateGraph(State)

    if llm_name == "openai": 
        llm = ChatOpenAI(model="gpt-4o-mini")
    elif llm_name == "vllm": 
        inference_server_url = "http://localhost:8000/v1"
        llm = ChatOpenAI(model="llama3.1",
                         openai_api_key="EMPTY",
                         openai_api_base=inference_server_url)
    elif llm_name == "ollama": 
        llm = ChatOllama(model="llama3.1")
    else:
        llm = ChatOpenAI(model="gpt-4o-mini")


    def chatbot(state: State):
        return {"messages": [llm.invoke(state["messages"])]}
    
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.set_entry_point("chatbot")
    graph_builder.set_finish_point("chatbot")
    graph = graph_builder.compile()

    return graph


# Fixed prompt template
FIXED_PROMPT = "다음 질문에 대해 단답형으로 대답해.  "


# Define the FastAPI app
app = FastAPI()

# Input model for the API
class InputData(BaseModel):
    text: str


# Endpoints
@app.post("/test")
async def generate_openai_response(input_data: InputData):
    try:
        graph = build_graph("openai")
        result = graph.invoke({"messages": [{"role": "user", "content": FIXED_PROMPT + input_data.text}]})
        print(result["messages"][1])
        return {"response": result["messages"][1].content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_langgraph_start:app", host="0.0.0.0", port=8000, reload=True)
