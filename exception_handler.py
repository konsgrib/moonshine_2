import RPi.GPIO as GPIO


class ExceptionHandler:
    def __init__(self, cmd, error) -> None:
        self.cmd = cmd
        self.error = error
        self.failed_class_name = self._get_cmd_class_name()
        self.exception_name = str(self.error.__class__.__name__)
        self._exceptions = {
            "device": {
                "ValueError": print(self.error),
            },
            "cmd": {
                "ValueError": print(self.error),
            },
            "event": {
                "ValueError": print(self.error),
            },
        }

    def _get_cmd_class_name(self):
        keys = list(self.cmd.__dict__.keys())
        klass_name = keys[0]
        return klass_name

    def handle(self):
        class_exceptions = self._exceptions.get(self.failed_class_name)
        print("ERROR", self.error)
        if not class_exceptions:
            print(f"Class {self.failed_class_name} not found in exceptions dictionary")
            return

        exception_handler = class_exceptions.get(self.exception_name)
        if not exception_handler:
            print(f"{self.exception_name}: Exception not found in dictionary for event")
            return
        exec(exception_handler)

    def add_handler(self, event_name: str, exception: str, handler: str):
        class_exceptions = self._exceptions.get(event_name)
        if not class_exceptions:
            print("Creating exception")
            self._exceptions[event_name] = {}
            self._exceptions[event_name][exception] = handler
        else:
            print("Updatinging exception")
            self._exceptions[event_name][exception] = handler

    def show_config(self):
        print(self._exceptions)
