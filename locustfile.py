from locust import HttpUser, task, between

class StressTest(HttpUser):
    host = "https://siginv.uniguajira.edu.co"
    wait_time = between(0.1, 0.3)

    @task
    def hit_login(self):
        self.client.get("/", verify=False)

    @task(2)
    def hit_assets(self):
        self.client.get("/#/login", verify=False)
