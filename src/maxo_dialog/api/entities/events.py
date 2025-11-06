from dataclasses import dataclass
from typing import Any, Union

from maxo import Bot
from maxo.enums import ChatType
from maxo.routing.signals.exception import ExceptionEvent
from maxo.routing.updates import MessageCallback, MessageCreated, UserAdded, UserRemoved
from maxo.types import Chat, User

from .update_event import DialogUpdateEvent

ChatEvent = Union[
    MessageCallback,
    UserAdded,
    UserRemoved,
    DialogUpdateEvent,
    ExceptionEvent[Any],
    MessageCreated,
]


@dataclass
class EventContext:
    bot: Bot
    chat_id: int | None
    user_id: int | None
    chat_type: ChatType | None
    user: User | None
    chat: Chat | None


EVENT_CONTEXT_KEY = "aiogd_event_context"
