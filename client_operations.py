import os
from dotenv import load_dotenv
from functools import wraps
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
import time
import json

load_dotenv()

def get_config():
    """
    Get the configuration from the config.json file.
    Task name, instructions, and role are defined in the config.json file.
    """
    with open("config.json") as f:
        return json.load(f)

def _handle_api_exceptions(func):
    """Decorator to handle common API exceptions."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (APIError, APIConnectionError, RateLimitError) as e:
            return f"An error occurred in the \"{func.__name__}\" function: {e}"
    return wrapper

class OpenAIClient:
    """Client for interacting with OpenAI's GPT API."""
    def __init__(self):
        """Initialize the OpenAIClient with the API key from environment variables."""
        self.config = get_config()
        self.OPENAI_API_TOKEN = os.getenv("OPENAI_API_TOKEN")
        self.ASSISTANT_ID_TOKEN = os.getenv("ASSISTANT_ID_TOKEN")
        self.client = OpenAI(api_key=self.OPENAI_API_TOKEN)
    
    @_handle_api_exceptions
    def get_assistant(self):
        """Retrieve the assistant agent from the OpenAI API."""
        assistant = self.client.beta.assistants.retrieve(self.ASSISTANT_ID_TOKEN)
        return assistant
     
    @_handle_api_exceptions
    def create_thread(self):
        """Create a new thread."""
        thread = self.client.beta.threads.create()
        return thread
    
    @_handle_api_exceptions
    def retrieve_thread(self, thread_id):
        """Retrieve a thread with the assistant agent based on the thread ID."""
        thread = self.client.beta.threads.retrieve(thread_id)   
        return thread
    
    @_handle_api_exceptions
    def delete_thread(self, thread_id):
        """Delete a thread based on the thread ID."""
        result = self.client.beta.threads.delete(thread_id)
        return result
    
    @_handle_api_exceptions
    def create_run(self, thread_id, assistant_id, task_instructions):
        """Create a new message in the thread with the assistant agent."""
        message = self.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, instructions=task_instructions)
        return message
    
    @_handle_api_exceptions
    def wait_on_run(self, run, thread_id):
        """Waits for the assistant's run to complete."""
        idx = 0
        while run.status in ["queued", "in_progress"]:
            print(f"Waiting for the assistant to complete the task... ({idx + 1})", end="\r")
            idx = (idx + 1) % 4
            time.sleep(0.5)
            run = self.client.beta.threads.runs.retrieve(
                run_id=run.id, thread_id=thread_id
            )
        return run
    
    @_handle_api_exceptions
    def create_message(self, thread_id, content, role):
        """Create a new message in the thread with the specified content and role."""
        message = self.client.beta.threads.messages.create(thread_id=thread_id, content=content, role=role)
        return message
    
    @_handle_api_exceptions
    def retrieve_message(self, thread_id, message_id):
        """Retrieve a message based on the thread ID and message ID."""
        messages = self.client.beta.threads.messages.list(
                thread_id=thread_id, order="asc", after=message_id
            )
        return messages.data[0].content[0].text.value
