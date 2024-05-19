def get_input(prompt, client, thread):
    """Helper function to get user input and check for 'q' to quit."""
    user_input = input(prompt).strip().lower()
    if user_input == 'q':
        client.delete_thread(thread.id)
        print("Session ended. Goodbye!")
        exit()
    return user_input

def collect_user_details(client, thread):
    """Function to collect user details."""
    print("\nType 'q' to quit at any time.")
    niche = f"Niche: {get_input('Please type in your niche: ', client, thread)}"
    title = f"Title: {get_input('Please type in your title: ', client, thread)}"
    description = f"Description: {get_input('Please type in your description: ', client, thread)}"
    return f"{niche}\n{title}\n{description}"

def display_tasks(client):
    """Function to display available tasks."""
    print("-" * 16, "Tasks", "-" * 17)
    for task_num, task in client.config["tasks"].items():
        print(f"{task_num}: {task['name']}")

def select_task(client, thread):
    """Function to select a task and validate the selection."""
    while True:
        user_input_task = get_input("Please type in the task number: ", client, thread)
        if user_input_task in client.config["tasks"]:
            return user_input_task
        print("Invalid task number. Please try again.")
