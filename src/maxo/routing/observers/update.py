from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar

from maxo.routing.ctx import Ctx
from maxo.routing.handlers.update import UpdateHandler, UpdateHandlerFn
from maxo.routing.interfaces.filter import Filter
from maxo.routing.observers.base import BaseObserver
from maxo.routing.updates.base import BaseUpdate
from maxo.routing.utils import inline_ctx as _inline_ctx

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)
_ReturnT_co = TypeVar("_ReturnT_co", covariant=True)


class UpdateObserver(
    BaseObserver[
        _UpdateT,
        UpdateHandler[_UpdateT, Any],
        UpdateHandlerFn[_UpdateT, Any],
    ],
    Generic[_UpdateT],
):
    def handler(
        self,
        handler_fn: UpdateHandlerFn[_UpdateT, Any],
        filter: Filter[_UpdateT] | None = None,
        inline_ctx: Callable | None = _inline_ctx,
    ) -> UpdateHandlerFn[_UpdateT, Any]:
        self._state.ensure_add_handler()

        if inline_ctx:
            handler_fn = inline_ctx(handler_fn)

        self._handlers.append(UpdateHandler(handler_fn, filter))

        return handler_fn

    if TYPE_CHECKING:

        async def execute_handler(
            self,
            ctx: Ctx[_UpdateT],
            handler: UpdateHandler[_UpdateT, _ReturnT_co],
        ) -> _ReturnT_co: ...
