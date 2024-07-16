from openai import OpenAI
from openai_event_handler import EventHandler
from decorators import _handle_api_exceptions


class OpenAIClient:
    """
    Client for interacting with OpenAI's GPT API.
    Methods: get_assistant, create_thread, retrieve_thread, delete_thread, stream_run, create_message, retrieve_message
    """
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
    def retrieve_thread(self, thread_id: str):
        """Retrieve a thread with the assistant agent based on the thread ID."""
        thread = self.client.beta.threads.retrieve(thread_id)   
        return thread
    
    @_handle_api_exceptions
    def delete_thread(self, thread_id: str):
        """Delete a thread based on the thread ID."""
        result = self.client.beta.threads.delete(thread_id)
        return result
    
    @_handle_api_exceptions
    def stream_run(self, thread_id: str, assistant_id: str, task_instructions: str):
        """Stream the assistant's run process."""
        with self.client.beta.threads.runs.stream(
            thread_id=thread_id, 
            assistant_id=assistant_id, 
            instructions=task_instructions,
            event_handler=EventHandler()
            ) as stream:
            stream.until_done()
    
    @_handle_api_exceptions
    def create_message(self, thread_id: str, content: str, role: str):
        """Create a new message in the thread with the specified content and role."""
        message = self.client.beta.threads.messages.create(thread_id=thread_id, content=content, role=role)
        return message
    
    @_handle_api_exceptions
    def retrieve_message(self, thread_id: str, message_id: str):
        """Retrieve a message based on the thread ID and message ID."""
        messages = self.client.beta.threads.messages.list(
                thread_id=thread_id, order="asc", after=message_id
            )
        return messages.data[0].content[0].text.value
