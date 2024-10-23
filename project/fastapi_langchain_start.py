from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser



def build_chain(llm_name:str):

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

    chain = llm | StrOutputParser()

    return chain 


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
        chain = build_chain("openai")
        result = chain.invoke([{"role": "user", "content": FIXED_PROMPT + input_data.text}])
        print(result)
        return {"response": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_langchain_start:app", host="0.0.0.0", port=8000, reload=True)
