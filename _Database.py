import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, or_, select
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

from Entities import *

class Database():
    
    def __init__(self):
        self.session = self.initialize_database()

        # Проверяем, пуста ли база
        if not self.session.query(Gas).first():
            self.populate_defaults()
            # print("База данных заполнена значениями по умолчанию.")
        # else:
            # print("База данных уже содержит данные.")

            # for gas in self.session.query(Gas).all():
            #     print(f"Газ: {gas.name}")
            #     print(f"Процентный состав: {gas.mixed_percentage}%")
            #     print("Компоненты:")
            #     for component in gas.components:
            #         print(f"  {component.component}: {component.value}")
            #     print()

    def get_gases(self):
        return self.session.query(Gas).all()
    
    def get_natural_and_blast_gases(self):
        return self.session.query(Gas).filter(or_(Gas.name == "Природный газ", Gas.name == "Доменный газ")).all()
    
    def get_gas_components(self, gas):
        return self.session.query(Gas).filter(Gas.name == gas).first().components
    
    def get_parameters(self, name):
        return self.session.query(GlobalParameter).filter(GlobalParameter.parameter == name).first()
    
    def get_experiment_number(self):
        res = self.session.query(Experiment).order_by(Experiment.id.desc()).first()
        if(res != None):
            return res.id
        return 0
    
    def get_experiments(self, name):
        return self.session.query(Experiment).filter(Experiment.name == name).all()
    
    def get_experiment_by_id(self, id):
        return self.session.query(Experiment).filter(Experiment.id == id).first()
    
    def get_last_experiment(self):
        return self.session.query(Experiment).order_by(Experiment.id.desc()).first()
    
    def remove_gas(self, element_name):
        self.session.query(Gas).filter(Gas.name == element_name).delete()
        self.session.commit()

    def reset(self):
        self.session.query(Gas).delete()
        self.session.query(GasComponent).delete()
        self.session.query(GlobalParameter).delete()

        self.session.commit()
        self.session.flush()

        self.populate_defaults()

    def get_percentage(self):
        # Процент вычета от 100
        p = 0
        
        for gas in self.session.query(Gas).filter(Gas.name != "Доменный газ").all():
            p += gas.mixed_percentage

        return 100 - p
    
    def get_gas_by_name(self, name):
        return self.session.query(Gas).filter(Gas.name == name).first()
    
    def update_blast_percentage(self):
        blast_percentage = self.get_percentage()

        blast_gas = self.get_gas_by_name("Доменный газ")

        if(blast_gas != None):
            blast_gas.mixed_percentage = blast_percentage
            self.session.commit()

    
    def update_gases(self, data):
        name = data['Название']
        mixed_per = data['Процентный состав']

        gas = self.session.query(Gas).filter(Gas.name == name).first()

        if(gas == None):
            gas = Gas(name=name, mixed_percentage=mixed_per)
            
            gas.components = [
                GasComponent(component="CH4", units="%", value=data['CH4']),
                GasComponent(component="C2H6", units="%", value=data['C2H6']),
                GasComponent(component="C3H8", units="%", value=data['C3H8']),
                GasComponent(component="C4H10", units="%", value=data['C4H10']),
                GasComponent(component="C5H12", units="%", value=data['C5H12']),
                GasComponent(component="CO", units="%", value=data['CO']),
                GasComponent(component="H2", units="%", value=data['H2']),
                GasComponent(component="CO2", units="%", value=data['CO2']),
                GasComponent(component="N2", units="%", value=data['N2']),
                GasComponent(component="O2", units="%", value=data['O2']),
                GasComponent(component="d", units="г/м³", value=data['d']),
                GasComponent(component="Стоимость", units="тг/1000м³", value=data['Стоимость']),
            ]
            self.session.add(gas)
        else:
            gas.mixed_percentage = mixed_per
            for element in gas.components:
                element.value = data[element.component]

        self.session.commit()

    def save_gases_global_parameters(self, pir_cf_v, t_air_v, t_gas_v, air_con_v):
        # Обновление пирометрического коэффициент
        pir = self.session.query(GlobalParameter).filter(GlobalParameter.parameter == "Пирометрический коэффициент").first()
        pir.value = pir_cf_v

        # Обновление подогрева воздуха
        t_air = self.session.query(GlobalParameter).filter(GlobalParameter.parameter == "Температура подогрева воздуха").first()
        t_air.value = t_air_v

        # Обновление смешанного газа
        t_gas = self.session.query(GlobalParameter).filter(GlobalParameter.parameter == "Температура смешанного газа").first()
        t_gas.value = t_gas_v

        # Обновление расхода воздуха
        air_con = self.session.query(GlobalParameter).filter(GlobalParameter.parameter == "Коэффициент расхода воздуха").first()
        air_con.value = air_con_v

        self.session.commit()

    def save_gas_results(self, title, results):
        gases = self.session.query(Gas).all()

        params = self.session.query(GlobalParameter).all()

        # Сохраняем в истории газ
        history_gases = []

        for gas in gases:
            hist_components = []

            for el in gas.components:
                hist_comp = HistoryGasComponent(
                  component = el.component,
                  value = el.value,
                  units = el.units
                )
                hist_components.append(hist_comp)

            hist_gas = HistoryGas(
                name = gas.name,
                mixed_percentage = gas.mixed_percentage,
                components = hist_components
            )

            history_gases.append(hist_gas)

        # Сохраняем в истории параметры расчета
        history_params = []

        for param in params:
            try:
                float_param = float(param.value)
                hist_param = HistoryGlobalParameter(
                    parameter_name = param.parameter,
                    value = float_param,
                    units = param.units,
                    value_str = ''
                ) 
                history_params.append(hist_param)
            except: 
                hist_param = HistoryGlobalParameter(
                    parameter_name = param.parameter,
                    value = 0.0,
                    units = param.units,
                    value_str = param.value_str 
                )
                history_params.append(hist_param)

        # Сохранение результатов
        exp_res = []

        for (name, value) in results:
            if('cards' in name):
                for key, el in value.items():
                    exp_res.append(ExperimentResult(
                        parameter = key,
                        value = el
                    ))
            else:
                exp_res.append(ExperimentResult(
                    parameter = name,
                    value = value
                ))

        exp = Experiment(
            name = title,
            history_gases = history_gases,
            history_parameters = history_params,
            results = exp_res
        )

        self.session.add(exp)
        self.session.commit() ## uncomment in prod

        return self.get_last_experiment()
    
    def save_fuilburn_results(self, data): 
        exp = self.session.query(Experiment).order_by(Experiment.id.desc()).first()
        # experiment = self.get_last_experiment() 

        for name, value in data:
            result = ExperimentResult(
                parameter=name,
                value=float(value),
                experiment_id=exp.id
            )
            self.session.add(result)

        self.session.commit()
        return self.get_last_experiment() 

    def save_gas_to_metal_exp_data(self, exp, data):
        res = []

        for key, value in data.items():
            param = GasMetalParameter(
                experiment_id = exp.id,
                parameter = key,
                value = value
            )

            self.session.add(param)
            res.append(value)

        self.session.commit() ## uncomment in prod

        return res
    
    def save_heating_data(self, exp, heating_data):
        # from rich.console import Console
        # from rich.tree import Tree

        # console = Console()

        # metall_tree = Tree("[bold cyan]Расчет нагрева металла[/bold cyan]")

        metal = MetalResults(experiment=exp)
        self.session.add(metal)

        for zone_name, data in heating_data["Расчет нагрева металла"].items():
            # zone_tree = metall_tree.add(f"[bold gray]{zone_name}[/bold gray]")

            if isinstance(data, dict):
                zone = HeatingZone(name=zone_name, metal=metal)
                self.session.add(zone)

                for param_name, param_value in data.items():
                    # section_tree = zone_tree.add(f"[green]{param_name}[/green]: [blue]{param_value}[/blue]")
                    split = param_name.strip().split(',')
                    param = HeatingParameter(zone=zone, name=split[0], units=split[1], value=param_value)
                    self.session.add(param)

            else:
                # zone_tree.add(f"[blue]{data}[/blue]")
                split = zone_name.strip().split(',')
                overall_param = OverallHeatingData(name=split[0], units=split[1], value=data, metal=metal)
                self.session.add(overall_param)
        
        self.session.commit()

        # balance_tree = Tree("[bold cyan]Тепловой баланс печи[/bold cyan]")

        balance = FurnaceBalance(experiment=exp)
        self.session.add(balance)

        for zone_name, data in heating_data["Тепловой баланс"].items():
            # zone_tree = balance_tree.add(f"[bold gray]{zone}[/bold gray]")

            zone = ZoneResult(name=zone_name, balance=balance)
            self.session.add(zone)
            
            for section, values in data.items():
                # section_tree = zone_tree.add(f"[green]{section}[/green]")

                if isinstance(values, dict):
                    heat = HeatFlow(type=section, zone=zone)
                    self.session.add(heat)

                    for key, value in values.items():
                        # section_tree.add(f"[blue]{key}[/blue]: {value}")
                        split = key.strip().split(',')

                        details = HeatFlowDetail(heat_flow=heat, name=split[0], units=split[1], value=value)
                        self.session.add(details)
                else:
                    # section_tree.add(f"[blue]{values}[/blue]")
                    split = section.strip().split(',')

                    params = HeatParameter(zone=zone, name=split[0], units=split[1], value=values)
                    self.session.add(params)

        self.session.commit()

        graph = HeatGraph(experiment=exp)
        self.session.add(graph)

        for key, value in heating_data["График"].items():

            if isinstance(value, (list, tuple, np.ndarray)):
                dot = GraphDots(heat_graph=graph, name=key)
                self.session.add(dot)

                for x in value:
                    data = GraphData(dot=dot, value=x)
                    self.session.add(data)
            else:
                param = GraphParam(heat_graph=graph, name=key, value=value)
                self.session.add(param)

        self.session.commit()

        #console.print(metall_tree)
        #console.print(balance_tree)

    def get_exp_result(self, name):
        return self.session.query(ExperimentResult).filter(ExperimentResult.parameter == name).all()
    
    def update_furnace_params(self, data):
        for key, value in data.items():
            split = key.split(',')

            param = self.get_parameters(split[0])

            if param is not None:
                param.value = value
            else: 
                try:
                    float_value = float(value)
                    self.session.add(
                        GlobalParameter(
                            parameter=split[0],
                            units=(split[1].strip() if len(split) > 1 else ''),
                            value_str='',     # строка
                            value=float_value # обнуляем числовое значение
                        )
                    )
                except:
                    self.session.add(
                        GlobalParameter(
                            parameter=split[0],
                            units=(split[1].strip() if len(split) > 1 else ''),
                            value=0.0,        # число
                            value_str=value   # обнуляем строковое значение
                        )
                    )
        self.session.commit()

    def get_overral_heating_data(self):
        return self.session.query(OverallHeatingData).order_by(OverallHeatingData.id.desc()).all()
    
    def get_overral_heating_data_by_name(self, name):
        return self.session.query(OverallHeatingData).filter(OverallHeatingData.name == name).order_by(OverallHeatingData.id.desc()).first()
    
    def get_furnace_params(self):
        pass

    def delete_exp_by_id(self, id):
        self.session.query(Experiment).filter(Experiment.id == id).delete()
        self.session.query(ExperimentResult).filter(ExperimentResult.experiment_id == id).delete()

        gases = self.session.query(HistoryGas).filter(HistoryGas.experiment_id == id)

        for gas in gases:
            self.session.query(HistoryGasComponent).filter(HistoryGasComponent.gas_id == gas.id).delete()
        
        self.session.query(HistoryGas).filter(HistoryGas.experiment_id == id).delete()
        self.session.query(HistoryGlobalParameter).filter(HistoryGlobalParameter.experiment_id == id).delete()

        self.session.query(GasMetalParameter).filter(GasMetalParameter.experiment_id == id).delete()

        self.session.commit()

    def delete_all_exp(self):
        self.session.query(Experiment).delete()
        self.session.query(ExperimentResult).delete()
        self.session.query(HistoryGas).delete()
        self.session.query(HistoryGasComponent).delete()
        self.session.query(HistoryGlobalParameter).delete()
        self.session.query(GasMetalParameter).delete()
        self.session.commit()

    # Инициализация базы данных
    def initialize_database(self):
        engine = create_engine("sqlite:///file.db", echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session()

    # Вставка данных по умолчанию
    def populate_defaults(self):
        # Газы
        natural_gas = Gas(name="Природный газ", mixed_percentage=0)
        coke_furnace_gas = Gas(name="Коксовый газ", mixed_percentage=19.03)
        liquified_furnace_gas = Gas(name="Сжиженный газ", mixed_percentage=0.63)
        blast_furnace_gas = Gas(name="Доменный газ", mixed_percentage=80.34)
        

        # Компоненты для природного газа
        natural_gas.components = [
            GasComponent(component="CH4", units="%", value=90.087),
            GasComponent(component="C2H4", units="%", value=0),
            GasComponent(component="C2H6", units="%", value=5.93),
            GasComponent(component="C3H8", units="%", value=1.64),
            GasComponent(component="C4H10", units="%", value=0.323),
            GasComponent(component="C5H12", units="%", value=0.036),
            GasComponent(component="CO", units="%", value=0),
            GasComponent(component="H2", units="%", value=0),
            GasComponent(component="CO2", units="%", value=0.199),
            GasComponent(component="N2", units="%", value=1.77),
            GasComponent(component="O2", units="%", value=0.015),
            GasComponent(component="d", units="г/м³", value=5),
            GasComponent(component="Стоимость", units="тг/1000м³", value=25000),
        ]

        # Компоненты для коксового газа
        coke_furnace_gas.components = [
            GasComponent(component="CH4", units="%", value=22.967),
            GasComponent(component="C2H4", units="%", value=1.833),
            GasComponent(component="C2H6", units="%", value=0.6),
            GasComponent(component="C3H8", units="%", value=0),
            GasComponent(component="C4H10", units="%", value=0),
            GasComponent(component="C5H12", units="%", value=0),
            GasComponent(component="CO", units="%", value=6.367),
            GasComponent(component="H2", units="%", value=60.9),
            GasComponent(component="CO2", units="%", value=1.633),
            GasComponent(component="N2", units="%", value=4.867),
            GasComponent(component="O2", units="%", value=0.833),
            GasComponent(component="d", units="г/м³", value=76),
            GasComponent(component="Стоимость", units="тг/1000м³", value=2000),
        ]

        # Компоненты для сжиженного газа
        liquified_furnace_gas.components = [
            GasComponent(component="CH4", units="%", value=22.967),
            GasComponent(component="C2H4", units="%", value=1.833),
            GasComponent(component="C2H6", units="%", value=0.6),
            GasComponent(component="C3H8", units="%", value=0),
            GasComponent(component="C4H10", units="%", value=0.),
            GasComponent(component="C5H12", units="%", value=0),
            GasComponent(component="CO", units="%", value=0),
            GasComponent(component="H2", units="%", value=0),
            GasComponent(component="CO2", units="%", value=0),
            GasComponent(component="N2", units="%", value=0),
            GasComponent(component="O2", units="%", value=0),
            GasComponent(component="d", units="г/м³", value=0),
            GasComponent(component="Плотность", units="кг/м³", value=450),
            GasComponent(component="Стоимость", units="тг/т", value=186.6667),
        ]

        # Компоненты для доменного газа
        blast_furnace_gas.components = [
            GasComponent(component="CH4", units="%", value=0),
            GasComponent(component="C2H4", units="%", value=0),
            GasComponent(component="C2H6", units="%", value=0),
            GasComponent(component="C3H8", units="%", value=0),
            GasComponent(component="C4H10", units="%", value=0),
            GasComponent(component="C5H12", units="%", value=0),
            GasComponent(component="CO", units="%", value=21.52),
            GasComponent(component="H2", units="%", value=1.64),
            GasComponent(component="CO2", units="%", value=16.26),
            GasComponent(component="N2", units="%", value=59.28),
            GasComponent(component="O2", units="%", value=1.3),
            GasComponent(component="d", units="г/м³", value=76),
            GasComponent(component="Стоимость", units="тг/1000м³", value=2500),
        ]

        # Параметры
        global_parameters = [
            GlobalParameter(parameter="Пирометрический коэффициент",  units="", value=0.725),
            GlobalParameter(parameter="Температура подогрева воздуха", units="°C", value=623 - 273),
            GlobalParameter(parameter="Температура смешанного газа",  units="°C", value=293 - 273),
            GlobalParameter(parameter="Коэффициент расхода воздуха",  units="", value=1.05),
        ]

        # Добавляем данные в сессию
        self.session.add(natural_gas)
        self.session.add(coke_furnace_gas)
        self.session.add(liquified_furnace_gas)
        self.session.add(blast_furnace_gas)
        self.session.add_all(global_parameters)
        self.session.commit()

        dtdop = 318 # Допустимый перепад
        n = 11      # Количество узлов
        s = 0.200   # Толщина сляба м
        bb = 9.1    # Длина сляба м
        a = 1.250   # Ширина сляба м

        toc = 20 # Т окружающей среды

        # Параметры футировки
        dst1 = 0.464  # Толщина первой стены, м
        dst2 = 0.115  # Толщина второй стены, м
        tnas = 180 # температура насыщения при P=10 МПа
        r2 = 0.146 / 2   # наружний радиус трубы
        r1 = r2 - 0.030  # внутренний радиус трубы
        r3 = r2 + 0.0132 # диаметр теплоизоляции

        time_H = 240 # Время нагрева в мин

        tMet_per = 0.1784 * 100 # время в процентах методическая зона
        tSv1_per = 0.2826 * 100 # время в процентах первая сварочная зона
        tSv2_per = 0.2944 * 100 # время в процентах во второй зоне
        tTom_per = 0.2446 * 100 # время в процентах в томильной зоне

        tmn = 20 # Начальная температура металла
        twDif = 50 # Разница тепмператур при посаде

        twMetn = 1050    # температура методической зоны
        twMetNpk = 1100; # температура нижней подогрева методической зоны

        twSv1n = 1300    # температура первой сварочной зоны

        twSv2  = 1350    # температура второй сварочной зоны
        twNp2k = 1250  # температура нижнего подогрева второй сварочной зоны

        twTom  = 1280    # температура томильной зоны
        
        twNp2n = 1250 # температура нижнего подогрева томильной зоны
        
        Lp = 35.544 # Длина печи
        
        # Площадь футеровки по зонам
        Fmet = 31.05+35.99  # методическая зона
        Fsv1 = 54.88+49.69  # первая сварочная зона
        Fsv2 = 92.7+63.4    # во второй зоне
        Ftom = 41.63+51.65  # в томильной зоне

        LsioMet = 2*4*Lp*0.189+6.708*2*2 # Суммарная длина труб СИО в методической зон, м
        LsioSv1 = 4*Lp*0.245+6.708*2*3   # Суммарная длина труб СИО в первой сварочной зоне, м
        LsioSv2 = 4*Lp*0.312+6.708*2*4   # Суммарная длина труб СИО во второй зоне, м
        LsioTom = 4*Lp*0.254+6.708*2*2   # Суммарная длина труб СИО в томильной зоне, м

        furnace_params = {
            "Толщина сляба (s), м": s,
            "Длина сляба (bb), м": bb,
            "Ширина сляба (a), м": a,
            "Длина печи (Lp), м": Lp,

            "Температура окружающей среды (toc), °C": toc,
            "Температура насыщения (tnas), °C": tnas,
            "Начальная температура металла (tmn), °C": tmn,
            "Разница температур при посаде (twDif), °C": twDif,
            "Температура методической зоны (twMetn), °C": twMetn,
            "Температура нижнего подогрева методической зоны (twMetNpk), °C": twMetNpk,
            "Температура первой сварочной зоны (twSv1n), °C": twSv1n,
            "Температура второй сварочной зоны (twSv2), °C": twSv2,
            "Температура нижнего подогрева 2-й сварочной зоны (twNp2k), °C": twNp2k,
            "Температура томильной зоны (twTom), °C": twTom,
            "Температура нижнего подогрева томильной зоны (twNp2n), °C": twNp2n,
            
            "Толщина первого слоя (dst1), м": dst1,
            "Толщина второго слоя (dst2), м": dst2,
            "Внутренний радиус трубы (r1), м": r1,
            "Внешний радиус трубы (r2), м": r2,
            "Радиус теплоизоляции (r3), м": r3,
            
            "Допустимый перепад (dtdop), °C": dtdop,
            "Количество узлов (n-нечётное), кол.": n,
            "Время нагрева (time_H), мин": time_H,
            "Время в методической зоне, %": tMet_per,
            "Время в первой сварочной зоне, %": tSv1_per,
            "Время во второй сварочной зоне, %": tSv2_per,
            "Время в томильной зоне, %": tTom_per,

            "Методическая зона (Fmet), м²": Fmet,
            "Первая сварочная зона (Fsv1), м²": Fsv1,
            "Вторая сварочная зона (Fsv2), м²": Fsv2,
            "Томильная зона (Ftom), м²": Ftom,

            "Суммарная длина труб СИО в методической зоне (LsioMet), м" : LsioMet,
            "Суммарная длина труб СИО в первой сварочной зоне (LsioSv1), м" : LsioSv1,
            "Суммарная длина труб СИО во второй зоне (LsioSv2), м" : LsioSv2,
            "Суммарная длина труб СИО в томильной зоне (LsioTom), м" : LsioTom,
            "Сохранность футеровки СИО, %": 50,
            "Марка стали (группа нагрева)": "DX51D (1)"
        }	 


        self.update_furnace_params(furnace_params)

    
            

