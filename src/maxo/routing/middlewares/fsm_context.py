from typing import Any

from maxo.fsm.key_builder import StorageKey
from maxo.fsm.manager import FSMContext
from maxo.fsm.storages.base import BaseEventIsolation, BaseStorage
from maxo.routing.ctx import Ctx
from maxo.routing.interfaces.middleware import BaseMiddleware, NextMiddleware
from maxo.routing.signals.update import Update
from maxo.types.update_context import UpdateContext


class FSMContextMiddleware(BaseMiddleware[Update[Any]]):
    __slots__ = (
        "_event_isolation",
        "_storage",
    )

    def __init__(
        self,
        storage: BaseStorage,
        event_isolation: BaseEventIsolation,
    ) -> None:
        self._storage = storage
        self._event_isolation = event_isolation

    async def __call__(
        self,
        update: Update[Any],
        ctx: Ctx[Update[Any]],
        next: NextMiddleware[Update[Any]],
    ) -> Any:
        storage_key = self.make_storage_key(
            bot_id=ctx.bot.state.info.user_id,
            update_context=ctx.update_context,
        )
        if storage_key is None:
            return await next(ctx)

        async with self._event_isolation.lock(key=storage_key):
            fsm_context = FSMContext(
                key=storage_key,
                storage=self._storage,
            )
            ctx.storage = self._storage
            ctx.fsm_context = fsm_context
            ctx.fsm_storage = self._storage
            ctx.raw_state = await fsm_context.get_state()

            return await next(ctx)

    def make_storage_key(
        self,
        bot_id: int,
        update_context: UpdateContext,
    ) -> StorageKey | None:
        chat_id, user_id = update_context.chat_id, update_context.user_id
        if chat_id is None or user_id is None:
            return None

        return StorageKey(
            bot_id=bot_id,
            chat_id=chat_id,
            user_id=user_id,
        )
