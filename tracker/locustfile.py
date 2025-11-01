from locust import HttpUser,task,between
import random

class User(HttpUser):
    wait_time = between(1,3)

    def on_start(self):
        response = self.client.post(
            "/login/",
            data={"username": "testuser","password":"testpass"}
        )
        if response.status_code==200:
            token = response.json()["access_token"]
            self.headers = {"Authorization":f"Bearer {token}"}
        else:
            self.headers = {}

    @task(2)
    def get_users(self):
        self.client.get("/users/",headers=self.headers)

    @task(1)
    def create_expense(self):
        payload = {
            "amount": random.randint(10, 500),
            "date": "2025-11-01",
            "user_id": 1,
            "description": "Testing expense",
            "category": "Test"
        }
        self.client.post("/expenses/",json=payload,headers=self.headers)

    @task(1)
    def get_budgets(self):
        self.client.get("/budget/",headers=self.headers)

    @task(2)
    def create_budget(self):
        payload = {
             "total_amount": random.randint(1000, 5000),
            "start_date": "2025-11-01",
            "end_date": "2025-12-01",
            "user_id": 1
        }

        self.client.post("/budget",json=payload,headers=self.headers)