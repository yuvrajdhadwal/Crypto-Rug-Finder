from dotenv import load_dotenv
import subprocess
import os
import json
import time

load_dotenv()
print("Username:", os.getenv("TRUTHSOCIAL_USERNAME"))  # Debugging

def run_command_with_retries(command, max_retries=5, initial_delay=5):
    attempt = 1
    delay = initial_delay
    while attempt <= max_retries:
        print(f"\nAttempt {attempt}...")
        result = subprocess.run(command, capture_output=True, text=True, env=os.environ)
        
        # Check if we received output
        if result.stdout:
            try:
                data = json.loads(result.stdout)
                return data  # Success, return the parsed JSON
            except json.JSONDecodeError as e:
                # Check if the output appears to be Cloudflare's HTML block
                if "<!DOCTYPE html>" in result.stdout:
                    print("Cloudflare block detected. Waiting and retrying...")
                else:
                    print("JSON decode error. Waiting and retrying...", e)
        else:
            print("No stdout received. STDERR:", result.stderr)
        
        # Wait and then try again
        time.sleep(delay)
        delay *= 2  # Exponential backoff
        attempt += 1

    return None

command = ["truthbrush", "search", "--searchtype", "statuses", "SOL"]
data = run_command_with_retries(command, max_retries=5, initial_delay=5)

if data:
    for truth in data:
        print(truth.get('content', ''))
else:
    print("Failed to retrieve valid output after multiple retries.")