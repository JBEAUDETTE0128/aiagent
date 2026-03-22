import os
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("Unauthorized / Inauthenticated User")

from google import genai

import argparse

from google.genai import types

client = genai.Client(api_key=api_key)

def main():
    print("Hello from aiagent!")

    parser = argparse.ArgumentParser(description="Genai_Chat")
    parser.add_argument("user_prompt", type=str, help="Please input a prompt for Genai")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0)
    )

    if response.usage_metadata is None:
        raise RuntimeError("Failed API Request")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        results_list = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result:
                raise Exception('Function Returned "None"')
            if not function_call_result.parts:
                raise Exception('Empty ".parts" list.')
            if not function_call_result.parts[0].function_response:
                raise Exception('No FunctionResponse object found.')
            if not function_call_result.parts[0].function_response.response:
                raise Exception('No function result found.')
            results_list.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
