from abc import abstractmethod
from collections.abc import Awaitable, Callable, Sequence
from typing import Any, Optional, Union

from magic_filter import F

from maxo.enums import AttachmentType
from maxo.integrations.magic_filter import MagicFilter
from maxo.types import Message
from maxo_dialog.api.internal import InputWidget
from maxo_dialog.api.protocols import (
    DialogManager,
    DialogProtocol,
)
from maxo_dialog.tools.filter_object import FilterObject
from maxo_dialog.widgets.common import Actionable
from maxo_dialog.widgets.widget_event import (
    WidgetEventProcessor,
    ensure_event_processor,
)

MessageHandlerFunc = Callable[
    [Message, "MessageInput", DialogManager],
    Awaitable,
]


class BaseInput(Actionable, InputWidget):
    @abstractmethod
    async def process_message(
        self,
        message: Message,
        dialog: DialogProtocol,
        manager: DialogManager,
    ) -> bool:
        raise NotImplementedError


class MessageInput(BaseInput):
    def __init__(
        self,
        func: Union[MessageHandlerFunc, WidgetEventProcessor, None],
        content_types: Union[Sequence[str], str] = AttachmentType.ANY,
        filter: Optional[Callable[..., Any]] = None,
        id: Optional[str] = None,
    ):
        super().__init__(id=id)
        self.func = ensure_event_processor(func)

        filters = []
        if isinstance(content_types, str):
            if content_types != AttachmentType.ANY:
                filters.append(
                    FilterObject(MagicFilter(F.content_type == content_types))
                )
        elif AttachmentType.ANY not in content_types:
            filters.append(FilterObject(MagicFilter(F.content_type.in_(content_types))))
        if filter is not None:
            filters.append(FilterObject(filter))
        self.filters = filters

    async def process_message(
        self,
        message: Message,
        dialog: DialogProtocol,
        manager: DialogManager,
    ) -> bool:
        for handler_filter in self.filters:
            if not await handler_filter.call(
                manager.event,
                **manager.middleware_data,
            ):
                return False
        await self.func.process_event(message, self, manager)
        return True
