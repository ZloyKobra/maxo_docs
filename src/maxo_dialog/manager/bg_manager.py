from datetime import datetime
from logging import getLogger
from typing import Any, Optional

from maxo import Bot, Dispatcher
from maxo.enums import ChatStatusType, ChatType
from maxo.fsm import State
from maxo.routing.interfaces import Router
from maxo.types import User
from maxo_dialog.api.entities import (
    DEFAULT_STACK_ID,
    AccessSettings,
    Data,
    DialogAction,
    DialogStartEvent,
    DialogSwitchEvent,
    DialogUpdate,
    DialogUpdateEvent,
    EventContext,
    ShowMode,
    StartMode,
)
from maxo_dialog.api.internal import (
    FakeRecipient,
    FakeUser,
)
from maxo_dialog.api.protocols import (
    BaseDialogManager,
    BgManagerFactory,
)
from maxo_dialog.manager.updater import Updater
from maxo_dialog.utils import is_user_loaded

logger = getLogger(__name__)


class BgManager(BaseDialogManager):
    def __init__(
        self,
        user: User,
        chat_id: int | None,
        bot: Bot,
        dp: Dispatcher,
        intent_id: Optional[str],
        stack_id: Optional[str],
        load: bool = False,
    ) -> None:
        self._event_context = EventContext(
            chat_id=chat_id,
            user_id=user.id,
            chat_type=ChatType.DIALOG,  # FIXME
            user=user,
            chat=None,
            bot=bot,
        )
        self._router = dp
        self._updater = Updater(dp)
        self.intent_id = intent_id
        self.stack_id = stack_id
        self.load = load

    def _get_fake_user(self, user_id: Optional[int] = None) -> User:
        if user_id is None or user_id == self._event_context.user.id:
            return self._event_context.user
        return FakeUser(
            user_id=user_id,
            is_bot=False,
            first_name="",
            last_activity_time=datetime.now(),
        )

    def bg(
        self,
        user_id: Optional[int] = None,
        chat_id: Optional[int] = None,
        stack_id: Optional[str] = None,
        load: bool = False,
    ) -> "BaseDialogManager":
        user = self._get_fake_user(user_id)

        new_event_context = EventContext(
            bot=self._event_context.bot,
            user=user,
            chat_id=chat_id,
            user_id=user_id,
            chat_type=ChatType.DIALOG,  # FIXME
            chat=None,
        )
        if stack_id is None:
            if self._event_context == new_event_context:
                stack_id = self.stack_id
                intent_id = self.intent_id
            else:
                stack_id = DEFAULT_STACK_ID
                intent_id = None
        else:
            intent_id = None

        return BgManager(
            user=new_event_context.user,
            chat_id=new_event_context.update_context.chat_id,
            bot=new_event_context.bot,
            dp=self._router,
            intent_id=intent_id,
            stack_id=stack_id,
            load=load,
        )

    def _base_event_params(self) -> dict[str, Any]:
        return {
            "from_user": self._event_context.user,
            "chat": self._event_context.chat,
            "intent_id": self.intent_id,
            "stack_id": self.stack_id,
        }

    async def _notify(self, event: DialogUpdateEvent) -> None:
        bot = self._event_context.bot
        event.bot = bot  # TODO: ???
        update = DialogUpdate(aiogd_update=event)
        await self._updater.notify(bot=bot, update=update)

    async def _load(self) -> None:
        if self.load:
            bot = self._event_context.bot
            if not is_user_loaded(self._event_context.user):
                logger.debug(
                    "load user %s from chat %s",
                    self._event_context.user_id,
                    self._event_context.chat_id,
                )
                chat_member = await bot.get_chat_member(
                    self._event_context.chat_id,
                    self._event_context.user.id,
                )
                self._event_context.user = chat_member

    async def done(
        self,
        result: Any = None,
        show_mode: Optional[ShowMode] = None,
    ) -> None:
        await self._load()
        await self._notify(
            DialogUpdateEvent(
                action=DialogAction.DONE,
                data=result,
                show_mode=show_mode,
                **self._base_event_params(),
            ),
        )

    async def start(
        self,
        state: State,
        data: Data = None,
        mode: StartMode = StartMode.NORMAL,
        show_mode: Optional[ShowMode] = None,
        access_settings: Optional[AccessSettings] = None,
    ) -> None:
        await self._load()
        await self._notify(
            DialogStartEvent(
                action=DialogAction.START,
                data=data,
                new_state=state,
                mode=mode,
                show_mode=show_mode,
                access_settings=access_settings,
                **self._base_event_params(),
            ),
        )

    async def switch_to(
        self,
        state: State,
        show_mode: Optional[ShowMode] = None,
    ) -> None:
        await self._load()
        await self._notify(
            DialogSwitchEvent(
                action=DialogAction.SWITCH,
                data={},
                new_state=state,
                show_mode=show_mode,
                **self._base_event_params(),
            ),
        )

    async def update(
        self,
        data: dict,
        show_mode: Optional[ShowMode] = None,
    ) -> None:
        await self._load()
        await self._notify(
            DialogUpdateEvent(
                action=DialogAction.UPDATE,
                data=data,
                show_mode=show_mode,
                **self._base_event_params(),
            ),
        )


class BgManagerFactoryImpl(BgManagerFactory):
    def __init__(self, router: Router):
        self._router = router

    def bg(
        self,
        bot: Bot,
        user_id: int,
        chat_id: int,
        stack_id: Optional[str] = None,
        load: bool = False,
    ) -> "BaseDialogManager":
        chat = FakeRecipient(
            chat_id=chat_id,
            type="",
            is_public=False,
            last_event_time=datetime.now(),
            participants_count=1,
            status=ChatStatusType.ACTIVE,
        )
        user = FakeUser(
            user_id=user_id,
            is_bot=False,
            first_name="",
            last_activity_time=datetime.now(),
        )
        if stack_id is None:
            stack_id = DEFAULT_STACK_ID

        return BgManager(
            user=user,
            chat=chat,
            bot=bot,
            router=self._router,
            intent_id=None,
            stack_id=stack_id,
            load=load,
        )
