import os
import json
from dotenv import load_dotenv
from openai_client import OpenAIClient
from user_interaction import collect_user_details, display_tasks, select_task, correct_responses, display_task_groups, select_task_group
from task_processor import process_task, process_message

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API token and Assistant ID token from environment variables
OPENAI_API_TOKEN = os.getenv("OPENAI_API_TOKEN")
ASSISTANT_ID_TOKEN = os.getenv("ASSISTANT_ID_TOKEN")


def get_config():
    """
    Get the configuration from the config.json file.
    """
    with open("config.json") as f:
        return json.load(f)


def main():
    """Main function to run the chat interaction with the OpenAIClient."""
    # Load configuration
    config = get_config()
    
    # Initialize the OpenAI client
    client = OpenAIClient(config=config, api_key=OPENAI_API_TOKEN, assistant_id=ASSISTANT_ID_TOKEN)
    
    # Create a new thread for the session
    thread = client.create_thread()
    
    # Collect user details and process the initial message
    user_input = collect_user_details(client, thread)
    process_message(client, thread, user_input)
    
    while True:
        # Display available task groups and select one
        task_groups = client.config["task_groups"]
        display_task_groups(task_groups)
        
        selected_group = select_task_group(task_groups, client, thread)
        
        while True:
            # Display available tasks within the selected group and select one
            tasks = task_groups[selected_group]
            display_tasks(tasks)
            
            selected_task = select_task(tasks, client, thread)
            if selected_task is None:
                break
            
            process_task(client, thread, "task_groups", selected_group, selected_task)
            
            while True:
                # Allow user to correct responses or proceed
                user_input = correct_responses(client, thread)
                if user_input:
                    process_message(client, thread, user_input)
                else:
                    break


if __name__ == "__main__":
    main()
