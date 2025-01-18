import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the OpenAI API key and endpoint
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2023-05-15"  # Adjust this based on your API version

# Define the deployment name (model engine)
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Print the endpoint for debugging
print(f"Endpoint: {openai.api_base}")
print(f"Deployment Name: {deployment_name}")

# Test the setup by making a request to Azure OpenAI Chat Completion
try:
    response = openai.ChatCompletion.create(
        engine=deployment_name,  # Use your deployment name here
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"},
        ],
        max_tokens=5,
        temperature=0.7,
    )

    # Print the response
    print(response['choices'][0]['message']['content'].strip())

except openai.error.InvalidRequestError as e:
    print(f"Invalid Request Error: {e}")
except Exception as e:
    print(f"Error: {e}")
