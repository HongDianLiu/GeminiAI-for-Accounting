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
model = genai.GenerativeModel('gemini-pro')

# Check if you have set your Gemini API successfully
# You should see "Set Gemini API sucessfully!!" if nothing goes wrong.
try:
    model.generate_content(
      "test",
    )
    print("Set Gemini API sucessfully!!")
except:
    print("There seems to be something wrong with your Gemini API. Please follow our demonstration in the slide to get a correct one.")

chatbot_task = "The chatbot can read a user's text describing an expense and extract important details like amount, title, description, splitType, and currency, and then return this information in a structured JSON format."
prompt_for_task = """Read the user's text describing an expense, extract and format the necessary information into a JSON object. Each description will include details about the amount, the title of the expense, optional description or remarks, how the expense should be split among the group members, and the currency used. Identify these elements from the text and construct a JSON object with the fields: amount, title, description (optional), splitType, and currency. The following are the good examples:
----------------------
'Yesterday, I paid 45 USD for office supplies. We should split it equally among the four of us.' From this, you should extract:
{
  amount: 45,
  title: 'office supplies',
  description: '',
  splitType: 'equal',
  currency: 'USD'
}

'I just subscribed to a premium music service for 10 TWD per person, totaling 40 TWD.' Here, the JSON should be:
{
  amount: 40,
  title: 'premium music service subscription',
  description: '',
  splitType: 'equal',
  currency: 'TWD'
}"

'我是 daniel. Group Members 共有 3 位。我今天花了 3178 台幣買了電冰箱，我出 50%' Here, the JSON should be:
{
  amount: 3178,
  title: '電冰箱',
  description: 'daniel 出 50%',
  splitType: 'shared',
  currency: 'TWD'
}"
----------------------
Clarify the meanings of each field and the formats they should take, especially explaining how to interpret the split types:
Equal: The amount is divided equally among all members.
Shared: The amount is divided based on the percentage shares specified.
Fixed: Each member pays a fixed amount, and the total might need to be calculated.

"If the input text does not specify the currency, default to 'USD'. If the split type is unclear from the user's description, assume 'equal' split unless stated otherwise."

If you cannot understand user's text, response {"error": "text-can-not-be-understood"} with 400 Bad Request"""

# function to clear the conversation
def reset() -> List:
    return []

# function to call the model to generate
def interact_customize(chatbot: List[Tuple[str, str]], prompt: str ,user_input: str, temp = 1.0) -> List[Tuple[str, str]]:
    '''
    * Arguments

      - chatbot: the model itself, the conversation is stored in list of tuples

      - prompt: the prompt for your desginated task

      - user_input: the user input of each round of conversation

      - temp: the temperature parameter of this model. Temperature is used to control the output of the chatbot.
              The higher the temperature is, the more creative response you will get.

    '''
    try:
        messages = []

        for input_text, response_text in chatbot:
            messages.append({'role': 'user', 'parts': [input_text]})
            messages.append({'role': 'model', 'parts': [response_text]})

        messages.append({'role': 'user', 'parts': [prompt+ "\n" + user_input]})

        response = model.generate_content(
          messages,
          generation_config=genai.types.GenerationConfig(temperature=temp),
          safety_settings=[
          {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE",},
          {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE",},
          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE",},
          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE",},
          ]
        )

        chatbot.append((user_input, response.text))

    except Exception as e:
        print(f"Error occurred: {e}")
        chatbot.append((user_input, f"Sorry, an error occurred: {e}"))
    return chatbot

def export_customized(chatbot: List[Tuple[str, str]], description: str) -> None:
    '''
    * Arguments

      - chatbot: the model itself, the conversation is stored in list of tuples

      - description: the description of this task

    '''
    target = {"chatbot": chatbot, "description": description}
    with open("part3.json", "w") as file:
        json.dump(target, file)

def get_input_and_output_json(user_input: str) -> None:
    '''
    * Arguments

      - user_input: the user input statement to process

    This function processes the user input and outputs a JSON document.
    '''
    # Call the interact_customize function to get the chatbot response
    chatbot = reset()  # Reset the conversation
    response_chatbot = interact_customize(chatbot, prompt_for_task, user_input)

    # Export the response to a JSON file
    export_customized(response_chatbot, "Expense extraction task")

# Example usage
get_input_and_output_json("I paid 50 for office supplies. Split it equally among the four of us.")