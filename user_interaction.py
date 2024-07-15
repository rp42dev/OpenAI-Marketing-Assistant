class UserInteraction:
    """Class to handle user interaction with the OpenAI API."""
    def __init__(self, client, thread):
        self.client = client
        self.thread = thread

    def get_input(self, prompt):
        """Helper function to get user input and check for 'q' to quit."""
        try:
            user_input = input(f'\n"q" to quit | {prompt} ').strip()
        except (KeyboardInterrupt, EOFError):
            self.quit_handler()
        if user_input == 'q':
            self.quit_handler()
        return user_input

    def quit_handler(self):
        """Handles quitting the session."""
        self.client.delete_thread(self.thread.id)
        print("\nSession ended. Goodbye!")
        raise SystemExit

    def collect_user_details(self):
        """Function to collect niche details."""
        print("\nDETAILS (Please provide the following details)")
        print("-" * 45)
        title = f"Title: {self.get_input('Title: (Name of your niche) ')}"
        description = f"Description: {self.get_input('Description: (Describe your niche) ')}"
        return f"{title}\n{description}"

    def display_options(self, options: dict, title: str, is_task_group: bool):
        """Function to display available options with a given title."""
        print(f"\n{title}\n" + "-" * len(title))
        for i, (option_key, option_details) in enumerate(options.items(), 1):
            name = option_key if is_task_group else option_details['name']
            print(f"{i}. {name}")

    def select_option(self, options: dict, prompt: str, back_option=False):
        """Function to select an option and validate the selection."""
        while True:
            user_input = self.get_input(('"b" to go back | ' if back_option else "") + prompt)
            if back_option and user_input.lower() == 'b':
                return None
            if user_input.isdigit() and 1 <= int(user_input) <= len(options):
                selected_option = list(options.keys())[int(user_input) - 1]
                return selected_option
            print("Invalid selection. Please try again.", end="\n")

    def correct_responses(self):
        """Function to allow user to correct responses."""
        while True:
            user_input = self.get_input("Would you like to make corrections to the response? (yes/no): ")
            if user_input.lower() in ['yes', 'no']:
                if user_input.lower() == 'yes':
                    corrected_input = self.get_input('"b" to go back | Please type in the corrected response: ')
                    if corrected_input.lower() == 'b':
                        return None
                    return corrected_input
                return False
            print("Invalid input. Please try again.")
