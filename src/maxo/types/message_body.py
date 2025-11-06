from maxo.omit import Omittable, Omitted
from maxo.types.attachments import Attachments, InlineKeyboardAttachment
from maxo.types.base import MaxoType
from maxo.types.keyboard import Keyboard
from maxo.types.markup_elements import MarkupElements


class MessageBody(MaxoType):
    """
    Схема, представляющая тело сообщения.

    Args:
        mid: Уникальный ID сообщения
        seq: ID последовательности сообщения в чате
        text: Новый текст сообщения
        attachments: Вложения сообщения. Могут быть одним из типов Attachment. Смотрите описание схемы
        markup: Разметка текста сообщения. Для подробной информации загляните в раздел Форматирование

    """

    mid: str
    seq: int
    text: str | None = None
    attachments: list[Attachments] | None = None
    markup: Omittable[list[MarkupElements] | None] = Omitted()

    @property
    def id(self) -> str:
        return self.mid

    @property
    def keyboard(self) -> Keyboard | None:
        if not self.attachments:
            return None
        for attachment in self.attachments:
            if isinstance(attachment, InlineKeyboardAttachment):
                return attachment.payload
        return None

    @property
    def reply_markup(self) -> Keyboard | None:
        return self.keyboard
