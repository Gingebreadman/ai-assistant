import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    print("Hello from ai-assistant!")

    # -----------------------------
    # Parse CLI arguments
    # -----------------------------
    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # -----------------------------
    # Load API key
    # -----------------------------
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Environment Variable Not Found")

    client = genai.Client(api_key=api_key)

    # -----------------------------
    # Initialize conversation
    # -----------------------------
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]

    # -----------------------------
    # Agent Loop
    # -----------------------------
    for _ in range(20):

        # 1. Call the model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0
            ),
        )

        # 2. Add model candidates to conversation history
        if response.candidates:
            for c in response.candidates:
                messages.append(c.content)

        # 3. If no function calls → final answer
        if not response.function_calls:
            print("Final response:")
            print(response.text)
            return

        # 4. Execute function calls
        function_results = []

        for fc in response.function_calls:
            function_call_result = call_function(fc, verbose=args.verbose)

            # Validate returned Content object
            if not function_call_result.parts:
                raise RuntimeError("Function call returned no parts")

            fr = function_call_result.parts[0].function_response
            if fr is None:
                raise RuntimeError("Function response missing")

            if fr.response is None:
                raise RuntimeError("Function response missing .response field")

            # Save result for next iteration
            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {fr.response}")

        # 5. Add function results to conversation history
        messages.append(
            types.Content(
                role="user",
                parts=function_results
            )
        )

    # -----------------------------
    # Loop ended without final answer
    # -----------------------------
    print("Error: Agent exceeded maximum iterations without producing a final response.")
    exit(1)


if __name__ == "__main__":
    main()
