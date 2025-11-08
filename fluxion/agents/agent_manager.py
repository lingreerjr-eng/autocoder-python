from agents.base_agent import BaseAgent
from agents.fleet_coordinator import FleetCoordinator
from utils.ollama_client import OllamaClient

class AgentManager:
    def __init__(self, model='llama3'):
        self.model = model
        self.ollama_client = OllamaClient(model)
        self.fleet_coordinator = FleetCoordinator(self.ollama_client)
        
    def delegate_task(self, task_description):
        # For simplicity, we're using a single agent type
        # In a more complex system, we'd determine agent type based on task
        agent = BaseAgent(self.ollama_client)
        return agent.execute_task(task_description)
        
    def run_fleet(self):
        return self.fleet_coordinator.coordinate_fleet()
