from maxo import Ctx
from maxo.routing.interfaces import Router
from maxo_dialog.api.entities import ChatEvent
from maxo_dialog.api.internal import DialogManagerFactory
from maxo_dialog.api.protocols import (
    DialogManager,
    DialogRegistryProtocol,
    MediaIdStorageProtocol,
    MessageManagerProtocol,
)

from .manager import ManagerImpl


class DefaultManagerFactory(DialogManagerFactory):
    def __init__(
        self,
        message_manager: MessageManagerProtocol,
        media_id_storage: MediaIdStorageProtocol,
    ) -> None:
        self.message_manager = message_manager
        self.media_id_storage = media_id_storage

    def __call__(
        self,
        event: ChatEvent,
        ctx: Ctx,
        registry: DialogRegistryProtocol,
        router: Router,
    ) -> DialogManager:
        return ManagerImpl(
            event=event,
            ctx=ctx,
            message_manager=self.message_manager,
            media_id_storage=self.media_id_storage,
            registry=registry,
            router=router,
        )
