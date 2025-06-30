from CTkMessagebox import CTkMessagebox 
import customtkinter

from ExcelExport import export_to_excel
from FurnaceParamWindow import FurnaceParamWindow
from _AllParameters import *
from ExperimentWindow import *
from _ParametersListButtons import *
#доделать скролл
class DataSideBar(customtkinter.CTkFrame): 
    def __init__(self, master, database, **kwargs): 
        super().__init__(master, **kwargs)
        
        self.master = master
        self.toplevel = None
        self.database = database
        self.configure(fg_color="transparent") 
        self.grid_columnconfigure(0, weight=1) 
        
        self.plistb = ParametersListButtons(master=self, database=self.database) 
        self.plistb.grid(row=0, column=0, sticky="nsew")
        
        self.gases = AllParameters(self, database=self.database)
        self.gases.grid(row=1, column=0, pady=10, sticky="nsew") 

    def update_all(self, heating_data, gas_result):
        # Traverse up the widget hierarchy to find the App instance
        parent = self.master
        while parent is not None:
            if hasattr(parent, "update_all"):
                parent.update_all(heating_data, gas_result)
                break
            parent = getattr(parent, "master", None)
        # Call update_all on the correct object; replace 'self.master' with the appropriate reference if needed
        # if hasattr(self.plistb, "update_all"):
        #     self.plistb.update_all()
        # else:
        #     print("update_all method not found on plistb or master.")

    # def update(self):
    #     self.exp_num = str(self.database.get_experiment_number())
    #     self.scaling_label.configure(text="Номер опыта — " + self.exp_num)

    def open_exp(self, id):
        parent = self.master
        while parent is not None:
            if hasattr(parent, "update_all"):
                parent.open_exp(id)
                break
            parent = getattr(parent, "master", None)
    
    def start_export(self):
        heating_data = self.master.get_heating_data()
        if("data" not in heating_data):
            CTkMessagebox(title="Ошибка экспорта", message=f"Нет данных для экспорта в excel", icon='cancel')
            return
        
        filename = export_to_excel(heating_data, self.exp_num)
        
        CTkMessagebox(title="Экспорт завершен!", message=f"Данные для опыта № {self.exp_num} сохранены в {filename}", icon='info')
        
    
    def delete_exp_nummber(self, id):
        if(self.exp_num == str(id)):
            self.update()


    def _reset_data(self):
        self.database.reset()
        self.list.update_list()
        self.plist.update()

    def set_burn_page(self, page):
        self.page = page

    # def _open_table_view(self):
    #     if(self.toplevel is None or not self.toplevel.winfo_exists()):
    #         self.toplevel = TableViewWindow(self, page=self.page)
    #         self.toplevel.after(10, self.toplevel.lift)
    #     else:
    #         self.toplevel.focus()

    # def _open_exp_view(self):
    #     if(self.toplevel is None or not self.toplevel.winfo_exists()):
    #         self.toplevel = ExperimentWindow(database=self.database, page=self.master)
    #         self.toplevel.after(10, self.toplevel.lift)
    #     else:
    #         self.toplevel.focus()

    def _open_furnace_view(self):
        if(self.furnacetoplevel is None or not self.furnacetoplevel.winfo_exists()):
            self.furnacetoplevel = FurnaceParamWindow(database=self.database, page=self.master)
            self.furnacetoplevel.after(10, self.furnacetoplevel.lift)
        else:
            self.furnacetoplevel.focus()
