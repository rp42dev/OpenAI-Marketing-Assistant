import os
import json
from dotenv import load_dotenv
from openai_client import OpenAIClient
from user_interaction import collect_user_details, display_tasks, select_task, correct_responses
from task_processor import process_task, process_message, correct_task_response

load_dotenv()

OPENAI_API_TOKEN = os.getenv("OPENAI_API_TOKEN")
ASSISTANT_ID_TOKEN = os.getenv("ASSISTANT_ID_TOKEN")


def get_config():
    """
    Get the configuration from the config.json file.
    Task name, instructions, and role are defined in the config.json file.
    """
    with open("config.json") as f:
        return json.load(f)


def main():
    """Main function to run the chat interaction with the OpenAIClient."""
    config = get_config()

    # Initialize the OpenAIClient
    client = OpenAIClient(config=config, api_key=OPENAI_API_TOKEN, assistant_id=ASSISTANT_ID_TOKEN)
    thread = client.create_thread()

    print("\nType 'q' to quit at any time.", end="\n\n")
    user_input = collect_user_details(client, thread)

    process_message(client, thread, user_input)
    
    idx = 0
    while True:
        if not idx == 0:
            print("\nType 'q' to quit at any time.", end="\n\n")
            idx += 1

        display_tasks(client)
        task = select_task(client, thread)
        
        process_task(client, thread, task)
        
        while True:
            user_input = correct_responses()
        
            if user_input:
                correct_task_response(client, thread, user_input, task)
            else:
                break

if __name__ == "__main__":
    main()
