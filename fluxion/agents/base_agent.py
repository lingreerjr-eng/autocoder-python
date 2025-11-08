class BaseAgent:
    def __init__(self, ollama_client):
        self.ollama_client = ollama_client
        
    def execute_task(self, task_description):
        prompt = f"""You are an AI assistant. Please complete the following task:

{task_description}

Provide a concise response with your solution or steps to complete this task."""
        
        response = self.ollama_client.generate(prompt)
        return response
