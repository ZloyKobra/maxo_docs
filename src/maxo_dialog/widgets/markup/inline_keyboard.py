from maxo_dialog import DialogManager
from maxo_dialog.api.internal.widgets import (
    MarkupFactory,
    MarkupVariant,
    RawKeyboard,
)
from maxo_dialog.utils import add_intent_id


class InlineKeyboardFactory(MarkupFactory):
    async def render_markup(
        self,
        data: dict,
        manager: DialogManager,
        keyboard: RawKeyboard,
    ) -> MarkupVariant:
        # TODO validate buttons
        add_intent_id(keyboard, manager.current_context().id)
        return keyboard
