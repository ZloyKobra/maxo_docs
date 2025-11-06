import logging
import os
from time import time
from typing import Any

from maxo import Bot, Ctx, Dispatcher, SimpleRouter
from maxo.fsm import State, StatesGroup
from maxo.fsm.key_builder import DefaultKeyBuilder
from maxo.fsm.storages.memory import MemoryStorage, SimpleEventIsolation
from maxo.routing.updates import MessageCreated
from maxo.tools.long_polling import LongPolling
from maxo_dialog import (
    Dialog,
    DialogManager,
    ShowMode,
    StartMode,
    Window,
    setup_dialogs,
)
from maxo_dialog.widgets.kbd import Back, Next, SwitchTo
from maxo_dialog.widgets.text import Const, Format, Multi


class StartSG(StatesGroup):
    first = State()
    second = State()
    third = State()


async def get_username(**__: Any) -> dict[str, Any]:
    return {"username": "друг"}


async def get_phone(**__: Any) -> dict[str, Any]:
    return {"phone": "+78005553535"}


start_dialog = Dialog(
    Window(
        Multi(Const("Привет,"), Format("{username} {phone}!"), sep=" "),
        Const("Как твои дела?"),
        SwitchTo(Const("Вперёд первый"), id="next", state=StartSG.second),
        Next(Const("Вперёд второй")),
        getter=[get_username, get_phone],
        state=StartSG.first,
    ),
    Window(
        Const("Второе окно"),
        Format("{phone}"),
        SwitchTo(Const("Назад первый"), id="back", state=StartSG.first),
        Back(Const("Назад второй")),
        getter=get_phone,
        state=StartSG.second,
    ),
)


start_router = SimpleRouter(name=__name__)


@start_router.message_created()
async def start(
    message: MessageCreated,
    ctx: Ctx,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=StartSG.first,
        show_mode=ShowMode.SEND,
        mode=StartMode.RESET_STACK,
        data={"time": time()},
    )


def main() -> None:
    bot = Bot(os.environ["TOKEN"])

    key_builder = DefaultKeyBuilder(with_destiny=True)
    storage = MemoryStorage(key_builder=key_builder)
    event_isolation = SimpleEventIsolation(key_builder=key_builder)

    dispatcher = Dispatcher(
        storage=storage,
        event_isolation=event_isolation,
        key_builder=key_builder,
    )

    dispatcher.include(start_router, start_dialog)
    setup_dialogs(dispatcher, events_isolation=event_isolation)

    LongPolling(dispatcher).run(bot)


logging.basicConfig(level=logging.DEBUG)
main()
