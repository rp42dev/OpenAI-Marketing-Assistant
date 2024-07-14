from typing_extensions import override
from openai import AssistantEventHandler
 
 
class EventHandler(AssistantEventHandler):
    """EventHandler class to handle the events in the response stream."""
    @override
    def on_text_created(self, text) -> None:
        """Function to handle the text created event."""
        print(f"\nASSISTANT:", end="\n", flush=True)
        
    @override
    def on_text_delta(self, delta, snapshot):
        """Function to handle the text delta event."""
        print(delta.value, end="", flush=True)
        
    @override
    def on_message_done(self, message):
        """Function to handle the message done event."""
        print(f"\nMessage done: {message.id}", end="\n", flush=True)
