import customtkinter

class ProjectDialog(customtkinter.CTkToplevel):
    def __init__(self, master, title, project=None):
        super().__init__(master)
        self.title(title)
        self.geometry("400x200")
        self.lift()
        self.attributes("-topmost", True)
        self.grab_set()

        self.project = project
        self.result = None

        self.name_label = customtkinter.CTkLabel(self, text="Name:")
        self.name_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.name_entry = customtkinter.CTkEntry(self, width=250)
        self.name_entry.grid(row=0, column=1, padx=20, pady=10)

        self.description_label = customtkinter.CTkLabel(self, text="Description:")
        self.description_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.description_entry = customtkinter.CTkEntry(self, width=250)
        self.description_entry.grid(row=1, column=1, padx=20, pady=10)

        if self.project:
            self.name_entry.insert(0, self.project["name"])
            self.description_entry.insert(0, self.project["description"])

        self.ok_button = customtkinter.CTkButton(self, text="OK", command=self.ok_event)
        self.ok_button.grid(row=2, column=0, padx=20, pady=20, sticky="e")

        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.cancel_event)
        self.cancel_button.grid(row=2, column=1, padx=20, pady=20, sticky="w")

    def ok_event(self):
        self.result = {
            "name": self.name_entry.get(),
            "description": self.description_entry.get()
        }
        self.destroy()

    def cancel_event(self):
        self.destroy()

    def get_input(self):
        self.wait_window()
        return self.result

class TaskDialog(customtkinter.CTkToplevel):
    def __init__(self, master, title, data_manager, task=None):
        super().__init__(master)
        self.title(title)
        self.geometry("400x250")
        self.lift()
        self.attributes("-topmost", True)
        self.grab_set()

        self.data_manager = data_manager
        self.task = task
        self.result = None

        self.name_label = customtkinter.CTkLabel(self, text="Name:")
        self.name_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.name_entry = customtkinter.CTkEntry(self, width=250)
        self.name_entry.grid(row=0, column=1, padx=20, pady=10)

        self.due_date_label = customtkinter.CTkLabel(self, text="Due Date:")
        self.due_date_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.due_date_entry = customtkinter.CTkEntry(self, width=250)
        self.due_date_entry.grid(row=1, column=1, padx=20, pady=10)

        self.project_label = customtkinter.CTkLabel(self, text="Project:")
        self.project_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.project_menu = customtkinter.CTkOptionMenu(self, width=250, values=[])
        self.project_menu.grid(row=2, column=1, padx=20, pady=10)
        self.update_project_menu()

        if self.task:
            self.name_entry.insert(0, self.task["name"])
            self.due_date_entry.insert(0, self.task["due_date"])
            project = self.data_manager.get_project(self.task["project_id"])
            if project:
                self.project_menu.set(project["name"])

        self.ok_button = customtkinter.CTkButton(self, text="OK", command=self.ok_event)
        self.ok_button.grid(row=3, column=0, padx=20, pady=20, sticky="e")

        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.cancel_event)
        self.cancel_button.grid(row=3, column=1, padx=20, pady=20, sticky="w")

    def get_input(self):
        self.wait_window()
        return self.result

class ConfirmationDialog(customtkinter.CTkToplevel):
    def __init__(self, master, title, text):
        super().__init__(master)
        self.title(title)
        self.geometry("300x150")
        self.lift()
        self.attributes("-topmost", True)
        self.grab_set()

        self.result = False

        self.label = customtkinter.CTkLabel(self, text=text)
        self.label.pack(padx=20, pady=20)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.yes_event)
        self.yes_button.pack(side="left", padx=20, pady=20)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.no_event)
        self.no_button.pack(side="right", padx=20, pady=20)

    def yes_event(self):
        self.result = True
        self.destroy()

    def no_event(self):
        self.destroy()

    def get_input(self):
        self.wait_window()
        return self.result