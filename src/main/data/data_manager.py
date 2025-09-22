import json
import os

class DataManager:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        self.projects_file = os.path.join(self.data_folder, "projects.json")
        self.tasks_file = os.path.join(self.data_folder, "tasks.json")

    def _read_data(self, file_path):
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _write_data(self, file_path, data):
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    def get_projects(self):
        return self._read_data(self.projects_file)

    def get_project(self, project_id):
        projects = self.get_projects()
        for project in projects:
            if project["id"] == project_id:
                return project
        return None

    def add_project(self, name, description):
        projects = self.get_projects()
        new_project = {
            "id": len(projects) + 1,
            "name": name,
            "description": description,
        }
        projects.append(new_project)
        self._write_data(self.projects_file, projects)
        return new_project

    def update_project(self, project_id, name, description):
        projects = self.get_projects()
        for project in projects:
            if project["id"] == project_id:
                project["name"] = name
                project["description"] = description
                self._write_data(self.projects_file, projects)
                return project
        return None

    def delete_project(self, project_id):
        projects = self.get_projects()
        projects = [p for p in projects if p["id"] != project_id]
        self._write_data(self.projects_file, projects)

    def get_tasks(self):
        return self._read_data(self.tasks_file)

    def get_tasks_by_project(self, project_id):
        tasks = self.get_tasks()
        return [task for task in tasks if task["project_id"] == project_id]

    def get_task(self, task_id):
        tasks = self.get_tasks()
        for task in tasks:
            if task["id"] == task_id:
                return task
        return None

    def add_task(self, project_id, name, due_date):
        tasks = self.get_tasks()
        new_task = {
            "id": len(tasks) + 1,
            "project_id": project_id,
            "name": name,
            "due_date": due_date,
            "completed": False,
        }
        tasks.append(new_task)
        self._write_data(self.tasks_file, tasks)
        return new_task

    def update_task(self, task_id, name, due_date, completed):
        tasks = self.get_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["name"] = name
                task["due_date"] = due_date
                task["completed"] = completed
                self._write_data(self.tasks_file, tasks)
                return task
        return None

    def delete_task(self, task_id):
        tasks = self.get_tasks()
        tasks = [t for t in tasks if t["id"] != task_id]
        self._write_data(self.tasks_file, tasks)