"""Holds temp session info"""
from datetime import datetime
from typing import Optional


class Session:
    session_id: str
    session_expiry: datetime
    user_id: str
    oid: str
    subscription_id: Optional[str]

    def __init__(self, session_data: dict, session_id: str):
        self.session_id = session_id
        self.user_id = session_data.get("user_id")
        self.subscription_id = session_data.get("subscription_id")
        self.session_expiry: datetime = session_data.get("session_expiry")
        self.oid: datetime = session_data.get("oid")

