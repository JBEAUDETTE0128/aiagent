import os
from dotenv import load_dotenv

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
        model='gemini-2.5-flash', contents=messages
    )

    if response.usage_metadata is None:
        raise RuntimeError("Failed API Request")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)

if __name__ == "__main__":
    main()
