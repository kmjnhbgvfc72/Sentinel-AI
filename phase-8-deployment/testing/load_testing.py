from locust import HttpUser, between, task


class SOCUser(HttpUser):
    wait_time = between(.2, 1)
    token = ""
    def on_start(self):
        response = self.client.post("/api/v1/auth/token", data={"username": "admin", "password": "load-test-password"})
        self.token = response.json().get("access_token", "")
    @task(4)
    def threats(self): self.client.get("/api/v1/threats?limit=25", headers={"Authorization": f"Bearer {self.token}"})
    @task
    def prediction(self): self.client.post("/api/v1/predictions", json={"anomaly_score":.7,"asset_criticality":.9,"threat_confidence":.8,"exposure":.5}, headers={"Authorization": f"Bearer {self.token}"})

