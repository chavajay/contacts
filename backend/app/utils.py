from typing import Iterable, Dict, Any

def diff_fields(original: Dict[str, Any], updated: Dict[str, Any], fields: Iterable[str]):
    changes = []
    for f in fields:
        old = original.get(f)
        new = updated.get(f)
        if new is not None and new != old:
            changes.append((f, old, new))
    return changes
