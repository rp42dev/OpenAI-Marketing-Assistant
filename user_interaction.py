def get_input(prompt, quit_handler):
    """Helper function to get user input and check for 'q' to quit."""
    try:
        user_input = input(f"q to quit | {prompt}").strip()
    except (KeyboardInterrupt, EOFError):
        quit_handler()
    if user_input == 'q':
        quit_handler()
    return user_input


def quit_handler(client, thread):
    """Handles quitting the session."""
    client.delete_thread(thread.id)
    print("\nSession ended. Goodbye!")
    raise SystemExit


def collect_user_details(client, thread):
    """Function to collect niche details."""
    print("DETAILS", "-" * 23, end="\n")
    title = f"Title: {get_input('Please type in title: ', lambda: quit_handler(client, thread))}"
    description = f"Description: {get_input('Please type in description: ', lambda: quit_handler(client, thread))}"
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
        user_input_task = get_input("Please type in the task number: ", lambda: quit_handler(client, thread))
        if user_input_task in client.config["tasks"]:
            return user_input_task
        print("Invalid task number. Please try again.", end="\n")


def correct_responses(client, thread):
    """Function to allow user to correct responses."""
    while True:
        user_input = get_input("Would you like to make corrections to the response? (yes/no): ", lambda: quit_handler(client, thread))
        if user_input == 'yes':
            user_input = get_input("Please type in your corrections: ", lambda: quit_handler(client, thread))
            return user_input
        elif user_input == 'no':
            return False
        print("Invalid input. Please try again.")
