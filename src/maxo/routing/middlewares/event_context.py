from typing import Any

from maxo.routing.ctx import Ctx
from maxo.routing.interfaces.middleware import BaseMiddleware, NextMiddleware
from maxo.routing.signals.update import Update
from maxo.types import User

# TODO: Объединить с UpdateContextMiddleware

EVENT_FROM_USER_KEY = "event_from_user"


class EventContextMiddleware(BaseMiddleware[Update[Any]]):
    async def __call__(
        self,
        update: Update[Any],
        ctx: Ctx,
        next: NextMiddleware[Update[Any]],
    ) -> Any:
        user = self._resolve_event_context(update.update)
        if user:
            ctx[EVENT_FROM_USER_KEY] = user
        return await next(ctx)

    def _resolve_event_context(
        self,
        update: Any,
    ) -> User | None:
        if hasattr(update, "callback"):
            return update.callback.user
        if hasattr(update, "message"):
            return update.message.sender
        # TODO: Остальные ивенты
        return None
