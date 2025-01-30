import time
import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_version="2023-07-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# Load prompt template from file
def load_prompt_template():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script path
    file_path = os.path.join(base_dir, "trade_prompt.txt")  # Load from same directory
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Extract contract address (assumes first long alphanumeric string is the contract address)
def extract_contract_address(trading_signal):
    words = trading_signal.split()
    for word in words:
        if len(word) > 30 and all(c.isalnum() or c in "._-" for c in word):  # Rough heuristic
            return word
    return "Unknown"

# Function to classify the trade type and determine the function name & allocation percentage
def get_trade_decision(trading_signal, prompt_template):
    prompt = prompt_template.replace("{trading_signal}", trading_signal)

    start_time = time.time()

    # Call Azure OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20,  # Enough for function & allocation
    )

    end_time = time.time()

    # Extract response and clean it
    decision_text = response.choices[0].message.content.strip()

    print(f"Response Time: {end_time - start_time:.2f} seconds")
    
    try:
        decision = json.loads(decision_text)  # Parse as JSON
    except json.JSONDecodeError:
        print("Invalid JSON output from LLM:", decision_text)
        return None

    return decision

# Main Execution
if __name__ == "__main__":
    test_signal = """🚀 Buy $STANLEY at 0.004 SOL
    
    EPR4FLREVCD4BX9JNrSitDap66hVtquADqjykoNY3L2J
    
    Target 10x, but be cautious - partial sells recommended at 3x, 6x.
    
    High risk, but huge upside if we get volume."""

    # Load the prompt template
    prompt_template = load_prompt_template()

    # Get trading decision (LLM classifies buy/sell, limit/market & allocation %)
    decision = get_trade_decision(test_signal, prompt_template)

    if decision:
        # Extract contract address
        contract_address = extract_contract_address(test_signal)

        # Prepare final JSON output
        output = {
            "Function": decision["Function"],  # The function name LLM provides
            "Args": ["0.004", decision["Percentage"]],  # Example: 0.004 SOL, {allocation}% buy
            "Contract_address": contract_address
        }

        # Print JSON result
        print(json.dumps(output, indent=4))
