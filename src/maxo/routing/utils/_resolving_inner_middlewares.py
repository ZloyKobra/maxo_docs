from collections import defaultdict
from typing import Any, MutableMapping, MutableSequence, overload

from maxo.routing.interfaces.middleware import BaseMiddleware
from maxo.routing.interfaces.router import BaseRouter
from maxo.routing.updates.base import BaseUpdate

_INNER_MIDDLEWARES_KEY = "inner"
_OUTER_MIDDLEWARES_KEY = "outer"


def _resolving_middlewares(
    router: BaseRouter,
    middlewares_map: (
        MutableMapping[
            str, MutableMapping[type[BaseUpdate], MutableSequence[BaseMiddleware[Any]]]
        ]
        | None
    ) = None,
) -> None:
    for update_tp, observer in router.observers.items():
        new_inners = (*middlewares_map[_INNER_MIDDLEWARES_KEY][update_tp],)
        current_inners = (*observer.middleware.inner._middlewares,)

        observer.middleware.inner._middlewares.extend(new_inners)
        middlewares_map[_INNER_MIDDLEWARES_KEY][update_tp].extend(current_inners)

        new_outers = (*middlewares_map[_OUTER_MIDDLEWARES_KEY][update_tp],)
        current_outers = (*observer.middleware.outer._middlewares,)

        observer.middleware.outer._middlewares.extend(new_outers)
        middlewares_map[_OUTER_MIDDLEWARES_KEY][update_tp].extend(current_outers)


def _resolving_outer_middlewares(
    router: BaseRouter,
    middlewares_map: MutableMapping[
        type[BaseUpdate], MutableSequence[BaseMiddleware[Any]]
    ],
) -> None:
    for update_tp, observer in router.observers.items():
        new_middlewares = (*middlewares_map[update_tp],)
        current_middlewares = (*observer.middleware.outer._middlewares,)

        observer.middleware.outer._middlewares.extend(new_middlewares)
        middlewares_map[update_tp].extend(current_middlewares)


@overload
def resolve_middlewares(
    router: BaseRouter,
) -> None: ...


@overload
def resolve_middlewares(
    router: BaseRouter,
    middlewares_map: (
        MutableMapping[
            str, MutableMapping[type[BaseUpdate], MutableSequence[BaseMiddleware[Any]]]
        ]
        | None
    ) = None,
) -> None: ...


def resolve_middlewares(
    router: BaseRouter,
    middlewares_map: (
        MutableMapping[
            str, MutableMapping[type[BaseUpdate], MutableSequence[BaseMiddleware[Any]]]
        ]
        | None
    ) = None,
) -> None:
    if middlewares_map is None:
        middlewares_map = {
            _INNER_MIDDLEWARES_KEY: defaultdict(list),
            _OUTER_MIDDLEWARES_KEY: defaultdict(list),
        }

    _resolving_middlewares(router, middlewares_map)

    for children_router in router.children_routers:
        resolve_middlewares(children_router, {**middlewares_map})
