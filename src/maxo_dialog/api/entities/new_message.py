from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence, Union

from maxo.enums import TextFormat
from maxo.types import (
    InlineKeyboardAttachmentRequest,
    NewMessageLink,
    Recipient,
)
from maxo.types.attachments import Attachments
from maxo.types.keyboard_buttons import KeyboardButtons
from maxo.types.request_attachments import AttachmentsRequests
from maxo_dialog.api.entities import ShowMode
from maxo_dialog.api.entities.link_preview import LinkPreviewOptions

MarkupVariant = list[list[KeyboardButtons]]


class UnknownText(Enum):
    UNKNOWN = object()


@dataclass
class OldMessage:
    recipient: Recipient
    message_id: str
    sequence_id: int
    text: Union[str, None, UnknownText]
    attachments: list[Attachments]


@dataclass
class NewMessage:
    recipient: Recipient
    attachments: list[AttachmentsRequests]
    parse_mode: Optional[TextFormat] = None
    link_preview_options: Optional[LinkPreviewOptions] = None
    show_mode: ShowMode = ShowMode.AUTO
    text: Optional[str] = None
    link_to: Optional[NewMessageLink] = None

    @property
    def keyboard(self) -> Sequence[Sequence[KeyboardButtons]]:
        if not self.attachments:
            return None
        for attachment in self.attachments:
            if isinstance(attachment, InlineKeyboardAttachmentRequest):
                return attachment.payload.buttons
        return []
