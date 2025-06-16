import customtkinter as ctk

from custom_widget.CTkXYFrame.ctk_xyframe import CTkXYFrame
from utilities import toFixed

class AdditionalParameters(ctk.CTkFrame):
    def __init__(self, master, root, database, **kwargs):
        super().__init__(master, **kwargs)
        
        self.names = ['Максимальный перепад температур',
                 'Кол-во теплоты получаемое металлом',
                 'КПД нагрева',
                 'Плотность газа при н.у., кг/м³',
                 'Действительный расход воздуха, м³/м³',
                 'Удельный выход дыма, м³/м³',
                 'Теплоёмкость дыма, Дж/(м³·К)',
                 'Калориметрическая температура, °C',
                 'Действительная температура, °C',
                 'Цена смешанного газа, тг/1000м³',
                 'Себестоимость нагрева'
        ]
        
        # self.update(names)
        
    def update(self, data):
        block = ctk.CTkFrame(self, fg_color='#333333')
        block.grid(row=0, column=0)
        
        data_dict = dict(data)

        for i, name in enumerate(self.names):
            print(i)
            print(name)
            value = data_dict.get(name, "0")
        
            param_label = ctk.CTkLabel(
                block,
                text=name,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                text_color='white',
                padx=30,
                pady=3,
            )
            param_label.grid(row=value, column=0, sticky="w", padx=(5, 0), pady=(2, 2))

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
        
        # for i, value in enumerate(data):
        #     param_label = ctk.CTkLabel(
        #         block,
        #         text=value["name"],
        #         font=ctk.CTkFont(size=13, weight="bold"),
        #         anchor="w",
        #         text_color='white',
        #         padx=30,
        #         pady=3,
        #     )
        #     param_label.grid(row=i, column=0, sticky="w", padx=(5, 0), pady=(2, 2))

        #     value_label = ctk.CTkLabel(
        #         block,
        #         text="456",
        #         font=ctk.CTkFont(size=13, weight="bold"),
        #         anchor="w",
        #         text_color='white',
        #         padx=30,
        #         pady=3,
        #     )
        #     value_label.grid(row=i, column=1, sticky="w", padx=(5, 0), pady=(2, 2))