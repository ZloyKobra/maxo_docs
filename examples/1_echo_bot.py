import logging
import os

from maxo import Bot, Dispatcher
from maxo.routing.ctx import Ctx
from maxo.routing.updates.message_created import MessageCreated
from maxo.tools.facades.updates.message_created import MessageCreatedFacade
from maxo.tools.long_polling.long_polling import LongPolling

bot = Bot(os.environ["TOKEN"])
dispatcher = Dispatcher()


@dispatcher.message_created()
async def echo_handler(
    update: MessageCreated,
    ctx: Ctx[MessageCreated],
    facade: MessageCreatedFacade,
) -> None:
    text = update.message.unsafe_body.text or "Текста нет"
    await facade.answer_text(text)


logging.basicConfig(level=logging.DEBUG)
LongPolling(dispatcher).run(bot)
