from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import dotenv
from prompts import call_prompt, Event, PromptType  # Importing call_prompt and Event

# Initialize FastAPI
app = FastAPI()
dotenv.load_dotenv()

# CORS setup
origins = [
    "http://localhost:5173",  # Localhost for development
    "http://89.22.227.224"     # Your deployed React app's URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Use the defined origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ChatRequest(BaseModel):
    message: str
    reality: str
    brutality: str
    detailed: bool
    population: bool

@app.post("/chat")
async def chat_with_openai(request: ChatRequest):
    print(f"Chat: {request.message}, Reality: {request.reality}, Brutality: {request.brutality}, Detailed: {request.detailed}")
    print(request.__class__)
    # Create the prompt using the moved function
    prompt_message = call_prompt(
        message=request.message,
        isDetailed=request.detailed,
        reality_type=request.reality,
        brutality_type=request.brutality,
        isPopulation=request.population,
    )
    print(prompt_message)
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_message}],
            model="gpt-4o-mini",
        )
        print({"response": response.choices[0].message})
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
