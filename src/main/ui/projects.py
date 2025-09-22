import customtkinter
from main.data.data_manager import DataManager
from main.ui.dialogs import ProjectDialog, ConfirmationDialog

class ProjectsFrame(customtkinter.CTkFrame):
    # ... (code)
    def delete_project(self, project):
        dialog = ConfirmationDialog(self, title="Delete Project", text=f"Are you sure you want to delete '{project['name']}'?")
        if dialog.get_input():
            self.data_manager.delete_project(project["id"])
            self.update_projects_list()