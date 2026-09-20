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

## Prompt Engineering

The prompt is designed to make the travel assistant provide reliable and personalized recommendations. It includes

1.	Retrieved Knowledge Base Content
It uses retrieved knowledge base content for destination facts. It is covering major attraction and neighbourhood. Food and local experiences and indoor and outdoor activity suggestions.

2.	MCP Tool for current information 
Create two MCP tool. One for weather and another for currency.
It prefer current tool data over older or static information. 

3.	Handle Missing Information
If information is not available then clearly state “Information is not available from the sources”

`Example:`
Create a 3-day Singapore itinerary within my INR 60,000 budget. Use the knowledge base for destination facts and MCP data for current weather, prices, and availability. Do not guess missing information. Clearly separate information from your suggestions and include sources where available.


## Question Samples 
### MCP
#### Currency
Ques1 - How much is 200 SGD in INR? 
#### Weather
Ques2 - Should I plan indoor or outdoor activities tomorrow? 

### RAG
Ques1 - What are the must-visit attractions in Singapore? 
Ques2 - What are the essential information for Singapore Travel ?

### Combine MCP + RAG 
Ques1 - Plan a three-day trip to Singapore and adjust the activities based on the weather forecast.

### Conversational 

Ques1 - I am planning a 3-day trip to Singapore with a budget of ₹60,000. I like museums.
Ques2 - Make the second day more relaxed.

