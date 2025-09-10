from uuid import uuid4


def unique(prefix: str = "x") -> str:
    return f"{prefix}-{uuid4().hex[:8]}"
