import customtkinter
import requests
from main.data.data_manager import DataManager
from datetime import date

class DashboardFrame(customtkinter.CTkFrame):
    def __init__(self, master, *, data_manager: DataManager, poppins_font, poppins_bold_font, **kwargs):
        super().__init__(master, **kwargs)

        self.data_manager = data_manager
        self.poppins_font = poppins_font
        self.poppins_bold_font = poppins_bold_font

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Projects progress frame
        self.grid_rowconfigure(2, weight=1) # Today's tasks list
        self.grid_rowconfigure(3, weight=0) # Quote label

        self.projects_progress_frame = customtkinter.CTkScrollableFrame(self)
        self.projects_progress_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.projects_progress_frame.grid_columnconfigure(0, weight=1)

        self.today_tasks_label = customtkinter.CTkLabel(self, text="Today's Tasks", font=self.poppins_bold_font) # Apply custom font
        self.today_tasks_label.grid(row=1, column=0, padx=20, pady=(20, 10)) # Add top padding

        self.today_tasks_list = customtkinter.CTkTextbox(self, height=150, font=self.poppins_font) # Apply custom font
        self.today_tasks_list.grid(row=2, column=0, padx=20, pady=10, sticky="nsew") # Use nsew for expansion

        self.quote_label = customtkinter.CTkLabel(self, text="", font=self.poppins_font, wraplength=800) # Apply custom font
        self.quote_label.grid(row=3, column=0, padx=20, pady=(10, 20)) # Adjust padding

        self.update_dashboard()
        self.update_quote()

    def update_dashboard(self):
        for widget in self.projects_progress_frame.winfo_children():
            widget.destroy()

        projects = self.data_manager.get_projects()
        for i, project in enumerate(projects):
            project_frame = customtkinter.CTkFrame(self.projects_progress_frame)
            project_frame.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            project_frame.grid_columnconfigure(0, weight=1)

            project_name_label = customtkinter.CTkLabel(project_frame, text=project["name"], font=self.poppins_bold_font) # Apply custom font
            project_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            tasks = self.data_manager.get_tasks_by_project(project["id"])
            completed_tasks = [task for task in tasks if task["completed"]]
            
            progress = 0
            if len(tasks) > 0:
                progress = len(completed_tasks) / len(tasks)

            progress_bar = customtkinter.CTkProgressBar(project_frame)
            progress_bar.set(progress)
            progress_bar.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
            
            progress_label = customtkinter.CTkLabel(project_frame, text=f"{int(progress * 100)}%", font=self.poppins_font) # Apply custom font
            progress_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")


        today = date.today().strftime("%Y-%m-%d")
        today_tasks = [task for task in self.data_manager.get_tasks() if task["due_date"] == today]
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
                quote = f'"{data["content"]}" - {data["author"]}'
                self.quote_label.configure(text=quote)
        except requests.exceptions.RequestException:
            self.quote_label.configure(text="Could not fetch a quote. Please check your internet connection.")
