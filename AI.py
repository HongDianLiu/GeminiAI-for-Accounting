import google.generativeai as genai
from typing import List, Tuple
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
try:
    model = genai.GenerativeModel('gemini-pro')  # Ensure the model name is correct
except Exception as e:
    print(f"Error initializing the model: {e}")
    exit(1)

# Function to reset the conversation
def reset() -> List:
    return []

# Function to call the model to generate and print JSON output
def get_input_and_output_json(user_input: str) -> None:
    '''
    * Arguments

      - user_input: the user input statement to process

    This function processes the user input and outputs a JSON document.
    '''
    chatbot = reset()  # Reset the conversation
    prompt_for_task = """
    Your task is to read the user's text describing an expense and extract the following details:
    - amount: the total amount of the expense.
    - title: the name or title of the expense.
    - description: any additional remarks or information related to the expense (if provided). If the description is provided in the text, include it in the output. Otherwise, set it as an empty string `""`.
    - splitType: how the expense should be split among the group members (equal, shared, or fixed).
    - currency: the currency used in the transaction.

    Guidelines:
    1. If the user mentions a specific description or detail related to the payment, include it in the `description` field.
    2. If no description is provided, return an empty string `""` for the `description` field, not `null`.
    3. If the currency is not specified, assume the default is `"USD"`.
    4. If the splitType is unclear, assume the default is `"equal"`, unless specified otherwise.

    Output the extracted details as a JSON object. If the input cannot be understood, return an error response with `{"error": "text-can-not-be-understood"}` and a 400 status code.

    Examples:

    1. Input:
      "我是 daniel. Group Members 共有 3 位。我今天花了 3178 台幣買了電冰箱，我出 50%"
      Output:
      {
        "amount": 3178,
        "title": "電冰箱",
        "description": "daniel 出 50%",
        "splitType": "shared",
        "currency": "TWD"
      }

    2. Input:
      "I spent 45 USD on office supplies. Split it equally."
      Output:
      {
        "amount": 45,
        "title": "office supplies",
        "description": "",
        "splitType": "equal",
        "currency": "USD"
      }"""

    try:
        # Call the model to generate content
        response = model.generate_content(
            [{'role': 'user', 'parts': [prompt_for_task + "\n" + user_input]}],
            generation_config=genai.types.GenerationConfig(temperature=1.0)
        )

        # Parse the response text as JSON
        response_json = json.loads(response.text)

        # Print the structured response
        print(json.dumps(response_json, indent=2))

    except Exception as e:
        print(f"Error generating content: {e}")