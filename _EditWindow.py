import customtkinter
from CTkMessagebox import CTkMessagebox 

list_data = {
    "Undefined": {
        'CH4': ("%", 90.087),
        'C2H4': ("%", 0),
        'C2H6': ("%", 5.93),
        'C3H8': ("%", 1.64),
        'C4H10': ("%", 0.323),
        'C5H12': ("%", 0.036),
        'CO': ("%", 0),
        'H2': ("%", 0),
        'CO2': ("%", 0.199),
        'N2': ("%", 1.77),
        'O2': ("%", 0.015),
        'd': ("г/м³", 10),
        'Стоимость': ("тг/1000м³", 0),
    }
}

class EditWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__()
        
        # Сохраняем состояние родителя
        self.parent = args[0]

        width = 480
        height = 760
        spawn_x = int((self.winfo_screenwidth()-width)/2) 
        spawn_y = int((self.winfo_screenheight()-height)/2)

        self.geometry(f"{width}x{height}+{spawn_x}+{spawn_y}")

        self.grab_set()
        self.transient(self.parent)
        self.focus_force()    # Focus on this window

#TODO: Переработать добавление
        if args[1] is None:
            self.data_index = "Undefined"
            self.title("Форма добавления газа")
            self.label = customtkinter.CTkLabel(self, text="Добавить газ", font=customtkinter.CTkFont(size=18, weight="bold"))
        else:
            self.data_index = args[1]
            self.title("Форма редактирования газа")
            self.label = customtkinter.CTkLabel(self, text="Редактировать газ", font=customtkinter.CTkFont(size=18, weight="bold"))

        self.database = args[2]

        self.label.grid(row=0, column=0, columnspan=2, sticky="NESW",pady=(20, 5))
        self.columnconfigure((0, 1), weight=1)

        row_counter = 1

        self.text_boxes = []

        # Ввод названия газа
        list_item = customtkinter.CTkLabel(self, text="Название:", font=customtkinter.CTkFont(size=12, weight="bold"))
        list_item.grid(row=row_counter, column=0, padx=10, pady=10)
        
        # Значение по умолчанию
        if(self.data_index == "Undefined"):
            list_item_text_box = customtkinter.CTkEntry(self, height=20, width=160, state='normal')
            list_item_text_box.grid(row=row_counter, column=1, padx=(10,0), pady=5)
            list_item_text_box.insert(0, "")
            self.text_boxes.append(("Название", list_item_text_box))
            
            row_counter += 1

            # Вывод всех элементов состава газа
            for row, (key, value) in enumerate(list_data["Undefined"].items()):
                list_item = customtkinter.CTkLabel(self, text=key + ", " + value[0] + " :", font=customtkinter.CTkFont(size=12, weight="bold"))
                list_item.grid(row=row_counter, column=0, padx=10, pady=5)
                list_item_text_box = customtkinter.CTkEntry(self, height=20, width=160)
                list_item_text_box.grid(row=row_counter, column=1, padx=(10, 0), pady=5)
                list_item_text_box.insert(0, value[1])
                self.text_boxes.append((key, list_item_text_box))
                row_counter += 1

            # # Процентный состав данного газа в смешанном газе
            # list_item = customtkinter.CTkLabel(self, text="Процентный состав:", font=customtkinter.CTkFont(size=12, weight="bold"))
            # list_item.grid(row=row_counter, column=0, padx=10, pady=10)
            # list_item_text_box = customtkinter.CTkEntry(self, height=20, width=160)
            # list_item_text_box.grid(row=row_counter, column=1, padx=(10,0), pady=5)
            # list_item_text_box.insert(0, "20")
            # self.text_boxes.append(("Процентный состав", list_item_text_box))
        else:
            list_item_text_box = customtkinter.CTkEntry(self, height=20, width=160, state='normal')
            list_item_text_box.insert(0, self.data_index.name)
            list_item_text_box.grid(row=row_counter, column=1, padx=(10,0), pady=5)
            self.text_boxes.append(("Название", list_item_text_box))

            row_counter += 1

            # Вывод всех элементов состава газа
            for row, e in enumerate(self.data_index.components):
                list_item = customtkinter.CTkLabel(self, text=e.component + ", " + e.units + " :", font=customtkinter.CTkFont(size=12, weight="bold"))
                list_item.grid(row=row_counter, column=0, padx=10, pady=5)
                list_item_text_box = customtkinter.CTkEntry(self, height=20, width=160)
                list_item_text_box.grid(row=row_counter, column=1, padx=(10, 0), pady=5)
                list_item_text_box.insert(0, e.value)
                self.text_boxes.append((e.component, list_item_text_box))
                row_counter += 1

            # # Процентный состав данного газа в смешанном газе
            # list_item = customtkinter.CTkLabel(self, text="Процентный состав:", font=customtkinter.CTkFont(size=12, weight="bold"))
            # list_item.grid(row=row_counter, column=0, padx=10, pady=10)
            # list_item_text_box = customtkinter.CTkEntry(self, height=20, width=160)
            # list_item_text_box.grid(row=row_counter, column=1, padx=(10,0), pady=5)

            # if("Доменный газ" not in self.data_index.name):
            #     list_item_text_box.insert(0, self.data_index.mixed_percentage)
            # else:
            #     list_item_text_box.insert(0, self.database.get_percentage())
            #     list_item_text_box.configure(state="disabled")
            
            # self.text_boxes.append(("Процентный состав", list_item_text_box))

        row_counter += 1

        # Кнопки добавить/отменить
        confirm_button = customtkinter.CTkButton(self, text="Подтвердить", width=160, fg_color='#699187', hover_color='#84a59d', text_color='black', font=customtkinter.CTkFont(size=12, weight="bold"), command=self.confirm)
        confirm_button.grid(row=row_counter, column=0, padx=(0,10), pady=(20, 0))

        cancel_button = customtkinter.CTkButton(self, text="Отменить",  width=160, fg_color='#ed5855', hover_color='#f28482', text_color='black', font=customtkinter.CTkFont(size=12, weight="bold"), command=self.close_window)
        cancel_button.grid(row=row_counter, column=1, padx=(10,0), pady=(20, 0))


    def close_window(self):
        self.destroy()

    def confirm(self):
        data = {}

        try:
            for row, (name, val) in enumerate(self.text_boxes):
                res = val.get()
                name = name.split(",")[0]

                if(row > 0):
                    try:
                        res = float(res)
                    except:
                        raise ValueError(f"Значение поля '{name}' имеет неверный ввод!")
                else:
                    if(res == ""):
                        raise ValueError(f"Вы не ввели название газа")
                    
                if('Процентный состав' in name):
                    if(res > 100):
                        raise ValueError(f"Значение поля '{name}' более 100 %")
                    elif(res < 0):
                        raise ValueError(f"Значение поля '{name}' не может быть отрицательным")

                data[name] = res
                
            self.database.update_gases(data)

            self.parent.update_list()

            self.close_window()

        except Exception as ex:
            CTkMessagebox(title="Ошибка!", message=ex, icon="cancel")