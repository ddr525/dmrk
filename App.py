import customtkinter

import ctypes

from _DataSideBar import *
from FluidBurnPage import *
from _Database import Database
from _TabPage import TabPage
from custom_widget.CTkXYFrame.ctk_xyframe import CTkXYFrame 

class App(customtkinter.CTk):
    def __init__(self, scale_factor):
        super().__init__()

        xy_frame = CTkXYFrame(self)
        xy_frame.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        
        self.wm_iconbitmap("icons/QARMET-transparent-logo.ico")
        self.configure(fg_color="black") 
        
        self.database = Database()

        # configure window
        self.title("Расчет горения топлива")

        width = 1280
        height = 720

        width = int(width / scale_factor)
        height = int(height / scale_factor)
        spawn_x = int((self.winfo_screenwidth() - width) / 2)
        spawn_y = int((self.winfo_screenheight() - height) / 2)

        self.geometry(f"{width}x{height}+{spawn_x}+{spawn_y}")

        # Настройка сетки окна
        self.grid_columnconfigure(0, minsize=260)   # Левая колонка фиксированная
        self.grid_columnconfigure(1, weight=1)      # Правая колонка адаптивная
        self.grid_rowconfigure(0, weight=1)         # Высота адаптивная

        self.sidebar_frame = DataSideBar(xy_frame, database=self.database)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, 
                                padx=(5, 5), 
                                pady=(35, 20), 
                                sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
         
        self.tabview = TabPage(xy_frame, database=self.database)
        self.tabview.grid(row=0, column=1, rowspan=4, padx=(0, 5), pady=(20, 20), sticky="nsew")

        self.sidebar_frame.set_burn_page(self.tabview) 

    def calculate(self, data):
        return self.tabview.show_result(data)
    
    def update_all(self):
        self.tabview.update_all()
    
    def set_heating_data(self, heating_data):
        self.tabview.set_heating_data(heating_data)
    
    def get_heating_data(self):
        return self.tabview.get_heating_data()
    
    def open_exp(self, id):
        self.tabview.open_exp(id)
        self.sidebar_frame.open_exp(id)

    def set_exp_number(self, id):
        self.sidebar_frame.open_exp(id)
    
    def open_last(self):
        self.tabview.open_last()
    
    def delete_exp_nummber(self, id):
        self.sidebar_frame.delete_exp_nummber(id)


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ctypes.windll.user32.SetProcessDPIAware()
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100  # Например, 1.25 для 125%
    except Exception:
        scale_factor = 1.0  # Если не удалось, используем 100%

    app = App(scale_factor)
    
    app._state_before_windows_set_titlebar_color = 'zoomed'

    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
    
    app.mainloop()