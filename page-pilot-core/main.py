from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

app = FastAPI()

# Allow browser extension calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🧠 Conversation memory (per page URL)
conversation_store = {}

# -------- Request model --------
class AskRequest(BaseModel):
    url: str
    content: str
    question: str


# -------- Normalize follow-up / fragment questions --------
def normalize_question(question: str, conversation: list) -> str:
    """
    If the user input is a short or fragmented follow-up,
    attach it to the previous user question to preserve context.
    """
    words = question.strip().split()

    if len(words) < 6 and conversation:
        last_user_question = None

        for msg in reversed(conversation):
            if msg["role"] == "user":
                last_user_question = msg["content"]
                break

        if last_user_question:
            return (
                f"Based on the previous question: '{last_user_question}', "
                f"answer the following follow-up question: {question}"
            )

    return question


# -------- API Endpoint --------
@app.post("/ask")
def ask_page(req: AskRequest):

    # Limit page content to avoid token overflow
    page_content = req.content[:15000]

    # Initialize memory for this page
    if req.url not in conversation_store:
        conversation_store[req.url] = []

    conversation = conversation_store[req.url]

    system_prompt = f"""
You are an AI assistant.

Rules:
- Answer ONLY using the provided page content or direct logical implications of it.
- Do NOT add external facts or assumptions.
- If the answer cannot be reasonably inferred from the page content, reply exactly:
  "The result for your question is not available."

Page Content:
{page_content}
"""

    # Build messages
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # Add conversation history
    messages.extend(conversation)

    # Normalize the incoming question (CRITICAL FIX)
    normalized_question = normalize_question(req.question, conversation)

    messages.append({
        "role": "user",
        "content": normalized_question
    })

    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = response.choices[0].message.content.strip()

    # Save conversation
    conversation.append({"role": "user", "content": req.question})
    conversation.append({"role": "assistant", "content": answer})

    return {
        "answer": answer
    }
