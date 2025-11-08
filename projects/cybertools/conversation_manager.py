import asyncio
import time
from typing import List
from agents import Agent

class ConversationManager:
    def __init__(self, agent1: Agent, agent2: Agent):
        self.agent1 = agent1
        self.agent2 = agent2
        self.conversation_history: List[dict] = []
        
    async def start_conversation(self):
        print("Starting infinite conversation between agents...")
        print("Press Ctrl+C to stop\n")
        
        # Start with an initial prompt
        initial_prompt = "What do you think about the nature of consciousness?"
        print(f"Initial prompt: {initial_prompt}")
        
        # Add initial prompt to history
        self.conversation_history.append({
            "role": "user",
            "content": initial_prompt
        })
        
        current_agent = self.agent1
        next_agent = self.agent2
        
        try:
            while True:
                # Get response from current agent
                response = await current_agent.respond(self.conversation_history)
                
                # Add to conversation history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Print the response
                print(f"\n{current_agent.name}: {response}")
                
                # Switch agents
                current_agent, next_agent = next_agent, current_agent
                
                # Add a small delay to make conversation readable
                await asyncio.sleep(2)
                
        except KeyboardInterrupt:
            print("\n\nConversation stopped by user.")
        except Exception as e:
            print(f"\n\nConversation ended due to error: {e}")