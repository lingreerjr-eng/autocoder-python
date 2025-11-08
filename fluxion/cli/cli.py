import sys
from agents.agent_manager import AgentManager
from utils.io_handler import IOHandler

class CLI:
    def __init__(self, model='llama3'):
        self.agent_manager = AgentManager(model)
        self.io_handler = IOHandler()
        
    def run_interactive(self):
        print("AI Agent CLI - Interactive Mode")
        print("Type 'help' for commands or 'exit' to quit\n")
        
        while True:
            try:
                user_input = input("> ")
                if user_input.lower() == 'exit':
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                elif user_input.startswith('run'):
                    task = user_input[4:].strip()
                    self.execute_task(task)
                elif user_input.startswith('fleet'):
                    self.run_fleet_mode()
                else:
                    print("Unknown command. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                
    def execute_task(self, task):
        print(f"Executing task: {task}")
        result = self.agent_manager.delegate_task(task)
        print(f"Result: {result}")
        
    def run_fleet_mode(self):
        print("Running in fleet mode...")
        fleet_result = self.agent_manager.run_fleet()
        print(f"Fleet result: {fleet_result}")
        
    def _show_help(self):
        print("Available commands:")
        print("  run <task>     - Execute a specific task")
        print("  fleet          - Run fleet mode")
        print("  help           - Show this help")
        print("  exit           - Exit the CLI")
