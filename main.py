import os
import json
from dotenv import load_dotenv
from openai_client import OpenAIClient
from user_interaction import UserInteraction
from task_processor import MessageProcessor


# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API token and Assistant ID token from environment variables
OPENAI_API_TOKEN = os.getenv("OPENAI_API_TOKEN")
ASSISTANT_ID_TOKEN = os.getenv("ASSISTANT_ID_TOKEN")


def get_config():
    """Get the configuration from the config.json file."""
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
    
    # Initialize UserInteraction
    ui = UserInteraction(client, thread)
    
    # Instantiate the MessageProcessor
    processor = MessageProcessor(client, thread)
    
    # Collect user details and process the initial message
    user_input = ui.collect_user_details()
    processor.process_message(user_input)
    
    while True:
        # Display available task groups and select one
        task_groups = client.config["task_groups"]
        ui.display_options(task_groups, "TASK GROUPS (Please select a task group)", is_task_group=True)
        
        selected_group = ui.select_option(task_groups, "Please type in the task group number")
        if selected_group is None:
            print("Exiting...")
            break
        
        while True:
            # Display available tasks within the selected group and select one
            tasks = task_groups[selected_group]
            ui.display_options(tasks, f"TASKS ({selected_group})", is_task_group=False)
            
            selected_task = ui.select_option(tasks, "Please type in the task number", back_option=True)
            if selected_task is None:
                break
            processor.process_task("task_groups", selected_group, selected_task)
            
            while True:
                # Allow user to correct responses or proceed
                user_input = ui.correct_responses()
                if user_input is None:
                    break
                elif user_input:
                    processor.process_message(user_input)
                    processor.process_task("function_groups", "corrections", "Task Correction")
                break


if __name__ == "__main__":
    main()
