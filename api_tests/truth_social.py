from dotenv import load_dotenv
import subprocess
import os
import json

load_dotenv()
print("Username:", os.getenv("TRUTHSOCIAL_USERNAME"))  # Debugging

command = ["truthbrush", "search", "--searchtype", "statuses", "Elon Musk"]
result = subprocess.run(command, capture_output=True, text=True)

if result.stdout:
    data = json.loads(result.stdout)
    for truth in data:
        print(truth['content'])
else:
    print(result.stderr)
