def get_input(prompt, client, thread):
    """Helper function to get user input and check for 'q' to quit."""
    try:
        user_input = input(prompt).strip().lower()
        print()
    except (KeyboardInterrupt, EOFError):
        client.delete_thread(thread.id)
        print("\n\nSession ended. Goodbye!")
        exit()
    if user_input == 'q':
        client.delete_thread(thread.id)
        print("\n\nSession ended. Goodbye!")
        exit()
    return user_input

def collect_user_details(client, thread):
    """Function to collect user details."""
    print("Details", "-" * 23, end="\n")
    title = f"Title: {get_input('Please type in your title: ', client, thread)}"
    description = f"Description: {get_input('Please type in your description: ', client, thread)}"
    return f"{title}\n{description}"

def display_tasks(client):
    """Function to display available tasks."""
    print("Tasks", "-" * 25, end="\n")
    for task_num, task in client.config["tasks"].items():
        print(f"{task_num}: {task['name']}")

def select_task(client, thread):
    """Function to select a task and validate the selection."""
    while True:
        user_input_task = get_input("\nPlease type in the task number: ", client, thread)
        if user_input_task in client.config["tasks"]:
            return user_input_task
        print("Invalid task number. Please try again.\n\n")
