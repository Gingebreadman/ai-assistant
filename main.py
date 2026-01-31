import os
from dotenv import load_dotenv
from google import genai

def main():
    print("Hello from ai-assistant!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("Environment Variable Not Found")

    client = genai.Client(api_key=api_key)

    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    # --- NEW: Validate usage metadata ---
    if response.usage_metadata is None:
        raise RuntimeError("API request failed: no usage metadata returned")

    # --- NEW: Print token counts ---
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # --- Print the model response ---
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
