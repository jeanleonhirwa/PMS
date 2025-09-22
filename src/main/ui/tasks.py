import customtkinter
from main.data.data_manager import DataManager
from main.ui.dialogs import TaskDialog, ConfirmationDialog

class TasksFrame(customtkinter.CTkFrame):
    def __init__(self, master, *, data_manager: DataManager, **kwargs):
        super().__init__(master, **kwargs)

        self.data_manager = data_manager
        self.selected_project_id = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_frame = customtkinter.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.add_task_button = customtkinter.CTkButton(self.top_frame, text="Add Task", command=self.add_task_dialog)
        self.add_task_button.pack(side="left")

        self.project_filter_menu = customtkinter.CTkOptionMenu(self.top_frame, values=[], command=self.filter_by_project)
        self.project_filter_menu.pack(side="right")
        self.update_project_filter_menu()

        self.tasks_list_frame = customtkinter.CTkScrollableFrame(self)
        self.tasks_list_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.update_tasks_list()

    def update_project_filter_menu(self):
        projects = self.data_manager.get_projects()
        project_names = ["All Projects"] + [project["name"] for project in projects]
        self.project_filter_menu.configure(values=project_names)
        self.project_filter_menu.set("All Projects")

    def filter_by_project(self, selected_project_name):
        if selected_project_name == "All Projects":
            self.selected_project_id = None
        else:
            projects = self.data_manager.get_projects()
            for project in projects:
                if project["name"] == selected_project_name:
                    self.selected_project_id = project["id"]
                    break
        self.update_tasks_list()

    def update_tasks_list(self):
        for widget in self.tasks_list_frame.winfo_children():
            widget.destroy()

        if self.selected_project_id is None:
            tasks = self.data_manager.get_tasks()
        else:
            tasks = self.data_manager.get_tasks_by_project(self.selected_project_id)

        for i, task in enumerate(tasks):
            task_frame = customtkinter.CTkFrame(self.tasks_list_frame)
            task_frame.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            task_frame.grid_columnconfigure(0, weight=1)

            task_name_label = customtkinter.CTkLabel(task_frame, text=task["name"], font=("", 16, "bold"))
            task_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            task_due_date_label = customtkinter.CTkLabel(task_frame, text=f"Due: {task['due_date']}")
            task_due_date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

            completed_checkbox = customtkinter.CTkCheckBox(task_frame, text="Completed", variable=customtkinter.BooleanVar(value=task["completed"]),
                                                           command=lambda t=task: self.toggle_task_completion(t))
            completed_checkbox.grid(row=0, column=1, padx=10, pady=10)

            edit_button = customtkinter.CTkButton(task_frame, text="Edit", command=lambda t=task: self.edit_task_dialog(t))
            edit_button.grid(row=0, column=2, padx=10, pady=10)

            delete_button = customtkinter.CTkButton(task_frame, text="Delete", command=lambda t=task: self.delete_task(t))
            delete_button.grid(row=0, column=3, padx=10, pady=10)

    def add_task_dialog(self):
        dialog = TaskDialog(self, title="Add Task", data_manager=self.data_manager)
        result = dialog.get_input()
        if result:
            self.data_manager.add_task(result["project_id"], result["name"], result["due_date"])
            self.update_tasks_list()

    def edit_task_dialog(self, task):
        dialog = TaskDialog(self, title="Edit Task", data_manager=self.data_manager, task=task)
        result = dialog.get_input()
        if result:
            self.data_manager.update_task(task["id"], result["name"], result["due_date"], task["completed"])
            self.update_tasks_list()

    def delete_task(self, task):
        dialog = ConfirmationDialog(self, title="Delete Task", text=f"Are you sure you want to delete '{task['name']}'?")
        if dialog.get_input():
            self.data_manager.delete_task(task["id"])
            self.update_tasks_list()

    def toggle_task_completion(self, task):
        self.data_manager.update_task(task["id"], task["name"], task["due_date"], not task["completed"])
        self.update_tasks_list()