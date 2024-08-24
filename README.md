# GeminiAI-for-Accounting

## Overview

The **GeminiAI-for-Accounting** is a Python-based tool that utilizes the Google Gemini API to analyze user-provided expense statements. It processes input text to extract key information such as the amount, title, description, split type, and currency, and returns this data in a structured JSON format.

## Features

- Supports expense statement parsing in both English and Chinese.
- Automatically structures the extracted data into a clean JSON format.
- Handles various input formats, applying default values where necessary.

## Requirements

- Python 3.x
- `google-generativeai` library
- `python-dotenv` library

## Installation

1. **Install the required packages** using pip:

   ```bash
   pip install google-generativeai python-dotenv
   ```

2. **Set up your API key**:
   - Create a `.env` file in the project directory.
   - Add your Google API key to the `.env` file:

     ```
     GOOGLE_API_KEY=type_your_api_key_here
     ```

## Usage

1. **Run the script** from your terminal:

   ```bash
   python AI.py
   ```

2. **Provide your expense statement** at the prompt. For example:

   ```
   Enter your expense statement: I spent 50 USD on groceries.
   ```

3. **View the output**: The script will process your input and print the extracted details in JSON format. Example:

   ```json
   {
     "amount": 50,
     "title": "groceries",
     "description": "",
     "splitType": "equal",
     "currency": "USD"
   }
   ```

4. **Exit the program** by typing `exit` at the prompt.

## Example Inputs and Outputs

- **Input**: 
  ```
  I spent 45 USD on office supplies. Split it equally.
  ```
  **Output**:
  ```json
  {
    "amount": 45,
    "title": "office supplies",
    "description": "",
    "splitType": "equal",
    "currency": "USD"
  }
  ```

- **Input**: 
  ```
  我是 daniel. Group Members 共有 3 位。我今天花了 3178 台幣買了電冰箱，我出 50%
  ```
  **Output**:
  ```json
  {
    "amount": 3178,
    "title": "電冰箱",
    "description": "daniel 出 50%",
    "splitType": "shared",
    "currency": "TWD"
  }
  ```

## Error Handling

If the input is unclear or unrecognizable, the script will return an error message to indicate the issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
