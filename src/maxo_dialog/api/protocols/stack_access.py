from abc import abstractmethod
from typing import Optional, Protocol

from maxo import Ctx
from maxo_dialog import ChatEvent
from maxo_dialog.api.entities import Context, Stack


class StackAccessValidator(Protocol):
    @abstractmethod
    async def is_allowed(
        self,
        stack: Stack,
        context: Optional[Context],
        event: ChatEvent,
        ctx: Ctx,
    ) -> bool:
        """Check if current user is allowed to interactor with dialog."""
        raise NotImplementedError
