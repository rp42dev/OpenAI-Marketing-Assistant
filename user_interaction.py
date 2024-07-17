class UserInteraction:
    """
    Class to handle user interaction with the OpenAI API.
    Methods: get_input, quit_handler, collect_user_details, display_options, select_option, correct_responses, process_message, process_task
    """
    def __init__(self, client, thread):
        self.client = client
        self.thread = thread

    def get_input(self, prompt: str, back_option=False):
        """Helper function to get user input and check for 'q' to quit."""
        try:
            user_input = input(f'\n"q" to quit' + (f' | "b" to go back' if back_option else '') + f' | {prompt}: ')
        except (KeyboardInterrupt, EOFError):
            self.quit_handler()
        if user_input == 'q':
            self.quit_handler()
        elif back_option and user_input.lower() == 'b':
            return None
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
        title = f"Title: {self.get_input('Title: (Name of your niche)')}"
        description = f"Description: {self.get_input('Description: (Describe your niche)')}"
        return f"{title}\n{description}"

    def display_options(self, options: dict, title: str):
        """Function to display available options with a given title."""
        print(f"\n{title}\n" + "-" * len(title))
        for i, option_key in enumerate(options.items(), 1):
            name = option_key[0]
            print(f"{i}. {name}")

    def select_option(self, options: dict, prompt: str, back_option=False):
        """Function to select an option and validate the selection."""
        while True:
            user_input = self.get_input(prompt, back_option)
            if user_input is None:  # Handle 'b' for back option
                return None
            if user_input.isdigit() and 1 <= int(user_input) <= len(options):
                selected_option = list(options.keys())[int(user_input) - 1]
                return selected_option
            print("Invalid selection. Please try again.", end="\n")

    def correct_responses(self, back_option=False):
        """Function to allow user to correct responses."""
        while True:
            user_input = self.get_input('Would you like to make corrections to the response? (yes/no)')
            if user_input.lower() == 'yes':
                corrected_input = self.get_input('Type in the correction that you would like to make', back_option)
                if corrected_input is None:  # Handle 'b' for back option
                    continue
                return corrected_input
            elif user_input.lower() == 'no':
                return None
            print("Invalid input. Please try again.")
