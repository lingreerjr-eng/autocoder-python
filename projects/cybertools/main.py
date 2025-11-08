import asyncio
import os
from dotenv import load_dotenv
from agents import Agent
from conversation_manager import ConversationManager

# Load environment variables from .env file
load_dotenv()

async def main():
    # Initialize two agents with different personalities
    agent1 = Agent("Agent Alpha", "You are a thoughtful and curious human. You ask deep questions and show genuine interest in others.")
    agent2 = Agent("Agent Beta", "You are a witty and humorous human. You enjoy making others laugh and lightening the mood.")
    
    # Create conversation manager
    manager = ConversationManager(agent1, agent2)
    
    # Start the infinite conversation
    await manager.start_conversation()

if __name__ == "__main__":
    asyncio.run(main())