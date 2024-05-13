import os
from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, RateLimitError

load_dotenv()

class OpenAIClient:
    """Client for interacting with OpenAI's GPT-3 API for chat-based responses."""

    def __init__(self):
        """Initialize the OpenAIClient with the API key from environment variables."""
        self.OPENAI_API_TOKEN = os.getenv("OPENAI_API_TOKEN")
        self.client = OpenAI(api_key=self.OPENAI_API_TOKEN)

    def openai_chat(self, message):
        """
        Generate a response using the GPT-3.5 model based on user input.

        Args:
            message (str): The user's message to generate a response for.

        Returns:
            str: The AI-generated response based on the user's input.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                max_tokens=1000,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message},
                ],
            )
        except (APIError, APIConnectionError, RateLimitError) as e:
            return f"An error occurred: {e}"

        return response.choices[0].message.content

def main():
    """Main function to run the chat interaction with the OpenAIClient."""
    client = OpenAIClient()

    while True:
        message = input("You: ")
        if message == "exit":
            break
        print("AI: ", client.openai_chat(message))

if __name__ == "__main__":
    main()
