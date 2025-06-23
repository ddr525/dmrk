import customtkinter as ctk

from utilities import split_string, toFixed


class BalanceTableView(ctk.CTkScrollableFrame):

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
        heat_balance_data = self.page.get_heating_data()["Тепловой баланс"]

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
        for zone, values in heat_balance_data.items():
            if isinstance(values, dict):  # Если это зона с подкатегориями
                # Добавляем зону с colspan=2
                zone_label = ctk.CTkLabel(
                    self.frame,
                    text=zone,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    anchor="center",
                    pady=5,
                    text_color='white',
                    fg_color="#555555"
                )
                zone_label.grid(row=row_index, column=0, columnspan=2, sticky="nsew", padx=(1, 0), pady=(5, 0))
                row_index += 1

                # Разбираем "Приход тепла" и "Расход тепла"
                for subcategory, subvalues in values.items():
                    if isinstance(subvalues, dict):  # Подкатегории (Приход, Расход)
                        sub_label = ctk.CTkLabel(
                            self.frame,
                            text=subcategory,
                            font=ctk.CTkFont(size=13, weight="bold"),
                            anchor="center",
                            fg_color="#777777",
                            text_color='white',
                            pady=3
                        )
                        sub_label.grid(row=row_index, column=0, columnspan=2, sticky="nsew", padx=(1, 0), pady=(2, 0))
                        row_index += 1

                        val = {}

                        for param, value in subvalues.items():
                            split = param.strip().split(',')

                            if split[0] not in val:
                                val[split[0]] = value + split[1] + "  "
                            else:
                                val[split[0]] += value + split[1]

                        for param, value in val.items():

                            param_label = ctk.CTkLabel(
                                self.frame,
                                text=param,
                                font=ctk.CTkFont(size=13, weight="bold"),
                                anchor="w",
                                text_color='white',
                                padx=10
                            )
                            param_label.grid(row=row_index, column=0, sticky="w", padx=(5, 0), pady=(2, 2))

                            value_label = ctk.CTkLabel(
                                self.frame,
                                text=value,
                                font=ctk.CTkFont(size=13, weight="bold"),
                                anchor="w",
                                text_color='white',
                                padx=10
                            )
                            value_label.grid(row=row_index, column=1, sticky="w", padx=(5, 0), pady=(2, 2))

                            row_index += 1
                    else:  # Это просто параметр (например, "Расход топлива, тыс. м³/час")
                        param_label = ctk.CTkLabel(
                            self.frame,
                            text=subcategory,  # subcategory — это название параметра
                            font=ctk.CTkFont(size=13, weight="bold"),
                            anchor="w",
                            text_color='white',
                            padx=10
                        )
                        param_label.grid(row=row_index, column=0, sticky="w", padx=(5, 0), pady=(2, 2))

                        value_label = ctk.CTkLabel(
                            self.frame,
                            text=subvalues,  # subvalues — это значение параметра
                            font=ctk.CTkFont(size=13, weight="bold"),
                            anchor="w",
                            text_color='white',
                            padx=10
                        )
                        value_label.grid(row=row_index, column=1, sticky="w", padx=(5, 0), pady=(2, 2))

                        row_index += 1
