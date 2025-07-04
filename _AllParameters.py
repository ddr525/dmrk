import customtkinter

from CTkMessagebox import CTkMessagebox 

from ExperimentWindow import *
from _Calculations import MetallBurnCalculation, FuelСonsumptionCalculation
from utilities import toFixed

class AllParameters(customtkinter.CTkFrame):
    def __init__(self, master, database, **kwargs):
        super().__init__(master, **kwargs)
        self.toplevel = None
        self.master = master

        self.font=customtkinter.CTkFont(size=13, weight="bold")
        
        self.configure(fg_color="#7c7878")
        
        #-----Доля газов---------
        self.gases_label = customtkinter.CTkLabel(self, text="Доля газов", font=self.font, text_color="#ffffff", justify="left")
        self.gases_label.grid(row=0, column=0, pady=[15,0])
        self.gases_label.grid_configure(sticky="ew")
        self.grid_columnconfigure(0, weight=1)
        
        self.database = database
        self.list = database.get_gases()
        self.table = customtkinter.CTkFrame(self, fg_color="transparent")
        self.table.grid(row=1, column=0)

        row=0
        self.params = {}
        for row, value in enumerate(self.list):
            row += 1
            pady_block=0

            fg_color_block="#444242"
            if row%2==0:
                fg_color_block="#616161"

            label_frame = customtkinter.CTkFrame(self.table, width=150, height=28, border_color="black", border_width=2, fg_color=fg_color_block, corner_radius=0)
            label_frame.grid(row=row, column=0, padx=[10,0], pady=pady_block, sticky="nsew")
            label_frame.grid_propagate(False)
            label_name = customtkinter.CTkLabel(label_frame, text=value.name + ", %", height=24, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff")
            label_name.grid(row=0, column=0, pady=2, padx=5, sticky="w")
            
            label_percent = customtkinter.CTkEntry(self.table, width=50, height=28, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff", border_color="black", border_width=2)
            label_percent.grid(row=row, column=1)

            self.params[value.name] = label_percent
        #---------------------- 

        #----Режим нагрева-----
        mode_block = customtkinter.CTkFrame(self, fg_color="transparent")
        mode_block.grid(row=2, column=0)

        mode_title = customtkinter.CTkLabel(mode_block, text="Режим нагрева", font=self.font, text_color="#ffffff")
        mode_title.grid(row=0, column=0, pady=[15,0], sticky="nsew")

        mode_frame = customtkinter.CTkFrame(mode_block, width=150, height=28, border_color="black", border_width=2, fg_color=fg_color_block, corner_radius=0)
        mode_frame.grid(row=1, column=0, padx=[10,0], pady=0, sticky="nsew")
        mode_frame.grid_propagate(False)
        mode_label = customtkinter.CTkLabel(mode_frame, text="Время нагрева, мин", height=24, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff")
        mode_label.grid(row=0, column=0, pady=2, padx=5, sticky="w")

        self.time_H = customtkinter.CTkEntry(mode_block, width=50, height=28, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff", border_color="black", border_width=2)
        self.time_H.grid(row=1, column=1)
        self.params["Время нагрева, мин"] = self.time_H
        #-------------------

        #------Температура по зонам печи---------
        temps_block = customtkinter.CTkFrame(self, fg_color="transparent")
        temps_block.grid(row=3, column=0, pady=20)

        temps_title = customtkinter.CTkFrame(temps_block, border_color="black", border_width=2, height=24, width=200)
        temps_title.grid(row=0, column=0) 
        temps_title.grid_propagate(False)
        temps_title.grid_configure(columnspan=2)
        temps_label = customtkinter.CTkLabel(temps_title, text="Температура по зонам печи", width=200, height=24, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff")
        temps_label.grid(row=0, column=0)

        temps_table_title = customtkinter.CTkFrame(temps_block, width=50, height=28, border_color="black", border_width=2, fg_color=fg_color_block, corner_radius=0)
        temps_table_title.grid(row=1, column=0, padx=[0,0], pady=0, sticky="nsew")
        temps_table_title.grid_propagate(False)
        temps_table_title.grid_columnconfigure(0, weight=1)
        temps_table_title_label = customtkinter.CTkLabel(temps_table_title, text="№ зоны", height=24, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff")
        temps_table_title_label.grid(row=0, column=0, pady=(2,0), padx=0)

        temps_table_degrees = customtkinter.CTkFrame(temps_block, width=100, height=28, border_color="black", border_width=2, fg_color=fg_color_block, corner_radius=0)
        temps_table_degrees.grid(row=1, column=1, padx=[0,0], pady=0, sticky="nsew")
        temps_table_degrees.grid_propagate(False)
        temps_table_degrees.grid_columnconfigure(0, weight=1)
        temps_table_degrees_label = customtkinter.CTkLabel(temps_table_degrees, text="°С", width=45, height=24, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff")
        temps_table_degrees_label.grid(row=0, column=0, pady=(2,0), padx=[0,5])
        

        temps_table_td = customtkinter.CTkFrame(temps_block, width=50, height=28, border_color="black", border_width=2, fg_color=fg_color_block, corner_radius=0)
        temps_table_td.grid(row=2, column=0, padx=[0,0], pady=0, sticky="nsew")
        temps_table_td.grid_propagate(False)
        temps_table_td.grid_columnconfigure(0, weight=1)
        temps_table_td_label = customtkinter.CTkLabel(temps_table_td, text="1", height=24, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff")
        temps_table_td_label.grid(row=0, column=0, pady=(2,0), padx=0)
        
        self.twSv1n = customtkinter.CTkEntry(temps_block, width=150, height=28, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff", border_color="black", border_width=2)
        self.twSv1n.grid(row=2, column=1)
        self.twSv1n._entry.configure(insertbackground="white")
        self.params["1 зона"] = self.twSv1n


        temps_table_td = customtkinter.CTkFrame(temps_block, width=50, height=28, border_color="black", border_width=2, fg_color=fg_color_block, corner_radius=0)
        temps_table_td.grid(row=3, column=0, padx=[0,0], pady=0, sticky="nsew")
        temps_table_td.grid_propagate(False)
        temps_table_td.grid_columnconfigure(0, weight=1)
        temps_table_td_label = customtkinter.CTkLabel(temps_table_td, text="2", height=24, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff")
        temps_table_td_label.grid(row=0, column=0, pady=(2,0), padx=0)
        
        self.twMetNpk = customtkinter.CTkEntry(temps_block, width=150, height=28, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff", border_color="black", border_width=2)
        self.twMetNpk.grid(row=3, column=1)
        self.twMetNpk._entry.configure(insertbackground="white")
        self.params["2 зона"] = self.twMetNpk
 
        
        temps_table_td = customtkinter.CTkFrame(temps_block, width=50, height=28, border_color="black", border_width=2, fg_color=fg_color_block, corner_radius=0)
        temps_table_td.grid(row=4, column=0, padx=[0,0], pady=0, sticky="nsew")
        temps_table_td.grid_propagate(False)
        temps_table_td.grid_columnconfigure(0, weight=1)
        temps_table_td_label = customtkinter.CTkLabel(temps_table_td, text="3", height=24, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff")
        temps_table_td_label.grid(row=0, column=0, pady=(2,0), padx=0)
        
        self.twSv2 = customtkinter.CTkEntry(temps_block, width=150, height=28, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff", border_color="black", border_width=2)
        self.twSv2.grid(row=4, column=1)
        self.twSv2._entry.configure(insertbackground="white")
        self.params["3 зона"] = self.twSv2


        temps_table_td = customtkinter.CTkFrame(temps_block, width=50, height=28, border_color="black", border_width=2, fg_color=fg_color_block, corner_radius=0)
        temps_table_td.grid(row=5, column=0, padx=[0,0], pady=0, sticky="nsew")
        temps_table_td.grid_propagate(False)
        temps_table_td.grid_columnconfigure(0, weight=1)
        temps_table_td_label = customtkinter.CTkLabel(temps_table_td, text="4", height=24, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff")
        temps_table_td_label.grid(row=0, column=0, pady=(2,0), padx=0)
        
        self.twNp2n = customtkinter.CTkEntry(temps_block, width=150, height=28, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff", border_color="black", border_width=2)
        self.twNp2n.grid(row=5, column=1) 
        self.twNp2n._entry.configure(insertbackground="white")
        self.params["4 зона"] = self.twNp2n


        temps_table_td = customtkinter.CTkFrame(temps_block, width=50, height=28, border_color="black", border_width=2, fg_color=fg_color_block, corner_radius=0)
        temps_table_td.grid(row=6, column=0, padx=[0,0], pady=0, sticky="nsew")
        temps_table_td.grid_propagate(False)
        temps_table_td.grid_columnconfigure(0, weight=1)
        temps_table_td_label = customtkinter.CTkLabel(temps_table_td, text="5", height=24, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff")
        temps_table_td_label.grid(row=0, column=0, pady=(2,0), padx=0)
        
        self.twTom = customtkinter.CTkEntry(temps_block, width=150, height=28, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff", border_color="black", border_width=2)
        self.twTom.grid(row=6, column=1)
        self.twTom._entry.configure(insertbackground="white", insertwidth=2)
        self.params["5 зона"] = self.twTom

        #------------------Кнопка "Просчитать"-------------------------
        add_button = customtkinter.CTkButton(self, text="Просчитать", fg_color='#ac0d0d',font=self.font, hover_color="#d81111", width=200
                                             , command=lambda: self._calculate(
                                                 float(self.time_H.get()), 
                                                 float(self.twSv1n.get()), 
                                                 float(self.twMetNpk.get()), 
                                                 float(self.twSv2.get()), 
                                                 float(self.twNp2n.get()), 
                                                 float(self.twTom.get()))
                                             )
        add_button.grid(row=4, column=0, padx=5, pady=(10, 10))
        #-------------------------------------------------------

        #---------------Опыты-----------------------------------
        exp_block = customtkinter.CTkFrame(self, fg_color="transparent")
        exp_block.grid(row=5, column=0, pady=20)

        exp_id_frame = customtkinter.CTkFrame(exp_block, width=120, height=28, border_color="black", border_width=2, fg_color=fg_color_block, corner_radius=0)
        exp_id_frame.grid(row=0, column=0, padx=[10,0], pady=pady_block, sticky="nsew")
        exp_id_frame.grid_propagate(False)
        exp_id_frame.grid_columnconfigure(0, weight=1)
        exp_id_label = customtkinter.CTkButton(exp_id_frame, text=f"№ опыта: 1", height=24, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff", command=self._open_exp_view)
        exp_id_label.grid(row=0, column=0, pady=2, padx=5)

        exp_description_frame = customtkinter.CTkFrame(exp_block, width=80, height=28, border_color="black", border_width=2, fg_color=fg_color_block, corner_radius=0)
        exp_description_frame.grid(row=0, column=1, padx=[0,10], pady=pady_block, sticky="nsew")
        exp_description_frame.grid_propagate(False)
        exp_description_frame.grid_columnconfigure(0, weight=1)
        self.exp_description_label = customtkinter.CTkLabel(exp_description_frame, text="", width=45, height=24, font=self.font, corner_radius=0, fg_color="transparent", text_color="#ffffff")
        self.exp_description_label.grid(row=0, column=0, pady=2, padx=[0,5])
        #-------------------------------------------------------

        #------------------Кнопка "Настройки по умолчанию"-------------------------
        add_button = customtkinter.CTkButton(self, text="Настройки по умолчанию", text_color="black", fg_color='#f7cdb1', hover_color="#ffba8d", width=200
                                            #  , command=self._reset_data
                                             )
        add_button.grid(row=6, column=0, padx=5, pady=(10, 10))
        #-------------------------------------------------------
    def _calculate(self, time_H, twSv1n, twMetNpk, twSv2, twNp2n, twTom): 
        from _Calculations import FuilBurnCalculation 
        gases = self.database.get_gases()
        if(len(gases) < 1):
            CTkMessagebox(title="Ошибка!", message="Нет данных доменного и/или природного газов", icon="cancel")
            return

        n = self.database.get_parameters("Пирометрический коэффициент").value
        tv = self.database.get_parameters("Температура подогрева воздуха").value + 273
        tg = self.database.get_parameters("Температура смешанного газа").value + 273
        l = self.database.get_parameters("Коэффициент расхода воздуха").value

        # сохранить в базу Доля газов
        params = self.params

        data = FuilBurnCalculation(gases, n, tv, tg, l, params) 
        result, gas_data = self.show_result(data) 
        
        history_params = [
            ("Время нагрева (time_H)", time_H), 
            ("Температура нижнего подогрева методической зоны (twMetNpk)", twMetNpk), 
            ("Температура первой сварочной зоны (twSv1n)", twSv1n), 
            ("Температура второй сварочной зоны (twSv2)", twSv2), 
            ("Температура томильной зоны (twTom)", twTom), 
            ("Температура нижнего подогрева томильной зоны (twNp2n)", twNp2n)]

        exp = self.database.save_gas_results("Расчет горения топлива", result, params, history_params) ## uncomment in prod

        Ts, ng, v, h2o, co2, n2, o2, Q, Qft, Qfv = self.database.save_gas_to_metal_exp_data(exp, gas_data) ## uncomment in prod
        
        # Геометрические параметры
        s = self.database.get_parameters("Толщина сляба (s)").value
        bb = self.database.get_parameters("Длина сляба (bb)").value
        a = self.database.get_parameters("Ширина сляба (a)").value
        Lp = self.database.get_parameters("Длина печи (Lp)").value

        # Температурные параметры
        toc = self.database.get_parameters("Температура окружающей среды (toc)").value + 273
        tnas = self.database.get_parameters("Температура насыщения (tnas)").value + 273
        tmn = self.database.get_parameters("Начальная температура металла (tmn)").value + 273
        twDif = self.database.get_parameters("Разница температур при посаде (twDif)").value
        twMetn = self.database.get_parameters("Температура методической зоны (twMetn)").value + 273
        twNp2k = self.database.get_parameters("Температура нижнего подогрева 2-й сварочной зоны (twNp2k)").value + 273
        
        twMetNpk += 273
        twSv1n += 273
        twSv2 += 273
        twTom += 273
        twNp2n += 273
        # twMetNpk = self.database.get_parameters("Температура нижнего подогрева методической зоны (twMetNpk)").value + 273
        # twSv1n = self.database.get_parameters("Температура первой сварочной зоны (twSv1n)").value + 273
        # twSv2 = self.database.get_parameters("Температура второй сварочной зоны (twSv2)").value + 273
        # twTom = self.database.get_parameters("Температура томильной зоны (twTom)").value + 273
        # twNp2n = self.database.get_parameters("Температура нижнего подогрева томильной зоны (twNp2n)").value + 273

        # Теплоизоляция
        dst1 = self.database.get_parameters("Толщина первого слоя (dst1)").value
        dst2 = self.database.get_parameters("Толщина второго слоя (dst2)").value
        r2 = self.database.get_parameters("Внешний радиус трубы (r2)").value
        r1 = self.database.get_parameters("Внутренний радиус трубы (r1)").value
        r3 = self.database.get_parameters("Радиус теплоизоляции (r3)").value

        # Другие параметры
        dtdop = self.database.get_parameters("Допустимый перепад (dtdop)").value
        n = int(self.database.get_parameters("Количество узлов (n-нечётное)").value)
        
        time_H *= 60
        # time_H = self.database.get_parameters("Время нагрева (time_H)").value * 60

        tMet_per = self.database.get_parameters("Время в методической зоне").value / 100
        tSv1_per = self.database.get_parameters("Время в первой сварочной зоне").value / 100
        tSv2_per = self.database.get_parameters("Время во второй сварочной зоне").value / 100
        tTom_per = self.database.get_parameters("Время в томильной зоне").value / 100

        # Площадь футеровки по зонам
        Fmet = self.database.get_parameters("Методическая зона (Fmet)").value
        Fsv1 = self.database.get_parameters("Первая сварочная зона (Fsv1)").value
        Fsv2 = self.database.get_parameters("Вторая сварочная зона (Fsv2)").value
        Ftom = self.database.get_parameters("Томильная зона (Ftom)").value

        LsioMet = self.database.get_parameters("Суммарная длина труб СИО в методической зоне (LsioMet)").value
        LsioSv1 = self.database.get_parameters("Суммарная длина труб СИО в первой сварочной зоне (LsioSv1)").value
        LsioSv2 = self.database.get_parameters("Суммарная длина труб СИО во второй зоне (LsioSv2)").value
        LsioTom = self.database.get_parameters("Суммарная длина труб СИО в томильной зоне (LsioTom)").value
        LsioPercent = self.database.get_parameters("Сохранность футеровки СИО").value
        heating_data = MetallBurnCalculation(
                    s, bb, a, Lp, toc, tnas, tmn, twDif, twMetn, twMetNpk, twSv1n, twSv2, twNp2k, twTom, twNp2n,
                    dst1, dst2, r1, r2, r3, dtdop, n, time_H, tMet_per, tSv1_per, tSv2_per, tTom_per, Fmet, Fsv1, Fsv2, Ftom,
                    LsioMet, LsioSv1, LsioSv2, LsioTom, LsioPercent,
                    Ts, ng, v, h2o, co2, n2, o2, Q, Qft, Qfv,
                    
                    str(self.database.get_parameters("Марка стали (группа нагрева)").value_str))
        


        self.database.save_heating_data(exp, heating_data) 
        heating_data["Расчет нагрева металла"]["Толщина сляба"] = s
        heating_data["Расчет нагрева металла"]["Длина сляба"] = bb
        heating_data["Расчет нагрева металла"]["Ширина сляба"] = a
        heating_data["Расчет нагрева металла"]["Длина печи"] = Lp
        heating_data["Расчет нагрева металла"]["Марка стали"] = str(self.database.get_parameters("Марка стали (группа нагрева)").value_str) 
        fuel_consumption = FuelСonsumptionCalculation(
            gases, 
            heating_data,
            heating_data["Расчет нагрева металла"]["Расход топлива на печь, тыс. м³/час"],
            heating_data["Расчет нагрева металла"]["Производительность печи, т/час"],
            result,
            self.params
            )
        result.extend(fuel_consumption) 
        self.database.save_fuilburn_results(fuel_consumption) ## uncomment in prod 
        self.master.update_all(heating_data, result) 


    def show_result(self, data):
        res = [ 
            ("Низшая рабочая теплота\nсгорания смеси, ккал/м³ (при 20°C)", toFixed(data[4], 3)),
            ("Цена смешанного газа, тг", toFixed(data[2], 1)),
            ("cards", data[5]),
            ("Плотность газа при н.у., кг/м³", toFixed(data[6], 3)),
            ("Действительный расход воздуха, м³/м³", toFixed(data[7], 3)),
            ("Удельный выход дыма, м³/м³", toFixed(data[8], 3)),
            ("Теплоёмкость дыма, кДж/(м³·К)", toFixed(data[9], 3)),
            ("Калориметрическая температура горения, °C", toFixed(data[10], 3)),
            ("Действительная температура горения, °C", toFixed(data[11], 3)),
        ]

        # Вставка значений сгорания газов
        for row, (key, value) in enumerate(data[1].items()):
            res.insert(1 + row, (f"Конечная стоимость\n{key}, тг/1000м³", toFixed(value, 1)))

        # Вставка значений сгорания газов
        for row, (key, value) in enumerate(data[3].items()):
            res.insert(0 + row, (f"Низшая рабочая теплота\nсгорания - {key},\nккал/м³ (при 20°C)", toFixed(value, 3)))

        for row, (key, value) in enumerate(data[0].items()):
            res.insert(0 + row, (f"{key}, %", toFixed(value, 1))) 
        return res, data[12]
    
    def _open_exp_view(self):
        if(self.toplevel is None or not self.toplevel.winfo_exists()):
            self.toplevel = ExperimentWindow(database=self.database, page=self)
            self.toplevel.after(10, self.toplevel.lift)
        else:
            self.toplevel.focus()

    
    def update(self):
        self.exp_num = str(self.database.get_experiment_number())
        self.exp_description_label.configure(text="Номер опыта — " + self.exp_num)

    def open_exp(self, id):
        self.exp_num = str(id)
        self.exp_description_label.configure(text="Номер опыта — " + self.exp_num)

        exp = self.database.get_experiment_by_id(id)
        heating_data, gas_data = self.show_exp(exp)
        print(heating_data)
        self.time_H.delete(0, "end")  # очистить
        time_H = heating_data["data"]["Время нагрева (time_H)"]
        self.time_H.insert(0, int(time_H) if float(time_H).is_integer() else round(float(time_H), 2))

        self.twMetNpk.delete(0, "end")  # очистить
        twMetNpk = heating_data["data"]["Температура нижнего подогрева методической зоны (twMetNpk)"]
        self.twMetNpk.insert(0, int(twMetNpk) if float(twMetNpk).is_integer() else round(float(twMetNpk), 2))
        
        self.twSv1n.delete(0, "end")  # очистить
        twSv1n = heating_data["data"]["Температура первой сварочной зоны (twSv1n)"]
        self.twSv1n.insert(0, int(twSv1n) if float(twSv1n).is_integer() else round(float(twSv1n), 2))

        self.twSv2.delete(0, "end")  # очистить
        twSv2 = heating_data["data"]["Температура второй сварочной зоны (twSv2)"]
        self.twSv2.insert(0, int(twSv2) if float(twSv2).is_integer() else round(float(twSv2), 2))

        self.twTom.delete(0, "end")  # очистить
        twTom = heating_data["data"]["Температура томильной зоны (twTom)"]
        self.twTom.insert(0, int(twTom) if float(twTom).is_integer() else round(float(twTom), 2))
        
        self.twNp2n.delete(0, "end")  # очистить
        twNp2n = heating_data["data"]["Температура нижнего подогрева томильной зоны (twNp2n)"]
        self.twNp2n.insert(0, int(twNp2n) if float(twNp2n).is_integer() else round(float(twNp2n), 2))

        for row, value in enumerate(self.list):
            entry = self.params[value.name]
            entry.delete(0, "end")  # очистить
            history_data = float(dict(gas_data).get(f"{value.name}, %"))
            entry.insert(0, int(history_data) if history_data.is_integer() else round(history_data, 2))

        self.master.open_exp(heating_data, gas_data)


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
        name_params = [
            "Время нагрева (time_H)", 
            "Температура нижнего подогрева методической зоны (twMetNpk)", 
            "Температура первой сварочной зоны (twSv1n)", 
            "Температура второй сварочной зоны (twSv2)", 
            "Температура томильной зоны (twTom)", 
            "Температура нижнего подогрева томильной зоны (twNp2n)"]
        param_names = [name for name in name_params]
        print(param_names)
        for param in exp.history_parameters:
            if param.parameter_name in name_params:
                heating_data["data"][param.parameter_name] = param.value

            if(param.parameter_name == "Время в методической зоне" or param.parameter_name == "Время в первой сварочной зоне" or param.parameter_name == "Время во второй сварочной зоне" or param.parameter_name == "Время в томильной зоне"):
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

        # heating_data["data"]["Температура нижнего подогрева методической зоны (twMetNpk)"] = self.database.get_parameters("Температура нижнего подогрева методической зоны (twMetNpk)").value
        # heating_data["data"]["Температура первой сварочной зоны (twSv1n)"] = self.database.get_parameters("Температура первой сварочной зоны (twSv1n)").value
        # heating_data["data"]["Температура второй сварочной зоны (twSv2)"] = self.database.get_parameters("Температура второй сварочной зоны (twSv2)").value
        # heating_data["data"]["Температура томильной зоны (twTom)"] = self.database.get_parameters("Температура томильной зоны (twTom)").value
        # heating_data["data"]["Температура нижнего подогрева томильной зоны (twNp2n)"] = self.database.get_parameters("Температура нижнего подогрева томильной зоны (twNp2n)").value
        
        return heating_data 
    