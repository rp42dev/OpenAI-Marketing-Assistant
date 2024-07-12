def process_message(client, thread, user_input):
    """Function to process the message."""
    client.create_message(thread.id, user_input, "user")


def process_task(client, thread, task):
    """Function to process the selected task."""
    task_name = client.config['tasks'][task]['name']
    task_instructions = client.config['tasks'][task]['instructions']
    print(f"\nProcessing task {task}: {task_name}")
    
    client.stream_run(thread.id, client.get_assistant().id, task_instructions)


def correct_task_response(client, thread, user_input, task):
    """Function to correct the task response."""
    task_instructions = f"Make corrections to the previous response based on user input"
    process_message(client, thread, user_input)
    print(f"\nCorrecting the response for task {task}: {client.config['tasks'][task]['name']}")
    
    client.stream_run(thread.id, client.get_assistant().id, task_instructions)
    
    