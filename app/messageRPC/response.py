"""Response"""
from typing import Optional, Dict, List
from enum import Enum


class State(Enum):
    INVALID = "invalid"
    VALID = "valid"


class Response:
    status: State
    error: Optional[str]
    properties: Dict[str, any]

    def __init__(self, message: dict):
        self.status = State[message["state"]]
        self.error = None
        self.properties = {}

        if self.status == State.INVALID:
            self.error = message["error"]
        for key, value in message.items():
            if key not in ['error', 'state']:
                self.properties[key] = value

    def __repr__(self):
        return f"Response(status: {self.status!r}, error:{self.error!r}, properties:{self.properties!r})"
