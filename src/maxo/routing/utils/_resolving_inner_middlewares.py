from collections import defaultdict
from typing import Any, MutableMapping, MutableSequence, overload

from maxo.routing.interfaces.middleware import BaseMiddleware
from maxo.routing.interfaces.router import Router
from maxo.routing.updates.base import BaseUpdate


def resolve_middlewares(
    router: Router,
    middlewares_map: MutableMapping[
        type[BaseUpdate], MutableSequence[BaseMiddleware[Any]]
    ],
) -> None:
    for update_tp, observer in router.observers.items():
        new_middlewares = (*middlewares_map[update_tp],)
        current_middlewares = (*observer.middleware.inner._middlewares,)

        observer.middleware.inner._middlewares.extend(new_middlewares)
        middlewares_map[update_tp].extend(current_middlewares)


@overload
def resolving_inner_middlewares(
    router: Router,
) -> None: ...


@overload
def resolving_inner_middlewares(
    router: Router,
    middlewares_map: MutableMapping[
        type[BaseUpdate], MutableSequence[BaseMiddleware[Any]]
    ],
) -> None: ...


def resolving_inner_middlewares(
    router: Router,
    middlewares_map: (
        MutableMapping[type[BaseUpdate], MutableSequence[BaseMiddleware[Any]]] | None
    ) = None,
) -> None:
    if middlewares_map is None:
        middlewares_map = defaultdict(list)

    resolve_middlewares(router, middlewares_map)

    for children_router in router.children_routers:
        resolving_inner_middlewares(children_router, middlewares_map)
