
import customtkinter as ctk
# from FluidBurnPage import *
from _KeyDesignParametersPage import KeyDesignParameters
from _HeatBalance import HeatBalance
from _AdditionalParameters import AdditionalParameters

from TableViewPage import *
from utilities import toFixed

class TabPage(ctk.CTkTabview):

    def on_resize(self, event):
        if event.widget is self.master:
            # Отменяем предыдущую запланированную задачу, если она существует
            if self.resize_task_id:
                self.master.after_cancel(self.resize_task_id)

            # Устанавливаем новую задачу с задержкой (200 мс)
            self.resize_task_id = self.master.after(200, self._size, event)

    def _size(self, event):
        if(event.widget is self.master):
            self.cards._size(event)
            self.table._size(event)

    def __init__(self, master, database, **kwargs):
        super().__init__(master, **kwargs)
        
        self.database = database
        self.master = master
        self.resize_task_id  = None  # Таймер для дебаунсинга 
        # create tabs 
        self.grid_propagate(False)
        self.configure(width=1700, height=1100)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.add("Ключевые расчетные параметры")
        self.add("Тепловой баланс")
        self.add("Дополнительные параметры")

        self.tab("Ключевые расчетные параметры").columnconfigure((0), weight=1)
        self.tab("Ключевые расчетные параметры").rowconfigure((0), weight=1)

        self.tab("Тепловой баланс").columnconfigure((0), weight=1)
        self.tab("Тепловой баланс").rowconfigure((0), weight=1)

        self.tab("Дополнительные параметры").columnconfigure((0), weight=1)
        self.tab("Дополнительные параметры").rowconfigure((0), weight=1)


        self.keydesign = KeyDesignParameters(master=self.tab("Ключевые расчетные параметры"), root=master, database=self.database)
        self.balance = HeatBalance(master=self.tab("Тепловой баланс"), root=master, database=self.database)
        self.addparams = AdditionalParameters(master=self.tab("Дополнительные параметры"), root=master, database=self.database)
        
        self.keydesign.grid(row=0, column=0, sticky="nsew")
        self.balance.grid(row=0, column=0, sticky="nsew")
        self.addparams.grid(row=0, column=0, sticky="nsew") 
     
    def open_last(self):
        self.cards.start_up()
        self.table.update()

    def open_exp(self, heating_data, gas_data):    
        print("-----heating_data-----")
        print(heating_data)
        print("-----gas-----")
        print(gas_data)
        self.update_all(heating_data, gas_data)

    def show_result(self, data):
        res = self.cards.show_result(data) 
        return res
    
    def update_all(self, heating_data, gas_result):
        self.keydesign.update(heating_data, gas_result)
        self.balance.update(heating_data)
        self.addparams.update(gas_result)
        pass
    
    def set_heating_data(self, heating_data):
        self.cards.set_heating_data(heating_data)
    
    def get_heating_data(self):
        return self.cards.get_heating_data() 