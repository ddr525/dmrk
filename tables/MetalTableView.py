import customtkinter as ctk

from utilities import toFixed

class MetalTableView(ctk.CTkScrollableFrame):

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

        # Получение данных
        heating_data = self.page.get_heating_data()["Расчет нагрева металла"]

        self.frame = ctk.CTkFrame(self, fg_color='#333333')
        self.frame.grid(row=0, column=0, sticky='nsew', padx=150, pady=20)
        self.frame.columnconfigure((0, 1), weight=1)

        # Заголовки таблицы
        headers = ["Параметр", "Значение"]
        for col_index, header in enumerate(headers):
            header_cell = ctk.CTkLabel(
                self.frame,
                text=header,
                font=ctk.CTkFont(size=15, weight="bold"),
                anchor="center",
                pady=5,
            )
            header_cell.grid(row=0, column=col_index, sticky="nsew", padx=(1, 0), pady=(5, 0))

        row_index = 1

        # Обрабатываем зоны
        for zone, values in heating_data.items():
            if isinstance(values, dict):  # Если это зона с параметрами
                # Добавляем зону с colspan=2
                zone_label = ctk.CTkLabel(
                    self.frame,
                    text=zone,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    anchor="center",
                    text_color='white',
                    pady=5,
                    fg_color="#555555"
                )
                zone_label.grid(row=row_index, column=0, columnspan=2, sticky="nsew", padx=(1, 0), pady=(5, 0))
                row_index += 1

                if(zone == "Расход топлива по зонам:"):
                    
                    val = {}

                    for param, value in values.items():
                        split = param.strip().split(',')

                        if split[0] not in val:
                            val[split[0]] = value + split[1] + "  "
                        else:
                            val[split[0]] += value + split[1]

                    for param, value in val.items():

                        param_label = ctk.CTkLabel(
                            self.frame,
                            text=" - " + param,
                            font=ctk.CTkFont(size=13, weight="bold"),
                            anchor="w",
                            text_color='white',
                            padx=30,
                            pady=3,
                        )
                        param_label.grid(row=row_index, column=0, sticky="w", padx=(5, 0), pady=(2, 2))

                        value_label = ctk.CTkLabel(
                            self.frame,
                            text=value,
                            font=ctk.CTkFont(size=13, weight="bold"),
                            anchor="w",
                            text_color='white',
                            padx=30,
                            pady=3,
                        )
                        value_label.grid(row=row_index, column=1, sticky="w", padx=(5, 0), pady=(2, 2))

                        row_index += 1

                else:
                    # Добавляем параметры зоны
                    for param, value in values.items():
                        
                        split = param.strip().split(',')

                        param_label = ctk.CTkLabel(
                            self.frame,
                            text=" - " + split[0],
                            font=ctk.CTkFont(size=13, weight="bold"),
                            anchor="w",
                            text_color='white',
                            padx=30,
                            pady=3,
                        )
                        param_label.grid(row=row_index, column=0, sticky="w", padx=(5, 0), pady=(2, 2))

                        string_value = ""

                        try:
                            string_value = toFixed(float(value), 1)
                        except:
                            string_value = value

                        value_label = ctk.CTkLabel(
                            self.frame,
                            text=string_value + split[1],
                            font=ctk.CTkFont(size=13, weight="bold"),
                            anchor="w",
                            text_color='white',
                            padx=30,
                            pady=3,
                        )
                        value_label.grid(row=row_index, column=1, sticky="w", padx=(5, 0), pady=(2, 2))

                        row_index += 1
            else:  # Если это отдельный параметр (например, "Время нагрева")

                split = zone.strip().split(',')

                string_value = ""

                if(split[0] == "Время нагрева"):
                    sp = values.strip().split(':')
                    string_value = sp[0] + "ч " + sp[1] + " м"
                else:
                    string_value = values + split[1]

                param_label = ctk.CTkLabel(
                    self.frame,
                    text=split[0],  # zone в данном случае — это название параметра
                    font=ctk.CTkFont(size=13, weight="bold"),
                    anchor="w",
                    text_color='white',
                    padx=30,
                    pady=3,
                )
                param_label.grid(row=row_index, column=0, sticky="w", padx=(5, 0), pady=(2, 2))

                value_label = ctk.CTkLabel(
                    self.frame,
                    text=string_value,  # values — это значение параметра
                    font=ctk.CTkFont(size=13, weight="bold"),
                    anchor="w",
                    text_color='white',
                    padx=30,
                    pady=3,
                )
                value_label.grid(row=row_index, column=1, sticky="w", padx=(5, 0), pady=(2, 2))

                row_index += 1
