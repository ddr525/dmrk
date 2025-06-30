
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

    def open_exp(self, id):
        exp = self.database.get_experiment_by_id(id)
    
        heating_data, gas_data = self.show_exp(exp)
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
    



    def show_exp(self, exp):
        res = exp.results

        heating_data = self.parse_heating_data(exp)

        data = []

        cards = {}

        for el in res:
            if("CO2" in el.parameter or "N2" in el.parameter or "H2O" in el.parameter or "O2" in el.parameter):
                cards[el.parameter] = el.value
            else:
                if("%" in el.parameter or "тг" in el.parameter):
                    data.append((el.parameter, toFixed(el.value, 1)))
                else:
                    data.append((el.parameter, toFixed(el.value, 3)))
            
        data.append(("cards", cards))

        # self.update(data)
        return heating_data, data

    def parse_heating_data(self, exp):

        heating_data = {
            "Расчет нагрева металла": {},
            "Тепловой баланс" : {},
            "График": {},
            "data": {},
            "t_data": {}
        }
        
 
        # metal heating
        for zone in exp.metal_results[0].zones:
            #print(zone.name)
            heating_data["Расчет нагрева металла"][zone.name] = {}

            for param in zone.parameters:
                heating_data["Расчет нагрева металла"][zone.name][param.name + "," + param.units] = param.value

        for param in exp.metal_results[0].parameters:
            #print(param.name)
            heating_data["Расчет нагрева металла"][param.name + "," + param.units] = param.value

        for zone in exp.balance_results[0].zones:
            #print(zone.name)
            heating_data["Тепловой баланс"][zone.name] = {}

            for heat_flow in zone.heat_flows:
                #print(heat_flow.type)
                heating_data["Тепловой баланс"][zone.name][heat_flow.type] = {}

                for detail in heat_flow.details:
                    #print(detail.name)
                    heating_data["Тепловой баланс"][zone.name][heat_flow.type][detail.name + "," + detail.units] = detail.value
            
            for param in zone.params:
                #print(param.name)
                heating_data["Тепловой баланс"][zone.name][param.name + "," + param.units] = param.value

        for param in exp.heat_graphs[0].params:
            #print(param.name)
            heating_data["График"][param.name] = param.value

        for dot in exp.heat_graphs[0].dots:
            #print(dot.name)
            heating_data["График"][dot.name] = [data.value for data in dot.data]
        # e = exp.history_parameters

        tmn = 0.0
        twMetn = 0.0
        twDif = 0.0

        for param in exp.history_parameters:
            if(param.parameter_name == "Время нагрева (time_H)" or param.parameter_name == "Время в методической зоне" or param.parameter_name == "Время в первой сварочной зоне" or param.parameter_name == "Время во второй сварочной зоне" or param.parameter_name == "Время в томильной зоне"):
                heating_data["data"][param.parameter_name] = param.value

            if(param.parameter_name == "Начальная температура металла (tmn)"):
                tmn = param.value
            elif(param.parameter_name == "Температура методической зоны (twMetn)"):
                twMetn = param.value
            elif(param.parameter_name == "Разница температур при посаде (twDif)"):
                twDif = param.value


        s = self.database.get_parameters("Толщина сляба (s)").value
        bb = self.database.get_parameters("Длина сляба (bb)").value
        a = self.database.get_parameters("Ширина сляба (a)").value
        Lp = self.database.get_parameters("Длина печи (Lp)").value

        heating_data["t_data"]["Температура сляба при посаде"] = tmn
        heating_data["t_data"]["Температура верха печи при посаде"] = twMetn
        heating_data["t_data"]["Температура низа печи при посаде"] = twMetn - twDif
        heating_data["Расчет нагрева металла"]["Толщина сляба"] = s
        heating_data["Расчет нагрева металла"]["Длина сляба"] = bb
        heating_data["Расчет нагрева металла"]["Ширина сляба"] = a
        heating_data["Расчет нагрева металла"]["Длина печи"] = Lp
        heating_data["Расчет нагрева металла"]["Марка стали"] = str(self.database.get_parameters("Марка стали (группа нагрева)").value_str) 
        
        return heating_data 
    