import unittest
import os
import json
from main.data.data_manager import DataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.test_data_folder = "test_data"
        os.makedirs(self.test_data_folder, exist_ok=True)
        self.data_manager = DataManager(data_folder=self.test_data_folder)
        self.projects_file = self.data_manager.projects_file
        self.tasks_file = self.data_manager.tasks_file

    def tearDown(self):
        if os.path.exists(self.projects_file):
            os.remove(self.projects_file)
        if os.path.exists(self.tasks_file):
            os.remove(self.tasks_file)
        os.rmdir(self.test_data_folder)

    def test_get_projects_no_file(self):
        projects = self.data_manager.get_projects()
        self.assertEqual(projects, [])

    def test_add_and_get_project(self):
        self.data_manager.add_project("Test Project", "Test Description")
        projects = self.data_manager.get_projects()
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]["name"], "Test Project")

    def test_update_project(self):
        self.data_manager.add_project("Test Project", "Test Description")
        self.data_manager.update_project(1, "Updated Project", "Updated Description")
        project = self.data_manager.get_project(1)
        self.assertEqual(project["name"], "Updated Project")

    def test_delete_project(self):
        self.data_manager.add_project("Test Project", "Test Description")
        self.data_manager.delete_project(1)
        projects = self.data_manager.get_projects()
        self.assertEqual(len(projects), 0)

    def test_get_tasks_no_file(self):
        tasks = self.data_manager.get_tasks()
        self.assertEqual(tasks, [])

    def test_add_and_get_task(self):
        self.data_manager.add_task(1, "Test Task", "2025-12-31")
        tasks = self.data_manager.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["name"], "Test Task")

    def test_update_task(self):
        self.data_manager.add_task(1, "Test Task", "2025-12-31")
        self.data_manager.update_task(1, "Updated Task", "2026-01-01", True)
        task = self.data_manager.get_task(1)
        self.assertEqual(task["name"], "Updated Task")
        self.assertEqual(task["completed"], True)

    def test_delete_task(self):
        self.data_manager.add_task(1, "Test Task", "2025-12-31")
        self.data_manager.delete_task(1)
        tasks = self.data_manager.get_tasks()
        self.assertEqual(len(tasks), 0)

if __name__ == "__main__":
    unittest.main()