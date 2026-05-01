import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from groq import Groq
import uvicorn

# 1. API Key Check (Security)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY is not set in environment variables!")

client = Groq(api_key=GROQ_API_KEY)

app = FastAPI(title="Super AI Secure Server")

# 2. CORS Security (Sirf zaroori requests allow karne ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein yahan apni app ka domain likhein
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    # Validation: Khali message allow nahi hoga
    text: str = Field(..., min_length=1, max_length=500)

def get_ai_response(user_input):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Super AI. Provide fast, secure and professional answers."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Service Error: Please try again later."

@app.get("/")
def home():
    return {"status": "Super AI Server is Online & Secure"}

@app.post("/ask")
async def ask_ai(query: Query):
    user_message = query.text.strip()

    # Intent Logic (Opening Apps)
    if "open" in user_message.lower():
        lower_msg = user_message.lower()
        app_to_open = ""
        
        if lower_msg.startswith("open "):
            app_to_open = lower_msg.replace("open", "", 1).strip()
        else:
            parts = lower_msg.split("open", 1)
            app_to_open = parts[1].strip() if len(parts) > 1 else ""

        if app_to_open:
            return {
                "reply": f"Opening {app_to_open.capitalize()} for you",
                "action": "open_app",
                "target_app": app_to_open 
            }

    # AI Response logic
    answer = get_ai_response(user_message)
    return {
        "reply": answer, 
        "action": "none"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Workers add karne se server zyada load utha sakta hai
    uvicorn.run(app, host="0.0.0.0", port=port)
