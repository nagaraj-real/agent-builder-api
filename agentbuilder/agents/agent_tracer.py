import re
from typing import Any
from langchain_core.tracers.stdout import FunctionCallbackHandler
from typing import Any


class PrintFileCallbackHandler(FunctionCallbackHandler):
    """Tracer that prints to the console."""

    name: str = "print_file_callback_handler"

    def remove_ansi_codes(self,text):
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)

    def print_to_file(self,msg:str):
        with open('trace.log', 'a') as f:
           msg = self.remove_ansi_codes(msg)
           print(msg, file=f)

    def __init__(self, **kwargs: Any) -> None:
        """Create a ConsoleCallbackHandler."""
        super().__init__(function=self.print_to_file, **kwargs)

