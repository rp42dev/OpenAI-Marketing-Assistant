def process_message(client, thread, user_input):
    """Function to process the message."""
    client.create_message(thread.id, user_input, "user")


def process_task(client, thread, task, user_input=None):
    """Function to process the selected task."""
    task_name = client.config[task][user_input]['name']
    task_instructions = client.config[task][user_input]['instructions']
    print(f"Processing task {task}: {task_name}")
    
    client.stream_run(thread.id, client.get_assistant().id, task_instructions)
