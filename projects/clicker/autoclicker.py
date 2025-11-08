import time
import threading
from pynput.mouse import Button, Controller

def auto_clicker():
    mouse = Controller()
    clicks = 0
    start_time = time.time()
    
    while clicks < 10000:
        mouse.click(Button.left, 1)
        clicks += 1
        
        # Small delay to prevent system overload
        time.sleep(0.000000001)
    
    end_time = time.time()
    print(f"Completed {clicks} clicks in {end_time - start_time:.2f} seconds")

def main():
    print("Auto clicker will start in 3 seconds. Position your cursor.")
    time.sleep(3)
    print("Starting auto clicker...")
    
    # Run the clicker in a separate thread to allow for potential interruption
    clicker_thread = threading.Thread(target=auto_clicker)
    clicker_thread.start()
    clicker_thread.join()
    
    print("Auto clicker finished.")

if __name__ == "__main__":
    main()
