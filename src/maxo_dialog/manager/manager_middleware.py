from typing import Any

from maxo.routing.ctx import Ctx
from maxo.routing.interfaces import BaseMiddleware, NextMiddleware, Router
from maxo.routing.updates.base import MaxUpdate
from maxo_dialog.api.internal import STORAGE_KEY, DialogManagerFactory
from maxo_dialog.api.protocols import (
    BgManagerFactory,
    DialogManager,
    DialogRegistryProtocol,
)

MANAGER_KEY = "dialog_manager"
BG_FACTORY_KEY = "dialog_bg_factory"


class ManagerMiddleware(BaseMiddleware[MaxUpdate]):
    def __init__(
        self,
        dialog_manager_factory: DialogManagerFactory,
        registry: DialogRegistryProtocol,
        router: Router,
    ) -> None:
        super().__init__()
        self.dialog_manager_factory = dialog_manager_factory
        self.registry = registry
        self.router = router

    async def __call__(
        self,
        update: MaxUpdate,
        ctx: Ctx,
        next: NextMiddleware,
    ) -> Any:
        if self._is_event_supported(ctx):
            dialog_manager = self.dialog_manager_factory(
                event=update,
                ctx=ctx,
                registry=self.registry,
                router=self.router,
            )
            setattr(ctx, MANAGER_KEY, dialog_manager)

        try:
            return await next(ctx)
        finally:
            manager: DialogManager | None = getattr(ctx, MANAGER_KEY, None)
            if manager:
                await manager.close_manager()

    def _is_event_supported(
        self,
        ctx: Ctx,
    ) -> bool:
        return hasattr(ctx, STORAGE_KEY)


class BgFactoryMiddleware(BaseMiddleware[MaxUpdate]):
    def __init__(
        self,
        bg_manager_factory: BgManagerFactory,
    ) -> None:
        super().__init__()
        self.bg_manager_factory = bg_manager_factory

    async def __call__(
        self,
        update: MaxUpdate,
        ctx: Ctx,
        next: NextMiddleware,
    ) -> Any:
        setattr(ctx, BG_FACTORY_KEY, self.bg_manager_factory)
        return await next(ctx)
