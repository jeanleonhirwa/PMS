import customtkinter
from main.data.data_manager import DataManager
from main.ui.dialogs import ProjectDialog

class ProjectsFrame(customtkinter.CTkFrame):
    def __init__(self, master, data_manager: DataManager, **kwargs):
        super().__init__(master, **kwargs)

        self.data_manager = data_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.add_project_button = customtkinter.CTkButton(self, text="Add Project", command=self.add_project_dialog)
        self.add_project_button.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.projects_list_frame = customtkinter.CTkScrollableFrame(self)
        self.projects_list_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.update_projects_list()

    def update_projects_list(self):
        for widget in self.projects_list_frame.winfo_children():
            widget.destroy()

        projects = self.data_manager.get_projects()

        for i, project in enumerate(projects):
            project_frame = customtkinter.CTkFrame(self.projects_list_frame)
            project_frame.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            project_frame.grid_columnconfigure(0, weight=1)

            project_name_label = customtkinter.CTkLabel(project_frame, text=project["name"], font=("", 16, "bold"))
            project_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            project_description_label = customtkinter.CTkLabel(project_frame, text=project["description"])
            project_description_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

            edit_button = customtkinter.CTkButton(project_frame, text="Edit", command=lambda p=project: self.edit_project_dialog(p))
            edit_button.grid(row=0, column=1, padx=10, pady=10)

            delete_button = customtkinter.CTkButton(project_frame, text="Delete", command=lambda p=project: self.delete_project(p))
            delete_button.grid(row=0, column=2, padx=10, pady=10)

    def add_project_dialog(self):
        dialog = ProjectDialog(self, title="Add Project")
        result = dialog.get_input()
        if result:
            self.data_manager.add_project(result["name"], result["description"])
            self.update_projects_list()

    def edit_project_dialog(self, project):
        dialog = ProjectDialog(self, title="Edit Project", project=project)
        result = dialog.get_input()
        if result:
            self.data_manager.update_project(project["id"], result["name"], result["description"])
            self.update_projects_list()

    def delete_project(self, project):
        # I will add a confirmation dialog later.
        self.data_manager.delete_project(project["id"])
        self.update_projects_list()