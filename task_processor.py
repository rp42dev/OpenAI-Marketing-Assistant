def process_task(client, thread, task, user_input):
    """Function to process the selected task."""
    task_name = client.config['tasks'][task]['name']
    task_instructions = client.config['tasks'][task]['instructions']
    task_role = client.config['tasks'][task]['role']
    
    print(f"Processing task {task}: {task_name}\nInstructions: {task_instructions}\nRole: {task_role}\n")
    
    message = client.create_message(thread.id, user_input, task_role)
    run = client.stream_run(thread.id, client.get_assistant().id, task_instructions)
    
    response = client.retrieve_message(thread.id, message.id)
    
    print(response)
