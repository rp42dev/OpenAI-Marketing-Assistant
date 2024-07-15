def get_input(prompt, quit_handler):
    """Helper function to get user input and check for 'q' to quit."""
    try:
        user_input = input(f'\n"q" to quit | {prompt} ').strip()
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
    print("\nDETAILS (Please provide the following details)")
    print("-" * 45)
    title = f"Title: {get_input('Title: (Name of your niche) ', lambda: quit_handler(client, thread))}"
    description = f"Description: {get_input('Description: (Describe your niche) ', lambda: quit_handler(client, thread))}"
    return f"{title}\n{description}"


def display_options(options: dict, title: str, is_task_group: bool):
    """Function to display available options with a given title."""
    print(f"\n{title}\n" + "-" * len(title))
    for i, (option_key, option_details) in enumerate(options.items(), 1):
        name = option_key if is_task_group else option_details['name']
        print(f"{i}. {name}")


def select_option(options: dict, prompt: str, quit_handler, back_option=False):
    """Function to select an option and validate the selection."""
    while True:
        user_input = get_input(('"b" to go back | ' if back_option else "") + prompt, quit_handler)
        if back_option and user_input.lower() == 'b':
            return None
        if user_input.isdigit() and 1 <= int(user_input) <= len(options):
            selected_option = list(options.keys())[int(user_input) - 1]
            return selected_option
        print("Invalid selection. Please try again.", end="\n")


def correct_responses(client, thread):
    """Function to allow user to correct responses."""
    while True:
        user_input = get_input("Would you like to make corrections to the response? (yes/no): ", lambda: quit_handler(client, thread))
        if user_input.lower() in ['yes', 'no']:
            if user_input.lower() == 'yes':
                corrected_input = get_input('"b" to go back | Please type in the corrected response: ', lambda: quit_handler(client, thread))
                if corrected_input.lower() == 'b':
                    return None
                return corrected_input
            return False
        print("Invalid input. Please try again.")

