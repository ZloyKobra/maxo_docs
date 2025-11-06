from abc import abstractmethod
from typing import Protocol

from maxo import Ctx
from maxo.routing.interfaces import Router
from maxo_dialog.api.entities import ChatEvent
from maxo_dialog.api.protocols import (
    DialogManager,
    DialogRegistryProtocol,
)


class DialogManagerFactory(Protocol):
    @abstractmethod
    def __call__(
        self,
        event: ChatEvent,
        ctx: Ctx,
        registry: DialogRegistryProtocol,
        router: Router,
    ) -> DialogManager:
        raise NotImplementedError
