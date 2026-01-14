from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from openai import OpenAI

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print("API KEY LOADED:", api_key is not None)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="GenAI Chatbot API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI chatbot."},
            {"role": "user", "content": request.message}
        ]
    )

    return {
        "bot_response": completion.choices[0].message.content
    }

@app.get("/")
def root():
    return {"status": "GenAI Chatbot API running"}
