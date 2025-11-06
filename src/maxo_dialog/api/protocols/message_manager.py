from abc import abstractmethod
from typing import Optional, Protocol

from maxo import Bot
from maxo.routing.updates import MessageEdited
from maxo.types import Callback
from maxo_dialog import ShowMode
from maxo_dialog.api.entities import NewMessage, OldMessage
from maxo_dialog.api.exceptions import DialogsError


class MessageNotModified(DialogsError):
    pass


class MessageManagerProtocol(Protocol):
    @abstractmethod
    async def remove_kbd(
        self,
        bot: Bot,
        show_mode: ShowMode,
        old_message: Optional[OldMessage],
    ) -> Optional[MessageEdited]:
        raise NotImplementedError

    @abstractmethod
    async def show_message(
        self,
        bot: Bot,
        new_message: NewMessage,
        old_message: Optional[OldMessage],
    ) -> OldMessage:
        raise NotImplementedError

    @abstractmethod
    async def answer_callback(
        self,
        bot: Bot,
        callback: Callback,
    ) -> None:
        raise NotImplementedError
