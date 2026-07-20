from threat_response.executor import ResponseExecutor

def block_ip(db, ip_address: str, actor: str, approved: bool = False):
    return ResponseExecutor().execute(db, "block_ip", ip_address, actor, approved)

