def get_input(prompt, client, thread):
    """Helper function to get user input and check for 'q' to quit."""
    try:
        user_input = input(f"q to quit | {prompt}").strip()
    except (KeyboardInterrupt, EOFError):
        client.delete_thread(thread.id)
        print("\nSession ended. Goodbye!")
        exit()
    if user_input == 'q':
        client.delete_thread(thread.id)
        print("\nSession ended. Goodbye!")
        exit()
    return user_input


def collect_user_details(client, thread):
    """Function to collect niche details."""
    print("DETAILS", "-" * 23, end="\n")
    title = f"Title: {get_input('Please type in title: ', client, thread)}"
    description = f"Description: {get_input('Please type in description: ', client, thread)}"
    return f"{title}\n{description}"


def display_tasks(client):
    """Function to display available tasks."""
    print("\nTASKS", "-" * 25, end="\n")
    for task_num, task in list(client.config["tasks"].items())[:-1]:
        print(f"{task_num}: {task['name']}")
    print("-" * 30)


def select_task(client, thread):
    """Function to select a task and validate the selection."""
    while True:
        user_input_task = get_input("Please type in the task number: ", client, thread)
        if user_input_task in client.config["tasks"]:
            return user_input_task
        print("Invalid task number. Please try again.", end="\n")


def correct_responses(client, thread):
    """Function to alow user to correct responses."""
    while True:
        user_input = get_input("Would you like to make corrections to the response? (yes/no): ", client, thread)
        if user_input == 'yes':
            user_input = get_input("Please type in your corrections: ", client, thread)
            return user_input
        elif user_input == 'no':
            return False
        print("Invalid input. Please try again.")
