from locust import HttpUser, task, between

class StressTest(HttpUser):
    host = "https://siginv.uniguajira.edu.co"
    wait_time = between(0.1, 0.5)

    @task
    def hit_login(self):
        self.client.get("/#/login", verify=False)

    @task(3)
    def hit_api(self):
        self.client.get("/", verify=False)
