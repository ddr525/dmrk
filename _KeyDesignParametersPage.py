import customtkinter as ctk 
# from tables.GraphView import GraphView
from utilities import toFixed

class KeyDesignParameters(ctk.CTkFrame):
    def __init__(self, master, root, database, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#7c7878", width=kwargs.get("width", 250))
        
        self.database = database
        
        self.font=ctk.CTkFont(size=13, weight="bold")
        self.list = database.get_gases() 
    
    def update(self, heating_data, gas_result):
        firstblock = ctk.CTkFrame(self, fg_color="transparent")
        firstblock.grid(row=0, column=0)

        result = heating_data["Расчет нагрева металла"]
        all_time = heating_data["data"]["Время нагрева (time_H)"]

        #-----------таблица----------------------
        calculation_table = ctk.CTkFrame(firstblock, fg_color="black", corner_radius=0, border_width=2, border_color="black")
        calculation_table.grid(row=0,column=0)
        #----------------------------------------

        #-----------параметры под таблицей-------
        parameters = ctk.CTkFrame(firstblock, fg_color="#7c7878", corner_radius=0)
        parameters.grid(row=1,column=0)
        #----------------------------------------

        #-----------график-----------------------
        # graph = ctk.CTkFrame(firstblock, fg_color="black", corner_radius=0, border_width=1, border_color="black")
        # graph.grid(row=2,column=0)
        #----------------------------------------

        #----------row=0---------------------------------
        self.newcell(calculation_table, row=0, column=0, text="№1") 
         
        block=ctk.CTkFrame(calculation_table, fg_color="transparent", corner_radius=0, border_width=1 , border_color="black")
        block.grid(
            row=0, 
            column=1, 
            padx=(0,1), 
            sticky="ew"
            ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Расчет нагрева сляба в методической печи ЛПЦ-1", fg_color="#7c7878", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, sticky="ew")
        block.grid_configure(columnspan=9)
        #------------------------------------------------
        
        #----------row=1--------------------------------- 
        self.newcell(calculation_table, row=1, column=0, text="зона")  
        self.newcell(calculation_table, row=1, column=1, text="Время наг-\nрева, мин") 
        self.newcell(calculation_table, row=1, column=2, text="T печи\nверх, °С") 
        self.newcell(calculation_table, row=1, column=3, text="T печи\nниз, °С") 
        self.newcell(calculation_table, row=1, column=4, text="Т сляба\nверх, °С") 
        self.newcell(calculation_table, row=1, column=5, text="Т сляба\nцентр, °С") 
        self.newcell(calculation_table, row=1, column=6, text="Т сляба\nниз, °С") 
  
        self.newcell(calculation_table, row=1, column=7, text="\nСредне\nмассовая\nтемпература сляба на\nвыдаче, °С", rowspan=5, sticky="nsew", wraplength=120) 
        self.newcell(calculation_table, row=1, column=8, text="\nКонечный\nперепад\nтемпературы\nпо толщине\nсляба\nна выдаче, °С", rowspan=5, sticky="nsew", wraplength=120) 
        self.newcell(calculation_table, row=1, column=9, text="\nТемпература\nраската за\nпятой\nклетью Т5,  °С", rowspan=5, sticky="nsew", wraplength=120, padx=(1,2)) 
        #---------------------------------------------------------

        #----------------------row=2------------------------------  
        self.newcell(calculation_table, row=2, column=0, text="посад") 
        self.newcell(calculation_table, row=2, column=1, text="0") 
        self.newcell(calculation_table, row=2, column=2, text=round(float(result["Методическая зона"]["tпечи, °C"].split("-")[0].strip())))
        self.newcell(calculation_table, row=2, column=3, text=round(float(result["Методическая зона"]["tниз, °C"].split("-")[0].strip())))
        self.newcell(calculation_table, row=2, column=4, text=round(heating_data["t_data"]["Температура верха печи при посаде"]))
        self.newcell(calculation_table, row=2, column=5, text=round(heating_data["t_data"]["Температура сляба при посаде"])) 
        self.newcell(calculation_table, row=2, column=6, text=round(heating_data["t_data"]["Температура низа печи при посаде"])) 
        #---------------------------------------------------------
        #----------------------row=3------------------------------ 
        self.newcell(calculation_table, row=3, column=0, text="метод.") 
        self.newcell(calculation_table, row=3, column=1, text=self.time_percent(all_time, heating_data["data"]["Время в методической зоне"])) 
        self.newcell(calculation_table, row=3, column=2, text=round(float(result["Методическая зона"]["tпечи, °C"].split("-")[1].strip())))
        self.newcell(calculation_table, row=3, column=3, text=round(float(result["Методическая зона"]["tниз, °C"].split("-")[1].strip())))
        self.newcell(calculation_table, row=3, column=4, text=round(result["Методическая зона"]["tпов1, °C"]))
        self.newcell(calculation_table, row=3, column=5, text=round(result["Методическая зона"]["Tц, °C"]))
        self.newcell(calculation_table, row=3, column=6, text=round(result["Методическая зона"]["tпов2, °C"]))
        #---------------------------------------------------------
        #----------------------row=4------------------------------ 
        self.newcell(calculation_table, row=4, column=0, text="1/2 зона") 
        self.newcell(calculation_table, row=4, column=1, text=self.time_percent(all_time, heating_data["data"]["Время в первой сварочной зоне"])) 
        self.newcell(calculation_table, row=4, column=2, text=round(float(result["Первая сварочная зона"]["tпечи, °C"].split("-")[1].strip()))) 
        self.newcell(calculation_table, row=4, column=3, text=round(float(result["Первая сварочная зона"]["tниз, °C"].split("-")[1].strip()))) 
        self.newcell(calculation_table, row=4, column=4, text=round(result["Первая сварочная зона"]["tпов1, °C"]))
        self.newcell(calculation_table, row=4, column=5, text=round(result["Первая сварочная зона"]["Tц, °C"])) 
        self.newcell(calculation_table, row=4, column=6, text=round(result["Первая сварочная зона"]["tпов2, °C"])) 
        #---------------------------------------------------------
        #----------------------row=5------------------------------ 
        self.newcell(calculation_table, row=5, column=0, text="3/4 зона") 
        self.newcell(calculation_table, row=5, column=1, text=self.time_percent(all_time, heating_data["data"]["Время во второй сварочной зоне"])) 
        self.newcell(calculation_table, row=5, column=2, text=round(result["Томильная зона"]["tпечи, °C"]))
        self.newcell(calculation_table, row=5, column=3, text=round(float(result["Первая сварочная зона"]["tниз, °C"].split("-")[1].strip())))  
        self.newcell(calculation_table, row=5, column=4, text=round(result["Вторая сварочная зона"]["tпов1, °C"])) 
        self.newcell(calculation_table, row=5, column=5, text=round(result["Вторая сварочная зона"]["Tц, °C"]))
        self.newcell(calculation_table, row=5, column=6, text=round(result["Вторая сварочная зона"]["tпов2, °C"]))
        #---------------------------------------------------------
        #----------------------row=6------------------------------
        self.newcell(calculation_table, row=6, column=0, text="5 зона")  
        self.newcell(calculation_table, row=6, column=1, text=self.time_percent(all_time, heating_data["data"]["Время в томильной зоне"])) 
        self.newcell(calculation_table, row=6, column=2, text=round(result["Томильная зона"]["tпечи, °C"])) 
        self.newcell(calculation_table, row=6, column=3, text="X") 
        self.newcell(calculation_table, row=6, column=4, text=round(result["Томильная зона"]["tпов1, °C"])) 
        self.newcell(calculation_table, row=6, column=5, text=round(result["Томильная зона"]["Tц, °C"])) 
        self.newcell(calculation_table, row=6, column=6, text=round(result["Томильная зона"]["tпов2, °C"]))

        self.newcell(calculation_table, row=6, column=7, text=result["Среднемассовая температура металла, °C"])
        self.newcell(calculation_table, row=6, column=8, text=result["Конечный перепад температур, °C"])
        self.newcell(calculation_table, row=6, column=9, text=result["Температура раската за пятой клетью (T5), °C"], padx=(1,2)) 
        #---------------------------------------------------------
        #----------------------row=7------------------------------
        hours = heating_data["График"]["время"] // 60
        remaining_minutes = heating_data["График"]["время"] % 60

        self.newcell(calculation_table, row=7, column=0, text="Всего, ч:")  
        self.newcell(calculation_table, row=7, column=1, text=f"{int(hours)}:{int(remaining_minutes):02d}") 
        self.newcell(calculation_table, row=7, column=2, text="", columnspan=3)
        self.newcell(calculation_table, row=7, column=5, text="Целевой уровень:", columnspan=2)
        self.newcell(calculation_table, row=7, column=7, text="")
        self.newcell(calculation_table, row=7, column=8, text="")
        self.newcell(calculation_table, row=7, column=9, text="", padx=(1,2))
        #--------------------------------------------------------- 

        parameters_block_top = ctk.CTkFrame(parameters, border_color="black", border_width=0, fg_color="#7c7878", corner_radius=0, bg_color="#7c7878")
        parameters_block_top.grid(row=0, column=0, pady=15, sticky="ew") 
        parameters_block_top.grid_rowconfigure(0, weight=1)
        parameters_block_top.grid_columnconfigure(0, weight=1) 
        
        block=ctk.CTkFrame(parameters_block_top, border_color="black", border_width=1, fg_color="black", corner_radius=0)
        block.grid( row=0,column=0,padx=(1,0),pady=(1,0),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Параметры сляба", fg_color="transparent", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")

        block=ctk.CTkFrame(parameters_block_top, border_color="black", border_width=1, fg_color="#494949", corner_radius=0)
        block.grid( row=0,column=1,padx=(0,1),pady=(0,1),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Масса, т", fg_color="transparent", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")

        block=ctk.CTkFrame(parameters_block_top, border_color="black", border_width=1, fg_color="#7c7878", corner_radius=0)
        block.grid( row=0,column=2,padx=(0,1),pady=(0,1),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="", fg_color="transparent", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")

        
        block=ctk.CTkFrame(parameters_block_top, border_color="black", border_width=1, fg_color="#494949", corner_radius=0)
        block.grid( row=0,column=3,padx=(0),pady=(0,1),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Ширина, м", fg_color="transparent", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")

        block=ctk.CTkFrame(parameters_block_top, border_color="black", border_width=1, fg_color="#7c7878", corner_radius=0)
        block.grid( row=0,column=4,padx=(0),pady=(0,1),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="", fg_color="transparent", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")

        
        block=ctk.CTkFrame(parameters_block_top, border_color="black", border_width=1, fg_color="#494949", corner_radius=0)
        block.grid( row=0,column=5,padx=(0,1),pady=(0,1),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Длина, м", fg_color="transparent", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")

        block=ctk.CTkFrame(parameters_block_top, border_color="black", border_width=1, fg_color="#7c7878", corner_radius=0)
        block.grid( row=0,column=6,padx=(0,1),pady=(0,1),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="", fg_color="transparent", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")
        
        block=ctk.CTkFrame(parameters_block_top, border_color="black", border_width=1, fg_color="#494949", corner_radius=0)
        block.grid( row=0,column=7,padx=(0,1),pady=(0,1),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Толщина, м", fg_color="transparent", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")

        block=ctk.CTkFrame(parameters_block_top, border_color="black", border_width=1, fg_color="#7c7878", corner_radius=0)
        block.grid( row=0,column=8,padx=(0,1),pady=(0,1),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="", fg_color="transparent", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")


        parameters_block_bottom = ctk.CTkFrame(parameters, border_color="black", border_width=0, fg_color="#7c7878", corner_radius=0, bg_color="#7c7878")
        parameters_block_bottom.grid(row=1, column=0, pady=15) 
        parameters_block_bottom.grid_rowconfigure(0, weight=1)
        parameters_block_bottom.grid_columnconfigure(0, weight=1) 
        
        block=ctk.CTkFrame(parameters_block_bottom, border_color="black", border_width=1, fg_color="#494949", corner_radius=0)
        block.grid( row=0,column=0,padx=(0,1),pady=(0,1),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Марка стали", fg_color="transparent", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")

        block=ctk.CTkFrame(parameters_block_bottom, border_color="black", border_width=1, fg_color="#7c7878", corner_radius=0)
        block.grid( row=0,column=1,padx=(0,1),pady=(0,1),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="", fg_color="transparent", corner_radius=0)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")

        
        block=ctk.CTkFrame(parameters_block_bottom, border_color="black", border_width=1, fg_color="#494949", corner_radius=0)
        block.grid( row=0,column=2,padx=(0,1),pady=(0,1),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Производительность печи, т/час", fg_color="transparent", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")

        block=ctk.CTkFrame(parameters_block_bottom, border_color="black", border_width=1, fg_color="#7c7878", corner_radius=0)
        block.grid( row=0,column=3,padx=(0,1),pady=(0,1),sticky="ew" ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="", fg_color="transparent", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")




        # block=GraphView(graph, database=self.database)
        # block.grid(row=0, column=0)

        secondblock = ctk.CTkFrame(self, fg_color="transparent")
        secondblock.grid(row=0, column=1, padx=20, sticky="n")
        secondblock.grid_rowconfigure(0, weight=1)
        secondblock.grid_columnconfigure(0, weight=1)

        title = ctk.CTkFrame(secondblock, fg_color="black")
        title.grid(row=0, column=0, sticky="ew")
        title.grid_columnconfigure(0, weight=1)
        label=ctk.CTkLabel(title, text_color="white", fg_color="transparent", text="Горение топлива", font=self.font)
        label.grid(row=0, column=0, sticky="ew")

        secondtable=ctk.CTkFrame(secondblock, fg_color="black", border_color="black", border_width=1, corner_radius=0)
        secondtable.grid(row=2, column=0, padx=1, pady=20)
 
        block=ctk.CTkFrame(secondtable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=0, padx=1, pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Состав газов", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")
        
        block=ctk.CTkFrame(secondtable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=1, padx=(0,1), pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Доля, %", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")

        block=ctk.CTkFrame(secondtable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=2, padx=(0,1), pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Калорийность", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")
        
        for row, value in enumerate(self.list):
            self.newcell(secondtable, row=row+1, column=0, text=value.name)
            self.newcell(secondtable, row=row+1, column=1, text=gas_result[row][1])
            self.newcell(secondtable, row=row+1, column=2, text="?")


        thirdtable=ctk.CTkFrame(secondblock, fg_color="black", border_color="black", border_width=1, corner_radius=0)
        thirdtable.grid(row=3, column=0, padx=1, pady=20)
 
        block=ctk.CTkFrame(thirdtable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=0, padx=(1,0), pady=1, sticky="nsew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Состав дыма", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=5, pady=0, sticky="nsew")
        
        block=ctk.CTkFrame(thirdtable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=1, padx=(0,2), pady=1, sticky="nsew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Доля, %", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=5, pady=0, sticky="nsew") 
        
        cards_dict = next(val for key, val in gas_result if key == "cards")

        for row, (gas_name, gas_value) in enumerate(cards_dict.items()):
            self.newcell(thirdtable, row=row+1, column=0, text=gas_name, fg_color="#7c7878")
            
            block=ctk.CTkFrame(thirdtable, fg_color="#7c7878", corner_radius=0)
            block.grid(
                row=row+1, 
                column=1, 
                sticky="ew",
                padx=1
                ) 
            block.grid_rowconfigure(0, weight=1)
            block.grid_columnconfigure(0, weight=1)
            cell = ctk.CTkLabel(block, text=toFixed(gas_value, 1), fg_color="#7c7878", corner_radius=0, font=self.font)
            cell.grid(row=0, column=0, padx=5, sticky="ew")


        title = ctk.CTkFrame(secondblock, fg_color="black")
        title.grid(row=4, column=0, sticky="ew", pady=20)
        title.grid_columnconfigure(0, weight=1)
        label=ctk.CTkLabel(title, text_color="white", fg_color="transparent", text="Расход топлива", font=self.font)
        label.grid(row=0, column=0, sticky="ew")
 
        fourthtable=ctk.CTkFrame(secondblock, fg_color="black", border_color="black", border_width=1, corner_radius=0)
        fourthtable.grid(row=5, column=0, padx=1)

        block=ctk.CTkFrame(fourthtable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=0, padx=1, pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Расход топлива на печь", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")
        
        block=ctk.CTkFrame(fourthtable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=1, padx=(0,1), pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="тыс.м3/ч", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")

        block=ctk.CTkFrame(fourthtable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=2, padx=(0,1), pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="тыс.м3/т", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")

        block=ctk.CTkFrame(fourthtable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=3, padx=(0,1), pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="пр.тыс.м3/т", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")

        block=ctk.CTkFrame(fourthtable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=4, padx=(0,1), pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="кг/т", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")
        
        for row, value in enumerate(self.list):
            self.newcell(fourthtable, row=row+1, column=0, text=value.name)
            self.newcell(fourthtable, row=row+1, column=1, text="?")
            self.newcell(fourthtable, row=row+1, column=2, text="?")
            self.newcell(fourthtable, row=row+1, column=3, text="?")
            self.newcell(fourthtable, row=row+1, column=4, text="?")
            
            
        lasttable=ctk.CTkFrame(secondblock, fg_color="black", border_color="black", border_width=1, corner_radius=0)
        lasttable.grid(row=6, column=0, padx=(1,0), pady=20)
 
        block=ctk.CTkFrame(lasttable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=0, padx=(1,0), pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Расход топлива по зонам", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")
        
        block=ctk.CTkFrame(lasttable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=1, padx=(0), pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="м3/ч", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")

        block=ctk.CTkFrame(lasttable, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=2, padx=(1,0), pady=(1,2), sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="доля, %", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")
        
        zonedata = result["Расход топлива по зонам:"]
        zonelist = ["в первой сварочной зоне", "в зоне нижнего подогрева 2", "во второй сварочной зоне", "в зоне нижнего подогрева 4", "в томильной зоне"]
        for i, row in enumerate(zonelist):
            self.newcell(lasttable, row=i+1, column=0, text=i+1)
            self.newcell(lasttable, row=i+1, column=1, text=zonedata[f"{row}, тыс. м³/час"])
            self.newcell(lasttable, row=i+1, column=2, text=zonedata[f"{row}, %"])
            
            
        lastrow=ctk.CTkFrame(secondblock, fg_color="black", border_color="black", border_width=1, corner_radius=0)
        lastrow.grid(row=7, column=0, padx=1, pady=20)
        
        block=ctk.CTkFrame(lastrow, fg_color="#494949", corner_radius=0)
        block.grid( row=0, column=0, padx=1, pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="Удельный расход условного топлива", fg_color="#494949", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")
        
        block=ctk.CTkFrame(lastrow, fg_color="#7c7878", corner_radius=0)
        block.grid( row=0, column=1, padx=0, pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text=result["Удельный расход условного топлива, кг у.т. /т"], fg_color="#7c7878", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")

        block=ctk.CTkFrame(lastrow, fg_color="#7c7878", corner_radius=0)
        block.grid( row=0, column=2, padx=(1,2), pady=1, sticky="ew") 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text="кг у.т./т", fg_color="#7c7878", corner_radius=0, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=0, sticky="ew")

    def newcell(self, table, row, column, text, columnspan=0, rowspan=0, sticky="ew", wraplength=0, border_color="black", border_width=0, fg_color="#7c7878", padx=0):
        block=ctk.CTkFrame(table, border_color=border_color, border_width=border_width, fg_color=fg_color, corner_radius=0)
        if padx==0:
            padx = ((1,0) if column == 0 or column == 1 else (1,1))
        block.grid(
            row=row, 
            column=column, 
            padx=padx, 
            pady=((1,0) if row == 0 else (0,1)), 
            sticky=sticky
            ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        cell = ctk.CTkLabel(block, text=text, fg_color="transparent", corner_radius=0, wraplength=wraplength, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")
        if(columnspan > 0):
            block.grid_configure(columnspan=columnspan)
        if(rowspan > 0):
            block.grid_configure(rowspan=rowspan)


    def time_percent(self, all_time, current_time):
        return round(float((current_time / all_time) * 100), 2)
    