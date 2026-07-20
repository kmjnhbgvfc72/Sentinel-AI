from threat_response.executor import ResponseExecutor

def disable_account(db, account: str, actor: str, approved: bool = False):
    return ResponseExecutor().execute(db, "disable_account", account, actor, approved)

