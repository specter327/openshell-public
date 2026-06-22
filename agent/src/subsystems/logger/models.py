from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4


@dataclass
class LogEvent:

    id: str

    timestamp: datetime

    level: str

    source: str

    event: str

    payload: dict


    @staticmethod
    def create(
        source,
        event,
        payload=None,
        level="INFO"
    ):

        return LogEvent(
            id=str(uuid4()),
            timestamp=datetime.utcnow(),
            level=level,
            source=source,
            event=event,
            payload=payload or {}
        )