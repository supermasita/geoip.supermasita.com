# Requires FAKER
#   pip install faker

from locust import HttpLocust, TaskSet, task
from faker import Faker


class WebsiteTasks(TaskSet):

    @task
    def ipv4_json(self):
        fake = Faker()
        with self.client.get('/?ip=%s&json' % (fake.ipv4()),
                             catch_response=True) as response:
            if response.status_code == 400:
                response.success()

    @task
    def ipv4(self):
        fake = Faker()
        with self.client.get('/?ip=%s' % (fake.ipv4()),
                             catch_response=True) as response:
            if response.status_code == 400:
                response.success()

    @task
    def ipv6(self):
        fake = Faker()
        with self.client.get('/?ip=%s' % (fake.ipv6()),
                             catch_response=True) as response:
            if response.status_code == 400:
                response.success()

    @task
    def ipv6_json(self):
        fake = Faker()
        with self.client.get('/?ip=%s&json' % (fake.ipv6()),
                             catch_response=True) as response:
            if response.status_code == 400:
                response.success()


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 1000
    max_wait = 5000
