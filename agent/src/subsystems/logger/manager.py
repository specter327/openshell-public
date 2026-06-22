from ..base import Subsystem
from .models import LogEvent


class LoggingManager(Subsystem):


    def __init__(self, core):

        super().__init__(core)

        self.handlers = []


    def register(
        self,
        handler
    ):
        self.handlers.append(handler)



    def emit(
        self,
        source,
        event,
        payload=None,
        level="INFO"
    ):

        log = LogEvent.create(
            source,
            event,
            payload,
            level
        )


        for handler in self.handlers:
            handler.write(log)


        self.events.publish(
            "LOG_EVENT",
            log
        )


        return log