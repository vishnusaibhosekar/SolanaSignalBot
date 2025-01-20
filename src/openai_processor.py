import time
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_version="2023-07-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# Record the start time
start_time = time.time()

# Send a chat completion request using the faster model
completion = client.chat.completions.create(
    model="gpt-4o-mini",  # Using the faster model
    messages=[
        {
            "role": "user",
            "content": "Explain gravity in one sentence.",
        },
    ],
    max_tokens=50,  # Limit response length
)

# Record the end time
end_time = time.time()

# Print the assistant's response
print(completion.choices[0].message.content)

# Log the elapsed time
print(f"Response time: {end_time - start_time:.2f} seconds")
