import customtkinter as ctk

class HeatBalance(ctk.CTkFrame):
    def __init__(self, master, root, database, **kwargs):
        super().__init__(master, **kwargs)
        
        self.font=ctk.CTkFont(size=13, weight="bold")
        self.view_data = "MВт"
        
    def update(self, heating_data):
        table = ctk.CTkFrame(self, fg_color="black", border_color="black", border_width=2)
        table.grid(row=0, column=0)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=0, column=1, padx=15, sticky="nsew")
        
        button = ctk.CTkButton(button_frame, text="МВт/%", fg_color="red", text_color="white", corner_radius=0, font=self.font, command=self.change)
        button.grid(row=0,column=0)
        
        table.grid_rowconfigure(0, weight=1)
        table.grid_columnconfigure(0, weight=1)

        self.result = heating_data["Тепловой баланс"]

        self.newcell(table, 0, 0, "Расчет теплового баланса печи, МВт(%)", columnspan=9)

        self.newcell(table, 1, 0, "")
        self.newcell(table, 1, 1, "На печь")
        self.newcell(table, 1, 2, "метод.\nВерх")
        self.newcell(table, 1, 3, "метод.\nНиз")
        self.newcell(table, 1, 4, "1 зона")
        self.newcell(table, 1, 5, "2 зона")
        self.newcell(table, 1, 6, "3 зона")
        self.newcell(table, 1, 7, "4 зона")
        self.newcell(table, 1, 8, "5 зона")

        self.newcell(table, 2, 0, "Приход тепла", columnspan=9)

        self.newcell(table, 3, 0, "Химическое тепло топлива")
        self.newcell(table, 4, 0, "Физическое тепло воздуха")
        self.newcell(table, 5, 0, "Физическое тепло газа")
        self.newcell(table, 6, 0, "Тепло транзитных газов")
        self.newcell(table, 7, 0, "Итого приход")
        
        self.newcell(table, 8, 0, "Расход тепла", columnspan=9)
        
        self.newcell(table, 9, 0, "Тепло на нагрев металла")
        self.newcell(table, 10, 0, "Потери через кладку")
        self.newcell(table, 11, 0, "Тепло уходящее с дымом")
        self.newcell(table, 12, 0, "Потери через СИО")
        self.newcell(table, 13, 0, "Потери излучением ч/з окна")
        self.newcell(table, 14, 0, "Итого расход")
        self.newcell(table, 15, 0, "Расход топлива, тыс. м3/ч")
        
        self.newcell(table, 3, 1, text="", value="Тепловой баланс печи|Приход тепла|Химическое тепло топлива")
        self.newcell(table, 4, 1, "", value="Тепловой баланс печи|Приход тепла|Физическое тепло воздуха")
        self.newcell(table, 5, 1, "", value="Тепловой баланс печи|Приход тепла|Физическое тепло газа")
        self.newcell(table, 6, 1, "",)
        self.newcell(table, 7, 1, "", value="Тепловой баланс печи|Приход тепла|Итого приход")

        self.newcell(table, 9, 1, "", value="Тепловой баланс печи|Расход тепла|Тепло на нагрев металла")
        self.newcell(table, 10, 1, "", value="Тепловой баланс печи|Расход тепла|Потери через кладку")
        self.newcell(table, 11, 1, "", value="Тепловой баланс печи|Расход тепла|Тепло уходящее с дымом")
        self.newcell(table, 12, 1, "", value="Тепловой баланс печи|Расход тепла|Потери через СИО")
        self.newcell(table, 13, 1, "", value="Тепловой баланс печи|Расход тепла|Потери излучением ч/з окна")
        self.newcell(table, 14, 1, "", value="Тепловой баланс печи|Расход тепла|Итого расход")
        self.newcell(table, 15, 1, "", value="Тепловой баланс печи|Расход топлива, тыс. м³/час") # НА ПЕЧЬ Расход топлива, тыс. м3/ч

        self.newcell(table, 3, 2, "")
        self.newcell(table, 4, 2, "")
        self.newcell(table, 5, 2, "")
        self.newcell(table, 6, 2, "", value="Методическая зона верх|Приход тепла|Тепло транзитных газов")
        self.newcell(table, 7, 2, "", value="Методическая зона верх|Приход тепла|Итого приход")

        self.newcell(table, 9, 2, "", value="Методическая зона верх|Расход тепла|Тепло на нагрев металла")
        self.newcell(table, 10, 2, "", value="Методическая зона верх|Расход тепла|Потери через кладку")
        self.newcell(table, 11, 2, "")
        self.newcell(table, 12, 2, "", value="Методическая зона верх|Расход тепла|Потери через СИО")
        self.newcell(table, 13, 2, "", value="Методическая зона верх|Расход тепла|Потери через окно посада")
        self.newcell(table, 14, 2, "", value="Методическая зона верх|Расход тепла|Итого расход")
        self.newcell(table, 15, 2, "")

        self.newcell(table, 3, 3, "")
        self.newcell(table, 4, 3, "")
        self.newcell(table, 5, 3, "")
        self.newcell(table, 6, 3, "", value="Методическая зона низ|Приход тепла|Тепло транзитных газов")
        self.newcell(table, 7, 3, "", value="Методическая зона низ|Приход тепла|Итого приход")

        self.newcell(table, 9, 3, "", value="Методическая зона низ|Расход тепла|Тепло на нагрев металла")
        self.newcell(table, 10, 3, "", value="Методическая зона низ|Расход тепла|Потери через кладку")
        self.newcell(table, 11, 3, "")
        self.newcell(table, 12, 3, "", value="Методическая зона низ|Расход тепла|Потери через СИО")
        self.newcell(table, 13, 3, "", value="Методическая зона низ|Расход тепла|Потери через окно посада")
        self.newcell(table, 14, 3, "", value="Методическая зона низ|Расход тепла|Итого расход")
        self.newcell(table, 15, 3, "")

        self.newcell(table, 3, 4, "")
        self.newcell(table, 4, 4, "")
        self.newcell(table, 5, 4, "")
        self.newcell(table, 6, 4, "")
        self.newcell(table, 7, 4, "")

        self.newcell(table, 9, 4, "")
        self.newcell(table, 10, 4, "")
        self.newcell(table, 11, 4, "")
        self.newcell(table, 12, 4, "")
        self.newcell(table, 13, 4, "")
        self.newcell(table, 14, 4, "")
        self.newcell(table, 15, 4, "")

        self.newcell(table, 3, 5, "")
        self.newcell(table, 4, 5, "")
        self.newcell(table, 5, 5, "")
        self.newcell(table, 6, 5, "")
        self.newcell(table, 7, 5, "")

        self.newcell(table, 9, 5, "")
        self.newcell(table, 10, 5, "")
        self.newcell(table, 11, 5, "")
        self.newcell(table, 12, 5, "")
        self.newcell(table, 13, 5, "")
        self.newcell(table, 14, 5, "")
        self.newcell(table, 15, 5, "")

        self.newcell(table, 3, 6, "")
        self.newcell(table, 4, 6, "")
        self.newcell(table, 5, 6, "")
        self.newcell(table, 6, 6, "")
        self.newcell(table, 7, 6, "")

        self.newcell(table, 9, 6, "")
        self.newcell(table, 10, 6, "")
        self.newcell(table, 11, 6, "")
        self.newcell(table, 12, 6, "")
        self.newcell(table, 13, 6, "")
        self.newcell(table, 14, 6, "")
        self.newcell(table, 15, 6, "")

        self.newcell(table, 3, 7, "")
        self.newcell(table, 4, 7, "")
        self.newcell(table, 5, 7, "")
        self.newcell(table, 6, 7, "")
        self.newcell(table, 7, 7, "")
        self.newcell(table, 9, 7, "")
        self.newcell(table, 10, 7, "")
        self.newcell(table, 11, 7, "")
        self.newcell(table, 12, 7, "")
        self.newcell(table, 13, 7, "")
        self.newcell(table, 14, 7, "")
        self.newcell(table, 15, 7, "")

        self.newcell(table, 3, 8, "")
        self.newcell(table, 4, 8, "")
        self.newcell(table, 5, 8, "")
        self.newcell(table, 6, 8, "")
        self.newcell(table, 7, 8, "")
        self.newcell(table, 9, 8, "")
        self.newcell(table, 10,8, "")
        self.newcell(table, 11, 8, "")
        self.newcell(table, 12, 8, "")
        self.newcell(table, 13, 8, "")
        self.newcell(table, 14, 8, "")
        self.newcell(table, 15, 8, "")

    def newcell(self, table, row, column, text, value = "", columnspan=0, rowspan=0, sticky="ew", wraplength=0, border_color="black", border_width=0, fg_color="#7c7878"):
        block=ctk.CTkFrame(table, border_color=border_color, border_width=border_width, fg_color=fg_color, corner_radius=0)
        block.grid(
            row=row, 
            column=column, 
            padx=((1,0) if column == 0 else (0,1)), 
            pady=((1,1) if row == 0 else (0,1)), 
            sticky=sticky
            ) 
        block.grid_rowconfigure(0, weight=1)
        block.grid_columnconfigure(0, weight=1)
        label_text = text
        if len(value) > 0:
            path = value.split("|")
            if "," in value:
                label_text = self.result[path[0]][path[1]]
            else:    
                label_text = self.result[path[0]][path[1]][f"{path[2]}, {self.view_data}"]
            
        cell = ctk.CTkLabel(block, 
                            text=label_text,
                            fg_color="transparent", corner_radius=0, wraplength=wraplength, font=self.font)
        cell.grid(row=0, column=0, padx=15, pady=1, sticky="ew")
        if(columnspan > 0):
            block.grid_configure(columnspan=columnspan)
        if(rowspan > 0):
            block.grid_configure(rowspan=rowspan)

    def change(self):
        self.view_data = "%" if self.view_data == "MВт" else "MВт"
        print(self.view_data)
        # self.update()