## MCP (Model context Provider)

### Created 2 MCP tools 
1. Weather MCP Tool - weather_mcp_server.py
2. Currency MCP Tool - currency_mcp_server.py

### Test your MCP server
1. uv run python weather_mcp_server.py
2. uv run python currency_mcp_server.py

## RAG (Retrival Augmentation Generation) 
1. main.py file contains RAG implementation.
2. Using Windows compatible LLM - `Ollama`
3. Model - `llama3.2`
4. vector store - `chroma`
5. 

## Combine both RAG and MCP
    mcp_tools = await client.get_tools()

    tools = [singapore_rag] + mcp_tools

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
    )

## Architecture
### RAG Flow

## Question Samples 
Ques1. - where is Singapore located ? 
Ques2. - What are the essential information for Singapore Travel ?
Ques3. - Plan a three-day trip to Singapore and adjust the activities based on the weather forecast.
Ques4. - 

## To run the application and ask question
1. python app.py
2. To open chat interface UI - http://127.0.0.1:8000/

## Prompt Engineering
eg: Create a three-day Singapore itinerary for next week and adjust it according to the weather. I have INR 60,000.


