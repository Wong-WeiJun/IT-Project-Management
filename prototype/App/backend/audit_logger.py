from sqlalchemy.orm import Session

import models

DEFAULT_USER = "Admin"


def log_action(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: str,
    description: str,
    user: str = DEFAULT_USER,
) -> None:
    entry = models.AuditLog(
        user=user,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
    )
    db.add(entry)
    db.commit()
