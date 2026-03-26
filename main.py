import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import prompt, system_prompt
from call_functions import available_functions, call_function


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
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt()),
    )

    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        function_result = call_function(function_call)
        if not function_result.parts:
            raise Exception("Function result is empty - parts list is empty")
        if not function_result.parts[0].function_response:
            raise Exception("Function result is empty - function_response is None")
        if not function_result.parts[0].function_response.response:
            raise Exception(f"Function result is empty - response is: {function_result.parts[0].function_response.response}")
        results_list = [function_result.parts[0]]

        print_response(response, function_result,
                       response.usage_metadata.prompt_token_count,
                       response.usage_metadata.candidates_token_count,
                       user_prompt, options)


def parse_arguments():
    parser = argparse.ArgumentParser(prog="main.py")
    parser.add_argument("prompt")
    parser.add_argument("--verbose", "-v", action="store_true")
    return parser.parse_args()


def print_response(response, function_result, prompt_tokens,
                   response_tokens, user_prompt, options):
    if options.verbose:
        print(f"User prompt: {user_prompt} \n")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens} \n")
        print(f"-> {function_result.parts[0].function_response.response}")
    if response.candidates[0].content.parts[0].function_call:
        part = response.candidates[0].content.parts[0]
        print(f"Calling function: {part.function_call.name}({part.function_call.args})")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
