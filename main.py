import os
import json
from dotenv import load_dotenv
from openai_client import OpenAIClient
from user_interaction import collect_user_details, display_tasks, select_task
from task_processor import process_task

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

    while True:
        user_input = collect_user_details(client, thread)
        display_tasks(client)
        task = select_task(client, thread)
        process_task(client, thread, task, user_input)

if __name__ == "__main__":
    main()
