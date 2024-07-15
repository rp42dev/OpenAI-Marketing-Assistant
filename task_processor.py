def process_message(client, thread, user_input):
    """Function to process the message."""
    client.create_message(thread.id, user_input, "user")


def process_task(client, thread, group, stage, user_input):
    """Function to process the selected task."""
    task_name = client.config[group][stage][user_input]['name']
    task_instructions = client.config[group][stage][user_input]['instructions']
    print(f"\nProcessing task: {task_name}")
    
    client.stream_run(thread.id, client.get_assistant().id, task_instructions)
