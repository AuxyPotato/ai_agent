import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import prompt, system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = prompt()
    options = parse_arguments()
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt()),
    )
    print_response(response,
                   response.usage_metadata.prompt_token_count,
                   response.usage_metadata.candidates_token_count,
                   user_prompt, options)


def parse_arguments():
    parser = argparse.ArgumentParser(prog="main.py")
    parser.add_argument("prompt")
    parser.add_argument("--verbose", "-v", action="store_true")
    return parser.parse_args()


def print_response(response, prompt_tokens, response_tokens, user_prompt, options):
    if options.verbose:
        print(f"User prompt: {user_prompt} \n")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens} \n")
    print(response.text)


if __name__ == "__main__":
    main()
