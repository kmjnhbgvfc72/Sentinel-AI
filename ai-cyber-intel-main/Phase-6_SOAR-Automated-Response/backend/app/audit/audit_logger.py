from models import AuditLog


def log(session, actor, action, resource, details=""):
    session.add(
        AuditLog(actor=actor, action=action, resource=resource, details=details)
    )
    session.commit()
