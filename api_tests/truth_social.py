from dotenv import load_dotenv
import os
import json

load_dotenv()
print("Username:", os.getenv("TRUTHSOCIAL_USERNAME"))  # Debugging


import subprocess

command = ["truthbrush", "search", "--searchtype", "statuses", "Trump Coin"]
result = subprocess.run(command, capture_output=True, text=True)

data = json.loads(result.stdout)
print(len(data))
