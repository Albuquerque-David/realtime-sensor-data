from locust import HttpUser, TaskSet, task, between

class SensorTasks(TaskSet):
    @task
    def get_average(self):
        self.client.get("/sensors/average?equipmentId=STATION_1&period=24h")

class SensorUser(HttpUser):
    tasks = [SensorTasks]
    wait_time = between(1, 5)
