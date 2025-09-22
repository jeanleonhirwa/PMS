import customtkinter
from main.data.data_manager import DataManager
from main.ui.dialogs import TaskDialog, ConfirmationDialog

class TasksFrame(customtkinter.CTkFrame):
    def __init__(self, master, *, data_manager: DataManager, poppins_font, poppins_bold_font, **kwargs):
        super().__init__(master, **kwargs)

        self.data_manager = data_manager
        self.selected_project_id = None

        self.poppins_font = poppins_font # Store as instance variable
        self.poppins_bold_font = poppins_bold_font # Store as instance variable

        # Define fonts for strikethrough
        self.completed_font = customtkinter.CTkFont(family="Poppins", size=16, weight="bold", overstrike=True) # Use "Poppins"
        self.normal_font = customtkinter.CTkFont(family="Poppins", size=16, weight="bold") # Use "Poppins"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # tasks_list_frame should expand

        self.top_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.top_frame.grid_columnconfigure(0, weight=1) # Allow button to expand if needed

        self.add_task_button = customtkinter.CTkButton(self.top_frame, text="Add Task", command=self.add_task_dialog, font=self.poppins_font) # Apply custom font
        self.add_task_button.grid(row=0, column=0, sticky="w") # Align to west

        self.project_filter_menu = customtkinter.CTkOptionMenu(self.top_frame, values=[], command=lambda value: self.filter_by_project(value), font=self.poppins_font) # Apply custom font
        self.project_filter_menu.grid(row=0, column=1, sticky="e") # Align to east

        self.tasks_list_frame = customtkinter.CTkScrollableFrame(self)
        self.tasks_list_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew") # Adjust top padding

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

            task_name_label = customtkinter.CTkLabel(task_frame, text=task["name"], font=self.normal_font) # Apply custom font
            task_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            task_due_date_label = customtkinter.CTkLabel(task_frame, text=f"Due: {task['due_date']}", font=self.poppins_font) # Apply custom font
            task_due_date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

            completed_checkbox = customtkinter.CTkCheckBox(task_frame, text="Completed", variable=customtkinter.BooleanVar(value=task["completed"]),
                                                           command=lambda t=task: self.toggle_task_completion(t), font=self.poppins_font) # Apply custom font
            completed_checkbox.grid(row=0, column=1, padx=10, pady=10)

            edit_button = customtkinter.CTkButton(task_frame, text="Edit", command=lambda t=task: self.edit_task_dialog(t), font=self.poppins_font) # Apply custom font
            edit_button.grid(row=0, column=2, padx=10, pady=10)

            delete_button = customtkinter.CTkButton(task_frame, text="Delete", command=lambda t=task: self.delete_task(t), font=self.poppins_font) # Apply custom font
            delete_button.grid(row=0, column=3, padx=10, pady=10)

            # Apply visual feedback for completed tasks
            if task["completed"]:
                task_name_label.configure(text_color="gray", font=self.completed_font)
                task_due_date_label.configure(text_color="gray")
            else:
                task_name_label.configure(text_color=customtkinter.ThemeManager.theme["CTkLabel"]["text_color"], font=self.normal_font)

    def add_task_dialog(self):
        dialog = TaskDialog(self, title="Add Task", data_manager=self.data_manager, poppins_font=self.poppins_font, poppins_bold_font=self.poppins_bold_font)
        result = dialog.get_input()
        if result:
            self.data_manager.add_task(result["project_id"], result["name"], result["due_date"])
            self.update_tasks_list()

    def edit_task_dialog(self, task):
        dialog = TaskDialog(self, title="Edit Task", data_manager=self.data_manager, task=task, poppins_font=self.poppins_font, poppins_bold_font=self.poppins_bold_font)
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