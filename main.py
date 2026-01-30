import os
from dotenv import load_dotenv
from google import genai

client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-assistant!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Environment Variable Not Found")
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    print(response.text)


if __name__ == "__main__":
    main()
