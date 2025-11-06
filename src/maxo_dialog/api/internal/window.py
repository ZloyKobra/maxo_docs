from abc import abstractmethod
from typing import (
    Any,
    Protocol,
)

from maxo.fsm import State
from maxo.routing.updates import MessageCallback, MessageCreated
from maxo_dialog.api.entities import Data, NewMessage
from maxo_dialog.api.protocols import DialogProtocol

from .manager import DialogManager


class WindowProtocol(Protocol):
    @abstractmethod
    async def process_message(
        self,
        message: MessageCreated,
        dialog: "DialogProtocol",
        manager: DialogManager,
    ) -> bool:
        """Return True if message in handled."""
        raise NotImplementedError

    @abstractmethod
    async def process_callback(
        self,
        callback: MessageCallback,
        dialog: "DialogProtocol",
        manager: DialogManager,
    ) -> bool:
        """Return True if callback in handled."""
        raise NotImplementedError

    @abstractmethod
    async def process_result(
        self,
        start_data: Data,
        result: Any,
        manager: "DialogManager",
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def render(
        self,
        dialog: "DialogProtocol",
        manager: DialogManager,
    ) -> NewMessage:
        raise NotImplementedError

    @abstractmethod
    def get_state(self) -> State:
        raise NotImplementedError

    @abstractmethod
    def find(self, widget_id) -> Any:
        raise NotImplementedError
