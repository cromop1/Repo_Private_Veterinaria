from __future__ import annotations

from typing import Iterable, List, Mapping

from django import template

register = template.Library()


AppDict = Mapping[str, object]
ModelDict = Mapping[str, object]


def _iter_models(app_list: Iterable[AppDict]) -> Iterable[ModelDict]:
    for app in app_list:
        models = app.get("models") if isinstance(app, Mapping) else None
        if not models:
            continue
        for model in models:
            if isinstance(model, Mapping):
                yield model


@register.simple_tag
def admin_model_count(app_list: Iterable[AppDict]) -> int:
    """Return the total number of models displayed on the admin index."""
    return sum(1 for _ in _iter_models(app_list))


@register.simple_tag
def admin_quick_actions(app_list: Iterable[AppDict], limit: int | None = None) -> List[dict]:
    """Build a list of quick actions with available ``add`` URLs."""
    actions: List[dict] = []
    for model in _iter_models(app_list):
        add_url = model.get("add_url")
        name = model.get("name")
        if not add_url or not name:
            continue
        actions.append({"name": name, "url": add_url})
        if limit is not None and len(actions) >= limit:
            break
    return actions
