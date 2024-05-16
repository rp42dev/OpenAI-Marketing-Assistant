import os
from dotenv import load_dotenv
from functools import wraps
from openai import OpenAI, APIError, APIConnectionError, RateLimitError

import time
import json

load_dotenv()


def get_config():
    with open("config.json") as f:
        return json.load(f)


def handle_api_exceptions(func):
    """Decorator to handle common API exceptions."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (APIError, APIConnectionError, RateLimitError) as e:
            return f"An error occurred: {e}"
    return wrapper

class OpenAIClient:
    """Client for interacting with OpenAI's GPT-3 API for chat-based responses."""
    def __init__(self):
        """Initialize the OpenAIClient with the API key from environment variables."""
        self.config = get_config()
        self.OPENAI_API_TOKEN = os.getenv("OPENAI_API_TOKEN")
        self.ASSISTANT_ID_TOKEN = os.getenv("ASSISTANT_ID_TOKEN")
        self.client = OpenAI(api_key=self.OPENAI_API_TOKEN)
    
    @handle_api_exceptions
    def get_assistant(self):
        """Retrieve the assistant agent from the OpenAI API."""
        assistant = self.client.beta.assistants.retrieve(self.ASSISTANT_ID_TOKEN)
        return assistant
     
    @handle_api_exceptions
    def create_thread(self):
        """Create a new thread."""
        thread = self.client.beta.threads.create()
        return thread
    
    @handle_api_exceptions
    def retrieve_thread(self, thread_id):
        """Retrieve a thread with the assistant agent based on the thread ID."""
        thread = self.client.beta.threads.retrieve(thread_id)   
        return thread
    
    @handle_api_exceptions
    def delete_thread(self, thread_id):
        """Delete a thread based on the thread ID."""
        result = self.client.beta.threads.delete(thread_id)
        return result
    
    @handle_api_exceptions
    def create_run(self, thread_id, assistant_id):
        """Create a new message in the thread with the assistant agent."""
        message = self.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
        return message
    
    @handle_api_exceptions
    def wait_on_run(self, run, thread_id):
        """Waits for the assistant's run to complete."""
        idx = 0
        while run.status in ["queued", "in_progress"]:
            print(f"Waiting for assistant to load...", end="\r")
            idx = (idx + 1) % 4
            time.sleep(0.5)
            run = self.client.beta.threads.runs.retrieve(
                run_id=run.id, thread_id=thread_id
            )
        return run
    
    @handle_api_exceptions
    def create_message(self, thread_id, content, role):
        """Create a new message in the thread with the specified content and role."""
        message = self.client.beta.threads.messages.create(thread_id=thread_id, content=content, role=role)
        return message
    
    @handle_api_exceptions
    def retrieve_message(self, thread_id, message_id):
        """Retrieve a message based on the message ID."""
        messages = self.client.beta.threads.messages.list(
                thread_id=thread_id, order="asc", after=message_id
            )
        return messages.data[0].content[0].text.value

    @handle_api_exceptions
    def openai_completions(self, message):
        """Get completions from the OpenAI API based on the message provided."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=1000,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
        )
        return response.choices[0].message.content

def main():
    """Main function to run the chat interaction with the OpenAIClient."""

    client = OpenAIClient()
    thread = client.create_thread()
    while True:
        message = input("You: ")
        if message == "exit":
            client.delete_thread(thread.id)
            break
        message = client.create_message(thread.id, message, "user")
        run = client.create_run(thread.id, client.get_assistant().id)
        run = client.wait_on_run(run, thread.id)
        print(client.retrieve_message(thread.id, message.id))


if __name__ == "__main__":
    main()
