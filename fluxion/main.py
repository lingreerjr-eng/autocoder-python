import argparse
import sys
from cli.cli import CLI

def main():
    parser = argparse.ArgumentParser(description='AI Agent CLI')
    parser.add_argument('--model', default='llama3', help='Ollama model to use')
    parser.add_argument('--fleet', action='store_true', help='Run in fleet mode')
    parser.add_argument('--task', type=str, help='Direct task to execute')
    
    args = parser.parse_args()
    
    cli = CLI(model=args.model)
    
    if args.fleet:
        cli.run_fleet_mode()
    elif args.task:
        cli.execute_task(args.task)
    else:
        cli.run_interactive()

if __name__ == "__main__":
    main()
