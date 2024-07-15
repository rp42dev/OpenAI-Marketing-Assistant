class MessageProcessor:
    def __init__(self, client, thread):
        self.client = client
        self.thread = thread

    def process_message(self, user_input):
        """Method to process the message."""
        self.client.create_message(self.thread.id, user_input, "user")

    def process_task(self, group, stage, user_input):
        """Method to process the selected task."""
        task_name = self.client.config[group][stage][user_input]['name']
        task_instructions = self.client.config[group][stage][user_input]['instructions']
        print(f"\nProcessing task: {task_name}")

        self.client.stream_run(self.thread.id, self.client.get_assistant().id, task_instructions)
