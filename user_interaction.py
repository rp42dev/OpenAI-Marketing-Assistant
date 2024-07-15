def get_input(prompt, quit_handler):
    """Helper function to get user input and check for 'q' to quit."""
    try:
        user_input = input(f"\nq to quit | {prompt}").strip()
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


def display_task_groups(task_groups: dict):
    """Function to display available task groups."""
    print("\nTASK GROUPS\n" + "-" * 23)
    for i, group_name in enumerate(task_groups.keys(), 1):
        print(f"{i}. {group_name}")
        

def select_task_group(task_groups: dict, client, thread):
    """Function to select a task group and validate the selection."""
    while True:
        user_input_group = get_input("Please type in the task group number: ", lambda: quit_handler(client, thread))
        if user_input_group.isdigit() and 1 <= int(user_input_group) <= len(task_groups):
            selected_group = list(task_groups.keys())[int(user_input_group) - 1]
            return selected_group
        print("Invalid task group number. Please try again.", end="\n")
        

def display_tasks(tasks: dict):
    """Function to display available tasks within a selected group."""
    print("\nTASKS\n" + "-" * 23)
    for task_key, task_details in tasks.items():
        print(f"{task_key}. {task_details['name']}")


def select_task(tasks: dict, client, thread):
    """Function to select a task and validate the selection."""
    while True:
        user_input_task = get_input(" | b to go back | Please type in the task number: ", lambda: quit_handler(client, thread))
        if user_input_task.lower() == 'b':
            return None
        if user_input_task in tasks:
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
