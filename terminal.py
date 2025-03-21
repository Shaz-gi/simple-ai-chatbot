import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv
import os 
from typing import Optional, Dict, Any

load_dotenv()

gemini_api_key= os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel(model_name="gemini-2.0-flash")

@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.user,
) -> Optional[cl.User]:
    """
    Handle the OAuth callback from Github
    Return the user object if authentication is successful, None otherwise
    """

    print(f"Provider: {provider_id}")
    print(f"User Data: {raw_user_data}")

    return default_user

@cl.on_chat_start
async def handle_chat_start():

    cl.user.session.set("history", [])

    await cl.Message(content="Hello! How can I help you?").send()

@cl.on_message
async def handle_message(message: cl.Message):

    history = cl.user_session.get("histoy")

    history.append(("role": "user", "content": message.content))

    formatted_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"

        formatted_history.append("role": role, "parts": [{"text": msg["content"]}])

        

while True:
    user_input = input("Ask me anything (or type 'quit' to exit): ")
    
    if user_input.lower() == 'quit':
        print("Thanks for Chatting!")
        break
        
    response = model.generate_content(user_input)
    print(response.text)
    print() # Add blank line between responses