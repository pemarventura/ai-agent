import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions


load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")


def main():
    if api_key is None:
        raise RuntimeError("enviroment API key not found")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response_obj = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0))

    if response_obj.function_calls:
        for function_call in response_obj.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

    else:
        if response_obj.usage_metadata is None:
                raise RuntimeError("API request failed")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response_obj.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response_obj.usage_metadata.candidates_token_count}")

        print(response_obj.text)


if __name__ == "__main__":
    main()
