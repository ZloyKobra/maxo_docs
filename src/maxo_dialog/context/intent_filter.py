from typing import Optional

from maxo.fsm import StatesGroup
from maxo.routing.ctx import Ctx
from maxo.routing.filters import BaseFilter
from maxo.types import MaxoType
from maxo_dialog.api.entities import Context
from maxo_dialog.api.internal import CONTEXT_KEY


class IntentFilter(BaseFilter):
    def __init__(self, aiogd_intent_state_group: Optional[type[StatesGroup]]):
        self.aiogd_intent_state_group = aiogd_intent_state_group

    async def __call__(self, update: MaxoType, ctx: Ctx) -> bool:
        if self.aiogd_intent_state_group is None:
            return True

        context: Context = getattr(ctx, CONTEXT_KEY, None)
        if not context:
            return False
        return context.state.group == self.aiogd_intent_state_group
