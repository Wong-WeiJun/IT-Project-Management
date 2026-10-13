from sqlalchemy.orm import Session

import models
from auth import current_username

DEFAULT_USER = "Admin"


def log_action(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: str,
    description: str,
    user: str | None = None,
) -> None:
    entry = models.AuditLog(
        user=user or current_username.get() or DEFAULT_USER,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
    )
    db.add(entry)
    db.commit()
