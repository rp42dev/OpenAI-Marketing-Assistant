from openai_client import OpenAIClient
from user_interaction import collect_user_details, display_tasks, select_task
from task_processor import process_task

def main():
    """Main function to run the chat interaction with the OpenAIClient."""
    client = OpenAIClient()
    thread = client.create_thread()

    while True:
        user_input = collect_user_details(client, thread)
        display_tasks(client)
        task = select_task(client, thread)
        process_task(client, thread, task, user_input)

if __name__ == "__main__":
    main()
