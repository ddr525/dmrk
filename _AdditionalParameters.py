import customtkinter as ctk

from custom_widget.CTkXYFrame.ctk_xyframe import CTkXYFrame
from utilities import toFixed

class AdditionalParameters(ctk.CTkFrame):
    def __init__(self, master, root, database, **kwargs):
        super().__init__(master, **kwargs)
        
        data = [
            {'name': 'Максимальный перепад температур'},
            {'name': 'Кол-во теплоты получаемое металлом'},
            {'name': 'КПД нагрева'},
            {'name': 'Плотность газа при н.у.'},
            {'name': 'Действительный расход воздуха'},
            {'name': 'Удельный выход дыма'},
            {'name': 'Теплоёмкость дыма'},
            {'name': 'Калориметрическая температура'},
            {'name': 'Действительная температура'},
            {'name': 'Цена смешанного газа'},
            {'name': 'Себестоимость нагрева'}
        ]
        
        self.update(data)
        
    def update(self, data):
        block = ctk.CTkFrame(self, fg_color='#333333')
        block.grid(row=0, column=0)
        for i, value in enumerate(data):
            param_label = ctk.CTkLabel(
                block,
                text=value["name"],
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                text_color='white',
                padx=30,
                pady=3,
            )
            param_label.grid(row=i, column=0, sticky="w", padx=(5, 0), pady=(2, 2))

            value_label = ctk.CTkLabel(
                block,
                text="456",
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                text_color='white',
                padx=30,
                pady=3,
            )
            value_label.grid(row=i, column=1, sticky="w", padx=(5, 0), pady=(2, 2))