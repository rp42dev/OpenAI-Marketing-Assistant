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


def _print_self_name(func):
    """Decorator to print the name of the class."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(func.__name__.replace("_", " ").title())
        return func(self, *args, **kwargs)
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

    @_handle_api_exceptions
    def openai_completions(self, message):
        """Get completions from the OpenAI API based on the message provided."""
        response = self.client.chat.completions.create(
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
    
    def get_input(prompt):
        """Helper function to get user input and check for 'q' to quit."""
        user_input = input(prompt).strip().lower()
        if user_input == 'q':
            client.delete_thread(thread.id)
            print("Session ended. Goodbye!")
            exit()
        return user_input
    
    while True:
        print("\nType 'q' to quit at any time.")
        
        # Collecting user details
        user_input_niche = get_input("Please type in your niche: ")
        user_input_title = get_input("Please type in your title: ")
        user_input_description = get_input("Please type in your description: ")
        
        niche = f"Niche: {user_input_niche}"
        title = f"Title: {user_input_title}"
        description = f"Description: {user_input_description}"
        user_input = f"{niche}\n{title}\n{description}"

        while True:
            print("-" * 16, "Tasks", "-" * 17)
            
            # Display available tasks
            for task_num, task in client.config["tasks"].items():
                print(f"{task_num}: {task['name']}")
            
            # Get user task input and validate
            user_input_task = get_input("Please type in the task number: ")
            if user_input_task not in client.config["tasks"]:
                print("Invalid task number. Please try again.")
                continue
            
            task = user_input_task
            task_name = client.config['tasks'][task]['name']
            task_instructions = client.config['tasks'][task]['instructions']
            task_role = client.config['tasks'][task]['role']
            
            print(f"Processing task {task}: {task_name}\nInstructions: {task_instructions}\nRole: {task_role}\n")
            
            message = client.create_message(thread.id, user_input, task_role)
            run = client.create_run(thread.id, client.get_assistant().id, task_instructions)
            
            run = client.wait_on_run(run, thread.id)
            response = client.retrieve_message(thread.id, message.id)
            
            print(response)
            break


if __name__ == "__main__":
    main()
