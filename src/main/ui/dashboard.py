import customtkinter
import requests
from main.data.data_manager import DataManager
from datetime import date

class DashboardFrame(customtkinter.CTkFrame):
    def __init__(self, master, data_manager: DataManager, **kwargs):
        super().__init__(master, **kwargs)

        self.data_manager = data_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.projects_count_label = customtkinter.CTkLabel(self, text="Projects: 0", font=("", 20))
        self.projects_count_label.grid(row=0, column=0, padx=20, pady=20)

        self.tasks_count_label = customtkinter.CTkLabel(self, text="Tasks: 0", font=("", 20))
        self.tasks_count_label.grid(row=0, column=1, padx=20, pady=20)

        self.completed_tasks_count_label = customtkinter.CTkLabel(self, text="Completed: 0", font=("", 20))
        self.completed_tasks_count_label.grid(row=0, column=2, padx=20, pady=20)

        self.pending_tasks_count_label = customtkinter.CTkLabel(self, text="Pending: 0", font=("", 20))
        self.pending_tasks_count_label.grid(row=0, column=3, padx=20, pady=20)

        self.progress_bar = customtkinter.CTkProgressBar(self)
        self.progress_bar.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="ew")

        self.today_tasks_label = customtkinter.CTkLabel(self, text="Today's Tasks", font=("", 20))
        self.today_tasks_label.grid(row=2, column=0, columnspan=4, padx=20, pady=10)

        self.today_tasks_list = customtkinter.CTkTextbox(self, height=150)
        self.today_tasks_list.grid(row=3, column=0, columnspan=4, padx=20, pady=10, sticky="ew")

        self.quote_label = customtkinter.CTkLabel(self, text="", font=("", 16, "italic"), wraplength=800)
        self.quote_label.grid(row=4, column=0, columnspan=4, padx=20, pady=20)

        self.update_dashboard()
        self.update_quote()

    def update_dashboard(self):
        projects = self.data_manager.get_projects()
        tasks = self.data_manager.get_tasks()
        completed_tasks = [task for task in tasks if task["completed"]]
        pending_tasks = [task for task in tasks if not task["completed"]]

        self.projects_count_label.configure(text=f"Projects: {len(projects)}")
        self.tasks_count_label.configure(text=f"Tasks: {len(tasks)}")
        self.completed_tasks_count_label.configure(text=f"Completed: {len(completed_tasks)}")
        self.pending_tasks_count_label.configure(text=f"Pending: {len(pending_tasks)}")

        if len(tasks) > 0:
            progress = len(completed_tasks) / len(tasks)
            self.progress_bar.set(progress)
        else:
            self.progress_bar.set(0)

        today = date.today().strftime("%Y-%m-%d")
        today_tasks = [task for task in tasks if task["due_date"] == today]
        today_tasks_str = ""
        for task in today_tasks:
            today_tasks_str += f"- {task['name']}\n"
        
        self.today_tasks_list.delete("0.0", "end")
        self.today_tasks_list.insert("0.0", today_tasks_str)

    def update_quote(self):
        try:
            response = requests.get("https://api.quotable.io/random")
            if response.status_code == 200:
                data = response.json()
                quote = f'"'{data['content']}'"' - {data['author']}'
                self.quote_label.configure(text=quote)
        except requests.exceptions.RequestException:
            self.quote_label.configure(text="Could not fetch a quote. Please check your internet connection.")
