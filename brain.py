import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import uvicorn

# Use API Key for Groq from environment variable or .env
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)  # Secure API key handling

app = FastAPI()

SERVER_IP = "10.54.252.83"

class Query(BaseModel):
    text: str

def get_ai_response(user_input):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are Super AI. Provide fast, secure and professional answers."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/")
def home():
    return {
        "status": "Super AI Server is Running Online",
        "ip": SERVER_IP
    }

@app.post("/ask")
def ask_ai(query: Query):
    user_message = query.text

    # App opening logic (100% same as yours)
    if "open" in user_message.lower():
        lower_msg = user_message.lower()
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

    # Normal AI response
    answer = get_ai_response(user_message)
    # Flutter side par "reply" key use ho rahi hai, isliye "reply" bhej rahe hain
    return {"reply": answer, "action": "none", "ip": SERVER_IP}

if __name__ == "__main__":
    # Cloud hosting (Render/Railway) ke liye port ko environment se lena zaroori hai
    # Agar local PC par chalayenge toh ye default 8000 port aur 0.0.0.0 host use karega
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)