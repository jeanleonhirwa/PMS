import customtkinter
from main.data.data_manager import DataManager
from main.ui.dashboard import DashboardFrame
from main.ui.projects import ProjectsFrame
from main.ui.tasks import TasksFrame

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Project Management System")
        self.geometry("1100x580")

        self.data_manager = DataManager()

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="PMS",
                                                             font=customtkinter.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Dashboard",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.projects_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Projects",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.projects_button_event)
        self.projects_button.grid(row=2, column=0, sticky="ew")

        self.tasks_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Tasks",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.tasks_button_event)
        self.tasks_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create dashboard frame
        self.dashboard_frame = DashboardFrame(self, data_manager=self.data_manager, corner_radius=0, fg_color="transparent")

        # create projects frame
        self.projects_frame = ProjectsFrame(self, data_manager=self.data_manager, corner_radius=0, fg_color="transparent")

        # create tasks frame
        self.tasks_frame = TasksFrame(self, data_manager=self.data_manager, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("dashboard")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "dashboard" else "transparent")
        self.projects_button.configure(fg_color=("gray75", "gray25") if name == "projects" else "transparent")
        self.tasks_button.configure(fg_color=("gray75", "gray25") if name == "tasks" else "transparent")

        # show selected frame
        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.dashboard_frame.grid_forget()
        if name == "projects":
            self.projects_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.projects_frame.grid_forget()
        if name == "tasks":
            self.tasks_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.tasks_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("dashboard")

    def projects_button_event(self):
        self.select_frame_by_name("projects")

    def tasks_button_event(self):
        self.select_frame_by_name("tasks")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)