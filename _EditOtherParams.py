import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from utilities import toFixed

class EditOtherParams(ctk.CTkToplevel):
    def __init__(self, master, database, title="New Window", size="550x300"):
        super().__init__(master)
        self.database = database

        width = 1024
        height = 930
        spawn_x = int((self.winfo_screenwidth() - width) / 2)
        spawn_y = int((self.winfo_screenheight() - height) / 2)

        self.geometry(f"{width}x{height}+{spawn_x}+{spawn_y}")
        self.title("Редактирование прочих параметров")

        self.label = ctk.CTkLabel(self, text="Редактирование прочих параметров", font=ctk.CTkFont(size=18, weight="bold"))
        self.label.grid(row=0, column=0, columnspan=4, sticky="NSEW", pady=10)

        self.columnconfigure((0, 1, 2, 3), weight=1)
        self.text_boxes = {}
        self.furnace_params = {
            "Геометрические параметры": {
                "Длина печи (Lp), м": toFixed(database.get_parameters("Длина печи (Lp)").value, 3)
            },
            "Теплоизоляция труб сио": {
                "Толщина первого слоя (dst1), м": toFixed(database.get_parameters("Толщина первого слоя (dst1)").value, 3),
                "Толщина второго слоя (dst2), м": toFixed(database.get_parameters("Толщина второго слоя (dst2)").value, 3),
                "Внутренний радиус трубы (r1), м": toFixed(database.get_parameters("Внутренний радиус трубы (r1)").value, 3),
                "Внешний радиус трубы (r2), м": toFixed(database.get_parameters("Внешний радиус трубы (r2)").value, 3),
                "Радиус теплоизоляции (r3), м": toFixed(database.get_parameters("Радиус теплоизоляции (r3)").value, 3)
            },
            "Температурные параметры": {
                "Температура окружающей среды (toc), °C": toFixed(database.get_parameters("Температура окружающей среды (toc)").value, 3),
                "Температура насыщения (tnas), °C": toFixed(database.get_parameters("Температура насыщения (tnas)").value, 3),
                "Разница температур при посаде (twDif), °C": toFixed(database.get_parameters("Разница температур при посаде (twDif)").value, 3),
                "Температура методической зоны (twMetn), °C": toFixed(database.get_parameters("Температура методической зоны (twMetn)").value, 3),
                "Допустимый перепад (dtdop), °C": toFixed(database.get_parameters("Допустимый перепад (dtdop)").value, 3),
            },
            "Другие параметры": {
                "Количество узлов (n-нечётное), кол.": toFixed(database.get_parameters("Количество узлов (n)").value, 0),
                "Время в методической зоне, %": toFixed(database.get_parameters("Время в методической зоне").value, 3),
                "Время в первой сварочной зоне, %": toFixed(database.get_parameters("Время в первой сварочной зоне").value, 3),
                "Время во второй сварочной зоне, %": toFixed(database.get_parameters("Время во второй сварочной зоне").value, 3),
                "Время в томильной зоне, %": toFixed(database.get_parameters("Время в томильной зоне").value, 3),
            },
            "Площадь футеровки по зонам": {
                "Методическая зона (Fmet), м²": toFixed(database.get_parameters("Методическая зона (Fmet)").value, 3),
                "Первая сварочная зона (Fsv1), м²": toFixed(database.get_parameters("Первая сварочная зона (Fsv1)").value, 3),
                "Вторая сварочная зона (Fsv2), м²": toFixed(database.get_parameters("Вторая сварочная зона (Fsv2)").value, 3),
                "Томильная зона (Ftom), м²": toFixed(database.get_parameters("Томильная зона (Ftom)").value, 3),
                "Суммарная длина труб СИО в методической зоне (LsioMet), м": toFixed(database.get_parameters("Суммарная длина труб СИО в методической зоне (LsioMet)").value, 3),
                "Суммарная длина труб СИО в первой сварочной зоне (LsioSv1), м": toFixed(database.get_parameters("Суммарная длина труб СИО в первой сварочной зоне (LsioSv1)").value, 3),
                "Суммарная длина труб СИО во второй зоне (LsioSv2), м": toFixed(database.get_parameters("Суммарная длина труб СИО во второй зоне (LsioSv2)").value, 3),
                "Суммарная длина труб СИО в томильной зоне (LsioTom), м": toFixed(database.get_parameters("Суммарная длина труб СИО в томильной зоне (LsioTom)").value, 3),
                "Сохранность футеровки СИО, %": toFixed(database.get_parameters("Сохранность футеровки СИО").value, 0)
            }
        }

        self.init_ui()
        self.lift()           # Bring window to front
        self.focus_force()    # Focus on this window
        self.grab_set()       # Make modal (optional)

    def init_ui(self):
        row_counter = 1
        col_counter = 0

        geo_label = ctk.CTkLabel(self, text="Геометрические параметры", font=ctk.CTkFont(size=14, weight="bold"))
        geo_label.grid(row=row_counter, column=col_counter, columnspan=2, sticky="NSEW", pady=(10, 5), padx=10)

        row_counter += 1

        for key, value in self.furnace_params["Геометрические параметры"].items():
            list_item = ctk.CTkLabel(self, text=key, font=ctk.CTkFont(size=12))
            list_item.grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="E")

            list_item_text_box = ctk.CTkEntry(self, height=25, width=120)
            list_item_text_box.grid(row=row_counter, column=col_counter + 1, padx=10, pady=5, sticky="W")
            list_item_text_box.insert(0, str(value))
            self.text_boxes[key] = list_item_text_box

            row_counter += 1


        row_counter = 1
        col_counter = 2
        
        temp_label = ctk.CTkLabel(self, text="Теплоизоляция труб сио", font=ctk.CTkFont(size=14, weight="bold"))
        temp_label.grid(row=row_counter, column=col_counter, columnspan=2, sticky="NSEW", pady=(10, 5), padx=10)
        
        row_counter += 1

        for key, value in self.furnace_params["Теплоизоляция труб сио"].items():
            list_item = ctk.CTkLabel(self, text=key, font=ctk.CTkFont(size=12))
            list_item.grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="E")

            list_item_text_box = ctk.CTkEntry(self, height=25, width=120)
            list_item_text_box.grid(row=row_counter, column=col_counter + 1, padx=(0,10), pady=5, sticky="W")
            list_item_text_box.insert(0, str(value))
            self.text_boxes[key] = list_item_text_box

            row_counter += 1

        row_counter = len(self.furnace_params["Теплоизоляция труб сио"]) + 2
        col_counter = 2
        
        temp_label = ctk.CTkLabel(self, text="Площадь футеровки по зонам", font=ctk.CTkFont(size=14, weight="bold"))
        temp_label.grid(row=row_counter, column=col_counter, columnspan=2, sticky="NSEW", pady=(10, 5), padx=10)
        
        row_counter += 1

        for key, value in self.furnace_params["Площадь футеровки по зонам"].items():
            list_item = ctk.CTkLabel(self, text=key, font=ctk.CTkFont(size=12))
            list_item.grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="E")

            list_item_text_box = ctk.CTkEntry(self, height=25, width=120)
            list_item_text_box.grid(row=row_counter, column=col_counter + 1, padx=(0,10), pady=5, sticky="W")
            list_item_text_box.insert(0, str(value))
            self.text_boxes[key] = list_item_text_box

            row_counter += 1


        row_counter = len(self.furnace_params["Геометрические параметры"]) + 2
        col_counter = 0
        
        t_iso_label = ctk.CTkLabel(self, text="Температурные параметры", font=ctk.CTkFont(size=14, weight="bold"))
        t_iso_label.grid(row=row_counter, column=col_counter, columnspan=2, sticky="NSEW", pady=(10, 5), padx=10)
        
        row_counter += 1

        for key, value in self.furnace_params["Температурные параметры"].items():
            list_item = ctk.CTkLabel(self, text=key, font=ctk.CTkFont(size=12))
            list_item.grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="E")

            list_item_text_box = ctk.CTkEntry(self, height=25, width=120)
            list_item_text_box.grid(row=row_counter, column=col_counter + 1, padx=10, pady=5, sticky="W")
            list_item_text_box.insert(0, f"{float(value):.0f}")
            self.text_boxes[key] = list_item_text_box

            row_counter += 1

        
        row_counter = len(self.furnace_params["Геометрические параметры"]) + len(self.furnace_params["Теплоизоляция труб сио"]) + 3
        col_counter = 0
        
        t_iso_label = ctk.CTkLabel(self, text="Другие параметры", font=ctk.CTkFont(size=14, weight="bold"))
        t_iso_label.grid(row=row_counter, column=col_counter, columnspan=2, sticky="NSEW", pady=(10, 5), padx=10)
        
        row_counter += 1

        for key, value in self.furnace_params["Другие параметры"].items():
            list_item = ctk.CTkLabel(self, text=key, font=ctk.CTkFont(size=12))
            list_item.grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="E")

            list_item_text_box = ctk.CTkEntry(self, height=25, width=120)
            list_item_text_box.grid(row=row_counter, column=col_counter + 1, padx=10, pady=5, sticky="W")
            list_item_text_box.insert(0, str(value))
            self.text_boxes[key] = list_item_text_box

            row_counter += 1

        
        row_counter = len(self.furnace_params["Температурные параметры"]) + len(self.furnace_params["Площадь футеровки по зонам"]) + 3

        # Кнопки "Подтвердить" и "Отменить"
        confirm_button = ctk.CTkButton(self, text="Подтвердить", width=160, fg_color='#699187', hover_color='#84a59d', text_color='black',
                                                 font=ctk.CTkFont(size=12, weight="bold"), command=self.confirm)
        confirm_button.grid(row=row_counter, column=0, columnspan=2, pady=20)

        cancel_button = ctk.CTkButton(self, text="Отменить", width=160, fg_color='#ed5855', hover_color='#f28482', text_color='black',
                                                font=ctk.CTkFont(size=12, weight="bold"), command=self.close_window)
        cancel_button.grid(row=row_counter, column=2, columnspan=2, pady=20)
        
    def close_window(self):
        self.destroy()

    def confirm(self):
        data = {}
        try:
            for key, entry in self.text_boxes.items():
                value = entry.get()
                try:
                    data[key] = float(value)
                except ValueError:
                    raise ValueError(f"Значение '{key}' должно быть числом!")


            # Обновляем базу данных параметров печи
            self.database.update_furnace_params(data)

            self.close_window()

        except Exception as ex:
            CTkMessagebox(title="Ошибка!", message=str(ex), icon="cancel")