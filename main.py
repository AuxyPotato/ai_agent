import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types


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
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print_response(response, prompt_tokens, response_tokens, user_prompt, options)


def prompt():
    if len(sys.argv) < 2:
        print("Error: No prompt provided")
        sys.exit(1)
    else:
        return sys.argv[1]


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