from tests.test_db import BaseTestCase

class TestTasksAPI(BaseTestCase):

    def test_01_read_empty_tasks(self):
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_02_create_task(self):
        response = self.client.post("/tasks/", json={"title": "Test Task", "description": "This is a test"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Test Task")
        self.assertEqual(data["description"], "This is a test")
        self.assertEqual(data["status"], "Todo")
        self.__class__.task_id = data["id"]

    def test_03_update_task(self):
        task_id = getattr(self, "task_id", None)
        if task_id is None:
            self.skipTest("No task created")
        response = self.client.patch(f"/tasks/{task_id}", json={"status": "In Progress"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "In Progress")

    def test_04_update_invalid_status(self):
        task_id = getattr(self, "task_id", None)
        if task_id is None:
            self.skipTest("No task created")
        response = self.client.patch(f"/tasks/{task_id}", json={"status": "InvalidStatus"})
        self.assertEqual(response.status_code, 400)

    def test_05_delete_task(self):
        task_id = getattr(self, "task_id", None)
        if task_id is None:
            self.skipTest("No task created")
        response = self.client.delete(f"/tasks/{task_id}")
        self.assertEqual(response.status_code, 204)
        
        # Verify it is deleted (404)
        response = self.client.patch(f"/tasks/{task_id}", json={"status": "Done"})
        self.assertEqual(response.status_code, 404)

    def test_06_delete_nonexistent_task(self):
        response = self.client.delete("/tasks/999999")
        self.assertEqual(response.status_code, 404)
