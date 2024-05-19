def process_task(client, thread, task, user_input):
    """Function to process the selected task."""
    task_name = client.config['tasks'][task]['name']
    task_instructions = client.config['tasks'][task]['instructions']
    task_role = client.config['tasks'][task]['role']
    print(f"\nProcessing task {task}: {task_name}\nInstructions: {task_instructions}\nRole: {task_role}")
    
    client.create_message(thread.id, user_input, task_role)
    client.stream_run(thread.id, client.get_assistant().id, task_instructions)