from CTkMessagebox import CTkMessagebox
import customtkinter as ctk

from utilities import toFixed

class EditSlabs(ctk.CTkToplevel):
    def __init__(self, master, database, title="New Window", size="550x300"):
        super().__init__(master)
        self.resizable(False, False)
        self.database = database
        self.text_boxes = {}
        self.title(title)
        self.geometry(size)
        self.furnace_params = {
            "Геометрические параметры": {
                "Толщина сляба (s), м": toFixed(float(database.get_parameters("Толщина сляба (s)").value), 3),
                "Длина сляба (bb), м": toFixed(float(database.get_parameters("Длина сляба (bb)").value), 3),
                "Ширина сляба (a), м": toFixed(float(database.get_parameters("Ширина сляба (a)").value), 3),
                "Начальная температура металла (tmn), °C": toFixed(float(database.get_parameters("Начальная температура металла (tmn)").value), 3),
                "Марка стали (группа нагрева)": [
                    "08, 10, 3кп (1)",
                    "15, 25, 35 (2)",
                    "45, 17Г1С4 (3)",
                    # "DX51D (1)",
                    # "08кп, 08пс (1)",
                    # "10кп (1)",
                    # "3кп,3пс, S235JR (1)",
                    # "15 (2)",
                    # "20 (2)",
                    # "25 (2)",
                    # "35 (2)",
                    # "45 (3)",
                    # "17Г1С4 (3)",
                    # "10ХНДП(3)",
                    # "09Г2С(38Х2МЮА) (3)",
                ]
            },
        }

        self.init_ui()
        self.lift()           # Bring window to front
        self.focus_force()    # Focus on this window
        self.grab_set()       # Make modal (optional)


    def init_ui(self):
        row_counter = 1
        col_counter = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        geo_label = ctk.CTkLabel(self, text="Редактирование параметров сляба", font=ctk.CTkFont(size=14, weight="bold"))
        geo_label.grid(row=row_counter, column=col_counter, columnspan=2, sticky="NSEW", pady=(10, 5), padx=10)

        row_counter += 1

        for key, value in self.furnace_params["Геометрические параметры"].items():
            list_item = ctk.CTkLabel(self, text=key, font=ctk.CTkFont(size=12))
            list_item.grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="E")

            if isinstance(value, list):
                combo = ctk.CTkComboBox(self, values=value, width=200, state="readonly")
                combo.grid(row=row_counter, column=col_counter + 1, padx=10, pady=5, sticky="W")
                combo.set(value[0])
                self.text_boxes[key] = combo  # сохраняем combo
            else:
                entry = ctk.CTkEntry(self, height=25, width=120)
                entry.grid(row=row_counter, column=col_counter + 1, padx=10, pady=5, sticky="W")
                entry.insert(0, str(value))
                self.text_boxes[key] = entry  # сохраняем entry
            
            row_counter += 1

    # Кнопки "Подтвердить" и "Отменить"
        confirm_button = ctk.CTkButton(self, text="Подтвердить", width=160, fg_color='#699187', hover_color='#84a59d', text_color='black',
                                                 font=ctk.CTkFont(size=12, weight="bold"), command=self.confirm)
        confirm_button.grid(row=row_counter, column=0, pady=20, padx=20)

        cancel_button = ctk.CTkButton(self, text="Отменить", width=160, fg_color='#ed5855', hover_color='#f28482', text_color='black',
                                                font=ctk.CTkFont(size=12, weight="bold"), command=self.close_window)
        cancel_button.grid(row=row_counter, column=1, pady=20)


    
    def close_window(self):
        self.destroy()

    def confirm(self):
        data = {} 
        for key, entry in self.text_boxes.items():
            value = entry.get()  
            try:
                if key == "Марка стали (группа нагрева)":
                    data[key] = str(value)
                else:
                    data[key] = float(value)
            except ValueError:
                raise ValueError(f"Значение '{key}' должно быть числом!")

        # Обновляем базу данных параметров печи
         
        self.database.update_furnace_params(data)

        self.close_window()

        # except Exception as ex:
        #     print(ex)
        #     CTkMessagebox(title="Ошибка!", message=str(ex), icon="cancel")

    