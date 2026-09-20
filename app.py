import asyncio
from fastapi.responses import FileResponse
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from main import singapore_rag

# Load environment variables from .env
load_dotenv()


# Combine RAG and MCP tools into a single agent for travel planning assistance.
async def initialize_agent():

    # Connect to the MCP servers for weather and currency tools
    client = MultiServerMCPClient({
      "weather": {
          "command": "uv",
          "args": ["run", "python", "weather_mcp_server.py"],
          "transport": "stdio", 
      },
      "currency": {
          "command": "uv",
          "args": ["run", "python", "currency_mcp_server.py"],
          "transport": "stdio", 
      }
    })

    # MCP Tools
    mcp_tools = await client.get_tools()

    # RAG + MCP Tools
    tools = [singapore_rag] + mcp_tools

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful assistant for travel planning. Use the tools provided to answer questions about Singapore, weather, and currency conversion.",
    )

    return agent

# Initialize the FastAPI app to  handle the requests
fastApiApp = FastAPI()

fastApiApp.add_middleware(
    CORSMiddleware,
      allow_origins=["*"],
      allow_methods=["*"],
      allow_headers=["*"],
    )

class Question(BaseModel):
    question: str

@fastApiApp.get("/")
async def home():
    return FileResponse("index.html")

@fastApiApp.post("/ask")
async def ask(data: Question):

        agent = await initialize_agent()
        result = await agent.ainvoke({
            "messages": [
                {"role": "user", "content": data.question}
            ]
        })

        answer = result["messages"][-1].content

        # Sometimes AI responses come back as a list of blocks.
        if isinstance(answer, list):
            answer = "".join(
                block.get("text", "")
                for block in answer
                if isinstance(block, dict)
            )

        return {"answer": answer}


if __name__ == "__main__":
    uvicorn.run(fastApiApp, host="127.0.0.1", port=8000)


#     while True:
#         question = input("You: ")

#         if question.lower() in ["exit", "quit"]:
#             break

#         try:
#             result = await agent.ainvoke({
#                 "messages": [
#                     {"role": "user", "content": question}
#                 ]
#             })

#             print(
#                 f"AI: {result['messages'][-1].content}\n"
#             )
#         except Exception as e:
#             print(f"Error: {str(e)}\n")


# if __name__ == "__main__":
#     asyncio.run(app())