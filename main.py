import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from avaiable_functions import available_functions
from call_function import call_function
import sys
import time


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

    function_responses = []

    for _ in range(20):
        response_obj = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0))

        if response_obj.candidates:
            for candidate in response_obj.candidates:
                messages.append(candidate.content)

        if response_obj.function_calls:
            for function_call in response_obj.function_calls:

                function_call_result = call_function(function_call=function_call, verbose=args.verbose)

                function_responses.append(function_call_result.parts[0])

                if not function_call_result.parts:
                    raise Exception("Function call result do not posess a parts propertie")
                
                if not function_call_result.parts[0].function_response:
                    raise Exception("Function call result.parts[0] do not posess a function response propertie")
                
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Function call result.parts[0].reponse do not posess a response propertie")
                
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
                time.sleep(2)

            messages.append(types.Content(role="user", parts=function_responses))

        else:
            if response_obj.usage_metadata is None:
                    raise RuntimeError("API request failed")

            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response_obj.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response_obj.usage_metadata.candidates_token_count}")

            print(response_obj.text)

            break

    print("Total number of iterations reached without a response. Progam exited with code 1")

    sys.exit()


if __name__ == "__main__":
    main()
