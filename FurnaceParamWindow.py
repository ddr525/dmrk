import customtkinter
from CTkMessagebox import CTkMessagebox

from utilities import toFixed 

class FurnaceParamWindow(customtkinter.CTkToplevel):
    def __init__(self, database, page, *args, **kwargs):
        super().__init__()

        self.page = page
        self.database = database

        width = 1024
        height = 930
        spawn_x = int((self.winfo_screenwidth() - width) / 2)
        spawn_y = int((self.winfo_screenheight() - height) / 2)

        self.geometry(f"{width}x{height}+{spawn_x}+{spawn_y}")
        self.title("Редактирование параметров печи")

        self.label = customtkinter.CTkLabel(self, text="Редактирование параметров печи", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.label.grid(row=0, column=0, columnspan=4, sticky="NSEW", pady=10)

        self.columnconfigure((0, 1, 2, 3), weight=1)

        self.text_boxes = {}

        # dtdop = 318 # Допустимый перепад
        # n = 10      # Количество узлов
        # s = 0.200   # Толщина сляба м
        # bb = 9.1    # Длина сляба м
        # a = 1.250   # Ширина сляба м

        # toc = 20 # Т окружающей среды

        # # Параметры футировки
        # dst1 = 0.464  # Толщина первой стены, м
        # dst2 = 0.115  # Толщина второй стены, м
        # tnas = 180 # температура насыщения при P=10 МПа
        # r2 = 0.146 / 2   # наружний радиус трубы
        # r1 = r2 - 0.030  # внутренний радиус трубы
        # r3 = r2 + 0.0132 # диаметр теплоизоляции

        # time_H = 240 # Время нагрева в мин

        # tMet_per = 0.1784 * 100 # время в процентах методическая зона
        # tSv1_per = 0.2826 * 100 # время в процентах первая сварочная зона
        # tSv2_per = 0.2944 * 100 # время в процентах во второй зоне
        # tTom_per = 0.2446 * 100 # время в процентах в томильной зоне

        # tmn = 20 # Начальная температура металла
        # twDif = 50 # Разница тепмператур при посаде

        # twMetn = 1050    # температура методической зоны
        # twMetNpk = 1100; # температура нижней подогрева методической зоны

        # twSv1n = 1300    # температура первой сварочной зоны

        # twSv2  = 1350    # температура второй сварочной зоны
        # twNp2k = 1250  # температура нижнего подогрева второй сварочной зоны

        # twTom  = 1280    # температура томильной зоны
        
        # twNp2n = 1250 # температура нижнего подогрева томильной зоны
        
        # Lp = 35.544 # Длина печи
        
        # # Площадь футеровки по зонам
        # Fmet = 31.05+35.99  # методическая зона
        # Fsv1 = 54.88+49.69  # первая сварочная зона
        # Fsv2 = 92.7+63.4    # во второй зоне
        # Ftom = 41.63+51.65  # в томильной зоне

        # LsioMet = 2*4*Lp*0.189+6.708*2*2 # Суммарная длина труб СИО в методической зон, м
        # LsioSv1 = 4*Lp*0.245+6.708*2*3   # Суммарная длина труб СИО в первой сварочной зоне, м
        # LsioSv2 = 4*Lp*0.312+6.708*2*4   # Суммарная длина труб СИО во второй зоне, м
        # LsioTom = 4*Lp*0.254+6.708*2*2   # Суммарная длина труб СИО в томильной зоне, м

        furnace_params = {
            "Геометрические параметры": {
                "Толщина сляба (s), м": toFixed(database.get_parameters("Толщина сляба (s)").value, 3),
                "Длина сляба (bb), м": toFixed(database.get_parameters("Длина сляба (bb)").value, 3),
                "Ширина сляба (a), м": toFixed(database.get_parameters("Ширина сляба (a)").value, 3),
                "Длина печи (Lp), м": toFixed(database.get_parameters("Длина печи (Lp)").value, 3)
            },
            "Температурные параметры": {
                "Температура окружающей среды (toc), °C": toFixed(database.get_parameters("Температура окружающей среды (toc)").value, 3),
                "Температура насыщения (tnas), °C": toFixed(database.get_parameters("Температура насыщения (tnas)").value, 3),
                "Начальная температура металла (tmn), °C": toFixed(database.get_parameters("Начальная температура металла (tmn)").value, 3),
                "Разница температур при посаде (twDif), °C": toFixed(database.get_parameters("Разница температур при посаде (twDif)").value, 3),
                "Температура методической зоны (twMetn), °C": toFixed(database.get_parameters("Температура методической зоны (twMetn)").value, 3),
                "Температура нижнего подогрева методической зоны (twMetNpk), °C": toFixed(database.get_parameters("Температура нижнего подогрева методической зоны (twMetNpk)").value, 3),
                "Температура первой сварочной зоны (twSv1n), °C": toFixed(database.get_parameters("Температура первой сварочной зоны (twSv1n)").value, 3),
                "Температура второй сварочной зоны (twSv2), °C": toFixed(database.get_parameters("Температура второй сварочной зоны (twSv2)").value, 3),
                "Температура нижнего подогрева 2-й сварочной зоны (twNp2k), °C": toFixed(database.get_parameters("Температура нижнего подогрева 2-й сварочной зоны (twNp2k)").value, 3),
                "Температура томильной зоны (twTom), °C": toFixed(database.get_parameters("Температура томильной зоны (twTom)").value, 3),
                "Температура нижнего подогрева томильной зоны (twNp2n), °C": toFixed(database.get_parameters("Температура нижнего подогрева томильной зоны (twNp2n)").value, 3)
            },
            "Теплоизоляция": {
                "Толщина первого слоя (dst1), м": toFixed(database.get_parameters("Толщина первого слоя (dst1)").value, 3),
                "Толщина второго слоя (dst2), м": toFixed(database.get_parameters("Толщина второго слоя (dst2)").value, 3),
                "Внутренний радиус трубы (r1), м": toFixed(database.get_parameters("Внутренний радиус трубы (r1)").value, 3),
                "Внешний радиус трубы (r2), м": toFixed(database.get_parameters("Внешний радиус трубы (r2)").value, 3),
                "Радиус теплоизоляции (r3), м": toFixed(database.get_parameters("Радиус теплоизоляции (r3)").value, 3)
            },
            "Другие параметры": {
                "Допустимый перепад (dtdop), °C": toFixed(database.get_parameters("Допустимый перепад (dtdop)").value, 3),
                "Количество узлов (n), кол.": toFixed(database.get_parameters("Количество узлов (n)").value, 3),
                "Время нагрева (time_H), мин": toFixed(database.get_parameters("Время нагрева (time_H)").value, 3),
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
                "Суммарная длина труб СИО в томильной зоне (LsioTom), м": toFixed(database.get_parameters("Суммарная длина труб СИО в томильной зоне (LsioTom)").value, 3)
            }
        }

        row_counter = 1
        col_counter = 0

        geo_label = customtkinter.CTkLabel(self, text="Геометрические параметры", font=customtkinter.CTkFont(size=14, weight="bold"))
        geo_label.grid(row=row_counter, column=col_counter, columnspan=2, sticky="NSEW", pady=(10, 5), padx=10)

        row_counter += 1

        for key, value in furnace_params["Геометрические параметры"].items():
            list_item = customtkinter.CTkLabel(self, text=key, font=customtkinter.CTkFont(size=12))
            list_item.grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="E")

            list_item_text_box = customtkinter.CTkEntry(self, height=25, width=120)
            list_item_text_box.grid(row=row_counter, column=col_counter + 1, padx=10, pady=5, sticky="W")
            list_item_text_box.insert(0, str(value))
            self.text_boxes[key] = list_item_text_box

            row_counter += 1


        row_counter = 1
        col_counter = 2
        
        temp_label = customtkinter.CTkLabel(self, text="Температурные параметры", font=customtkinter.CTkFont(size=14, weight="bold"))
        temp_label.grid(row=row_counter, column=col_counter, columnspan=2, sticky="NSEW", pady=(10, 5), padx=10)
        
        row_counter += 1

        for key, value in furnace_params["Температурные параметры"].items():
            list_item = customtkinter.CTkLabel(self, text=key, font=customtkinter.CTkFont(size=12))
            list_item.grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="E")

            list_item_text_box = customtkinter.CTkEntry(self, height=25, width=120)
            list_item_text_box.grid(row=row_counter, column=col_counter + 1, padx=(0,10), pady=5, sticky="W")
            list_item_text_box.insert(0, str(value))
            self.text_boxes[key] = list_item_text_box

            row_counter += 1

        row_counter = len(furnace_params["Температурные параметры"]) + 2
        col_counter = 2
        
        temp_label = customtkinter.CTkLabel(self, text="Площадь футеровки по зонам", font=customtkinter.CTkFont(size=14, weight="bold"))
        temp_label.grid(row=row_counter, column=col_counter, columnspan=2, sticky="NSEW", pady=(10, 5), padx=10)
        
        row_counter += 1

        for key, value in furnace_params["Площадь футеровки по зонам"].items():
            list_item = customtkinter.CTkLabel(self, text=key, font=customtkinter.CTkFont(size=12))
            list_item.grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="E")

            list_item_text_box = customtkinter.CTkEntry(self, height=25, width=120)
            list_item_text_box.grid(row=row_counter, column=col_counter + 1, padx=(0,10), pady=5, sticky="W")
            list_item_text_box.insert(0, str(value))
            self.text_boxes[key] = list_item_text_box

            row_counter += 1


        row_counter = len(furnace_params["Геометрические параметры"]) + 2
        col_counter = 0
        
        t_iso_label = customtkinter.CTkLabel(self, text="Теплоизоляция", font=customtkinter.CTkFont(size=14, weight="bold"))
        t_iso_label.grid(row=row_counter, column=col_counter, columnspan=2, sticky="NSEW", pady=(10, 5), padx=10)
        
        row_counter += 1

        for key, value in furnace_params["Теплоизоляция"].items():
            list_item = customtkinter.CTkLabel(self, text=key, font=customtkinter.CTkFont(size=12))
            list_item.grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="E")

            list_item_text_box = customtkinter.CTkEntry(self, height=25, width=120)
            list_item_text_box.grid(row=row_counter, column=col_counter + 1, padx=10, pady=5, sticky="W")
            list_item_text_box.insert(0, str(value))
            self.text_boxes[key] = list_item_text_box

            row_counter += 1

        
        row_counter = len(furnace_params["Геометрические параметры"]) + len(furnace_params["Теплоизоляция"]) + 3
        col_counter = 0
        
        t_iso_label = customtkinter.CTkLabel(self, text="Другие параметры", font=customtkinter.CTkFont(size=14, weight="bold"))
        t_iso_label.grid(row=row_counter, column=col_counter, columnspan=2, sticky="NSEW", pady=(10, 5), padx=10)
        
        row_counter += 1

        for key, value in furnace_params["Другие параметры"].items():
            list_item = customtkinter.CTkLabel(self, text=key, font=customtkinter.CTkFont(size=12))
            list_item.grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="E")

            list_item_text_box = customtkinter.CTkEntry(self, height=25, width=120)
            list_item_text_box.grid(row=row_counter, column=col_counter + 1, padx=10, pady=5, sticky="W")
            list_item_text_box.insert(0, str(value))
            self.text_boxes[key] = list_item_text_box

            row_counter += 1

        
        row_counter = len(furnace_params["Температурные параметры"]) + len(furnace_params["Площадь футеровки по зонам"]) + 3

        # Кнопки "Подтвердить" и "Отменить"
        confirm_button = customtkinter.CTkButton(self, text="Подтвердить", width=160, fg_color='#699187', hover_color='#84a59d', text_color='black',
                                                 font=customtkinter.CTkFont(size=12, weight="bold"), command=self.confirm)
        confirm_button.grid(row=row_counter, column=0, columnspan=2, pady=20)

        cancel_button = customtkinter.CTkButton(self, text="Отменить", width=160, fg_color='#ed5855', hover_color='#f28482', text_color='black',
                                                font=customtkinter.CTkFont(size=12, weight="bold"), command=self.close_window)
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