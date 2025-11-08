import sys

class IOHandler:
    def __init__(self):
        pass
        
    def read_input(self, prompt=""):
        if prompt:
            print(prompt, end='', flush=True)
        return sys.stdin.readline().strip()
        
    def write_output(self, message):
        print(message)
        
    def write_error(self, error_message):
        print(f"Error: {error_message}", file=sys.stderr)
