from dotenv import load_dotenv
import subprocess
import os
import json
import time

load_dotenv()
print("Username:", os.getenv("TRUTHSOCIAL_USERNAME"))  # Debugging

def run_command_with_retries(command, max_retries=5, initial_delay=5):
    """
    Attempting to request Truth Social tweets, however, if we get flagged for bots
    we will call them again after a wait to keep trying
    """
    attempt = 1
    delay = initial_delay
    while attempt <= max_retries:
        print(f"\nAttempt {attempt}...")
        result = subprocess.run(command, capture_output=True, text=True, env=os.environ)
        
        if result.stdout:
            try:
                data = json.loads(result.stdout)
                return data
            except json.JSONDecodeError as e:
                print("JSON decode error. Waiting and retrying...", e)
        else:
            print("Cloudflare block detected. Waiting and retrying...")
        
        time.sleep(delay)
        delay *= 2
        attempt += 1

    return None

command = ["truthbrush", "search", "--searchtype", "statuses", "SOL"]
data = run_command_with_retries(command, max_retries=5, initial_delay=5)

if data:
    for truth in data:
        print(truth.get('content', ''))
else:
    print("Failed to retrieve valid output after multiple retries.")