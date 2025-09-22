import customtkinter
from main.data.data_manager import DataManager
from main.ui.dialogs import ProjectDialog, ConfirmationDialog

class ProjectsFrame(customtkinter.CTkFrame):
    def __init__(self, master, *, data_manager: DataManager, poppins_font, poppins_bold_font, **kwargs):
        super().__init__(master, **kwargs)

        self.data_manager = data_manager
        self.poppins_font = poppins_font
        self.poppins_bold_font = poppins_bold_font

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # projects_list_frame should expand

        self.top_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.top_frame.grid_columnconfigure(0, weight=1) # Allow button to expand if needed

        self.add_project_button = customtkinter.CTkButton(self.top_frame, text="Add Project", command=self.add_project_dialog, font=self.poppins_font) # Apply custom font
        self.add_project_button.grid(row=0, column=0, sticky="w") # Align to west

        self.projects_list_frame = customtkinter.CTkScrollableFrame(self)
        self.projects_list_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew") # Adjust top padding

        self.update_projects_list()

    def update_projects_list(self):
        for widget in self.projects_list_frame.winfo_children():
            widget.destroy()

        projects = self.data_manager.get_projects()

        for i, project in enumerate(projects):
            project_frame = customtkinter.CTkFrame(self.projects_list_frame)
            project_frame.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            project_frame.grid_columnconfigure(0, weight=1)

            project_name_label = customtkinter.CTkLabel(project_frame, text=project["name"], font=self.poppins_bold_font) # Apply custom font
            project_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            project_description_label = customtkinter.CTkLabel(project_frame, text=project["description"], font=self.poppins_font) # Apply custom font
            project_description_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

            edit_button = customtkinter.CTkButton(project_frame, text="Edit", command=lambda p=project: self.edit_project_dialog(p), font=self.poppins_font) # Apply custom font
            edit_button.grid(row=0, column=1, padx=10, pady=10)

            delete_button = customtkinter.CTkButton(project_frame, text="Delete", command=lambda p=project: self.delete_project(p), font=self.poppins_font) # Apply custom font
            delete_button.grid(row=0, column=2, padx=10, pady=10)

    def add_project_dialog(self):
        dialog = ProjectDialog(self, title="Add Project", poppins_font=self.poppins_font, poppins_bold_font=self.poppins_bold_font)
        result = dialog.get_input()
        if result:
            self.data_manager.add_project(result["name"], result["description"])
            self.update_projects_list()

    def edit_project_dialog(self, project):
        dialog = ProjectDialog(self, title="Edit Project", project=project, poppins_font=self.poppins_font, poppins_bold_font=self.poppins_bold_font)
        result = dialog.get_input()
        if result:
            self.data_manager.update_project(project["id"], result["name"], result["description"])
            self.update_projects_list()

    def delete_project(self, project):
        dialog = ConfirmationDialog(self, title="Delete Project", text=f"Are you sure you want to delete '{project['name']}'?")
        if dialog.get_input():
            self.data_manager.delete_project(project["id"])
            self.update_projects_list()