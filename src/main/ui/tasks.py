import customtkinter
from main.data.data_manager import DataManager
from main.ui.dialogs import TaskDialog

class TasksFrame(customtkinter.CTkFrame):
    def __init__(self, master, data_manager: DataManager, **kwargs):
        super().__init__(master, **kwargs)

        self.data_manager = data_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.add_task_button = customtkinter.CTkButton(self, text="Add Task", command=self.add_task_dialog)
        self.add_task_button.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.tasks_list_frame = customtkinter.CTkScrollableFrame(self)
        self.tasks_list_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.update_tasks_list()

    def update_tasks_list(self):
        for widget in self.tasks_list_frame.winfo_children():
            widget.destroy()

        tasks = self.data_manager.get_tasks()

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
        # I will add a confirmation dialog later.
        self.data_manager.delete_task(task["id"])
        self.update_tasks_list()

    def toggle_task_completion(self, task):
        self.data_manager.update_task(task["id"], task["name"], task["due_date"], not task["completed"])
        self.update_tasks_list()