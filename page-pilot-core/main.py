from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🧠 In-memory conversation store (per URL)
conversation_store = {}

class AskRequest(BaseModel):
    url: str
    content: str
    question: str

@app.post("/ask")
def ask_page(req: AskRequest):
    # Limit page content
    page_content = req.content[:15000]

    # Initialize memory for this page
    if req.url not in conversation_store:
        conversation_store[req.url] = []

    conversation = conversation_store[req.url]

    system_prompt = f"""
You are an AI assistant.

Rules:
- Answer ONLY using the provided page content.
- Use conversation history for context.
- If the answer is not found in the page content, reply exactly:
  "The result for your question is not available."

Page Content:
{page_content}
"""

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # Add conversation history
    messages.extend(conversation)

    # Add current user question
    messages.append({"role": "user", "content": req.question})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = response.choices[0].message.content.strip()

    # 🧠 Save conversation
    conversation.append({"role": "user", "content": req.question})
    conversation.append({"role": "assistant", "content": answer})

    return {"answer": answer}
