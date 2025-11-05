from collections.abc import Callable
from typing import Optional, Union

from maxo.types import CallbackKeyboardButton, MessageKeyboardButton
from maxo_dialog.api.internal import RawKeyboard
from maxo_dialog.api.protocols import DialogManager
from maxo_dialog.widgets.text import Text

from .base import Keyboard


class RequestContact(Keyboard):
    def __init__(
        self,
        text: Text,
        when: Union[str, Callable, None] = None,
    ):
        super().__init__(when=when)
        self.text = text

    async def _render_keyboard(
        self,
        data: dict,
        manager: DialogManager,
    ) -> RawKeyboard:
        return [
            [
                MessageKeyboardButton(
                    text=await self.text.render_text(data, manager),
                    request_contact=True,
                ),
            ],
        ]


class RequestLocation(Keyboard):
    def __init__(
        self,
        text: Text,
        when: Union[str, Callable, None] = None,
    ):
        super().__init__(when=when)
        self.text = text

    async def _render_keyboard(
        self,
        data: dict,
        manager: DialogManager,
    ) -> RawKeyboard:
        return [
            [
                MessageKeyboardButton(
                    text=await self.text.render_text(data, manager),
                    request_location=True,
                ),
            ],
        ]


class RequestPoll(Keyboard):
    def __init__(
        self,
        text: Text,
        poll_type: Optional[str] = None,
        when: Union[str, Callable, None] = None,
    ):
        super().__init__(when=when)
        self.text = text
        self.poll_type = poll_type

    async def _render_keyboard(
        self,
        data: dict,
        manager: DialogManager,
    ) -> RawKeyboard:
        text = await self.text.render_text(data, manager)
        request_poll = CallbackKeyboardButton(type=self.poll_type)

        return [
            [
                MessageKeyboardButton(
                    text=text,
                    request_poll=request_poll,
                ),
            ],
        ]
