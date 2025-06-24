import customtkinter as ctk

from custom_widget.CTkXYFrame.ctk_xyframe import CTkXYFrame
from utilities import toFixed

class AdditionalParameters(ctk.CTkFrame):
    def __init__(self, master, root, database, **kwargs):
        super().__init__(master, **kwargs)
        
        self.database = database
        
        self.names = [
                 'Максимальный перепад температур, °C',
                 'Кол-во теплоты получаемое металлом, кДж/кг',
                 'КПД нагрева, %',
                 'Плотность газа при н.у., кг/м³',
                 'Действительный расход воздуха, м³/м³',
                 'Удельный выход дыма, м³/м³',
                 'Теплоёмкость дыма, кДж/(м³·К)',
                 'Калориметрическая температура, °C',
                 'Действительная температура, °C',
                 'Цена смешанного газа, тг',
                 'Себестоимость нагрева, тг/т'
        ]
        
        # self.update(names)
        
    def update(self, data):
        block = ctk.CTkFrame(self, fg_color='#333333')
        block.grid(row=0, column=0)
        
        data_dict = dict(data)

        for i, name in enumerate(self.names):
            value = data_dict.get(name, "")
            
            if value == "":
                value = self.database.get_overral_heating_data_by_name(name.split(',')[0]).value
        
            param_label = ctk.CTkLabel(
                block,
                text=name,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                text_color='white',
                padx=30,
                pady=3,
            )
            param_label.grid(row=i, column=0, sticky="w", padx=(5, 0), pady=(2, 2))

            value_label = ctk.CTkLabel(
                block,
                text=value,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                text_color='white',
                padx=30,
                pady=3,
            )
            value_label.grid(row=i, column=1, sticky="w", padx=(5, 0), pady=(2, 2))