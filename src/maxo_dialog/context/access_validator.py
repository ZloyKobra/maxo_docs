from logging import getLogger
from typing import Optional

from maxo.routing.ctx import Ctx
from maxo.routing.middlewares.event_context import EVENT_FROM_USER_KEY
from maxo.types import User
from maxo_dialog import ChatEvent
from maxo_dialog.api.entities import (
    Context,
    Stack,
)
from maxo_dialog.api.protocols import StackAccessValidator

logger = getLogger(__name__)


class DefaultAccessValidator(StackAccessValidator):
    async def is_allowed(
        self,
        stack: Stack,
        context: Optional[Context],
        event: ChatEvent,
        ctx: Ctx,
    ) -> bool:
        if context:
            access_settings = context.access_settings
        else:
            access_settings = stack.access_settings

        # if everything is disabled, it is allowed
        if access_settings is None:
            return True
        if not (access_settings.user_ids or access_settings.custom):
            return True

        # check user
        user: User = getattr(ctx, EVENT_FROM_USER_KEY)
        if user.id in access_settings.user_ids:
            return True

        return False
