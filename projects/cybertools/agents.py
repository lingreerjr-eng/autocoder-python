import openai
import asyncio
import os
from typing import List

class Agent:
    def __init__(self, name: str, personality: str):
        self.name = name
        self.personality = personality
        self.messages: List[dict] = []
        # Initialize AsyncOpenAI without proxies parameter to avoid TypeError
        self.client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def respond(self, conversation_history: List[dict]) -> str:
        # Add personality to the system message
        system_message = {
            "role": "system",
            "content": f"{self.personality} Respond naturally as if in a casual conversation. Be concise but engaging."
        }
        
        # Combine system message with conversation history
        messages = [system_message] + conversation_history[-10:]  # Only keep last 10 messages for context
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.8,
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in {self.name}: {e}")
            return "I'm having trouble responding right now."
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
