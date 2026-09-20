## Git Repo Link 
https://github.com/singlaromal16/NAGP-AI-ML-2026

## Video Link

## MCP (Model context Provider)
MCP is used to access current information of weather and currency.
### Created 2 MCP tools 
1. Weather MCP Tool - weather_mcp_server.py
2. Currency MCP Tool - currency_mcp_server.py

## RAG (Retrival Augmentation Generation) 
1. main.py file contains RAG implementation.
2. Using Windows compatible LLM - `Ollama`
3. Model - `llama3.2`
4. vector store - `chroma`

## Combine both RAG and MCP
RAG and MCP can be combined to provide a more better result

## RAG Workflow
#### Chunking in RAG
Raw documentation -> Chunking -> Embedding -> Vector Store

#### Inference With RAG
User -> Prompt related travel -> Singapore Knowledge Base -> AI generated answer

## Setup instruction 

1. git clone https://github.com/singlaromal16/NAGP-AI-ML-2026
2. cd travel_planning_assistant
3. Install dependencies mentioned in requirements.txt
4. Create .env file and add `GOOGLE API KEY`
5. Run application
`python app.py`
6. Open chat UI interface enter url http://127.0.0.1:8000/
7. Example Question - 
Plan a three-day trip to Singapore and adjust the activities based on the weather forecast.


## Question Samples 
Ques1. - where is Singapore located ? 
Ques2. - What are the essential information for Singapore Travel ?
Ques3. - Plan a three-day trip to Singapore and adjust the activities based on the weather forecast.


