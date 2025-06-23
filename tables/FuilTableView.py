import customtkinter

from utilities import split_string, toFixed


class FuilTableView(customtkinter.CTkScrollableFrame):

    def __init__(self, master, page, root, database, *args, **kwargs):
        super().__init__(master, **kwargs)

        self.database = database
        self.root = root
        self.page = page

        self.columnconfigure((0), weight=1)

        self.update()


    def _clear(self):
            for widget in self.winfo_children():
                widget.destroy()

    def update(self):
        self._clear()

        data = []

        cards = []
        idx = 0

        # self.label = customtkinter.CTkLabel(
        #     self, text="Расчет горения топлива", font=customtkinter.CTkFont(size=18, weight="bold"), text_color='white'
        # )
        # self.label.grid(row=0, column=0, padx=20, pady=(10, 0))

        for (name, value) in self.page.get_data():
            if("cards" in name):
                for key, v in value.items():
                    cards.append([f"Состав дыма {key}", toFixed(v, 1) + " %"])
            else:
                # Разделение на наименование и количественную характеристику
                n, leg = split_string(name)

                if("%" in name or "тг" in name):
                    data.append([n, toFixed(float(value), 1) + " " + leg])
                    if('%' in name):
                        idx += 1
                else:
                    data.append([n, toFixed(float(value), 3) + " " + leg])

        for row, value in enumerate(cards):
            data.insert(idx + row, value)
        
        self.frame = customtkinter.CTkFrame(self, fg_color='#333333')
        #self.frame = customtkinter.CTkFrame(self, fg_color='white')
        
        self.frame.grid(row=0, column=0, sticky='nsew', padx=150, pady=20)
        self.frame.columnconfigure((0, 1), weight=1)

        # Заголовки таблицы
        headers = ["Параметр", "Значение"]
        for col_index, header in enumerate(headers):
            header_cell = customtkinter.CTkLabel(
                self.frame,
                text=header,
                font=customtkinter.CTkFont(size=15, weight="bold"),
                anchor="center",
                pady=5,
            )
            header_cell.grid(row=1, column=col_index, sticky="nsew", padx=(1, 0), pady=(5, 0))

        rows = 2

        # Добавление данных в таблицу с границами
        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row):
                # Создание рамки для каждой ячейки
                border_frame = customtkinter.CTkFrame(self.frame, fg_color='transparent', bg_color="transparent", border_width=2)
                border_frame.grid(
                    row=row_index + 2, column=col_index, sticky="nsew", padx=(1, 0), pady=(1, 3)
                )

                rows += 1

                # Добавление содержимого в рамку
                cell = customtkinter.CTkLabel(
                    border_frame,
                    text=value,
                    anchor="w",
                    font=customtkinter.CTkFont(size=13, weight="bold"),
                    corner_radius=20,
                    padx=30,
                    pady=3,
                    text_color='white',
                    fg_color='transparent',
                    bg_color='transparent'
                )
                #cell.grid(row=0, column=0)
                
                cell.pack(fill="both", expand=True)

        # Создание паддинга внизу таблицы
        border_frame = customtkinter.CTkFrame(self.frame, fg_color="transparent", height=2)
        border_frame.grid(
            row=rows, column=col_index, sticky="nsew", padx=(1, 0), pady=(0, 2)
        )
        
        border_frame = customtkinter.CTkFrame(self.frame, fg_color="transparent", height=2)
        border_frame.grid(
            row=rows + 1, column=col_index, sticky="nsew", padx=(1, 0), pady=(0, 2)
        )
