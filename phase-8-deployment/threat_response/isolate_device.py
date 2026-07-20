from threat_response.executor import ResponseExecutor

def isolate_device(db, device_id: str, actor: str, approved: bool = False):
    return ResponseExecutor().execute(db, "isolate_device", device_id, actor, approved)

