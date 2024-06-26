from functools import wraps
from openai import OpenAI, APIError, APIConnectionError, RateLimitError

from openai_event_handler import EventHandler


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
    def __init__(self, config=None, api_key=None, assistant_id=None):
        """Initialize the OpenAIClient with the API key from environment variables."""
        self.config = config
        self.OPENAI_API_TOKEN = api_key
        self.ASSISTANT_ID_TOKEN = assistant_id
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
    def stream_run(self, thread_id, assistant_id, task_instructions):
        """Stream the assistant's run process."""
        with self.client.beta.threads.runs.stream(
            thread_id=thread_id, 
            assistant_id=assistant_id, 
            instructions=task_instructions,
            event_handler=EventHandler()
            ) as stream:
            stream.until_done()
    
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
