import customtkinter

class ParameterList(customtkinter.CTkFrame):
    def __init__(self, master, database, **kwargs):
        super().__init__(master, **kwargs)

        self.database = database

        # Ввод пирометрического коэффицента
        self.pir_cf_form = customtkinter.CTkFrame(self, fg_color='transparent')
        self.pir_cf_form.grid(row=0, column=0, padx=0, pady=0)
        self.pir_cf = customtkinter.CTkLabel(self.pir_cf_form, text="Пирометрический коэффициент", font=customtkinter.CTkFont(size=10, weight="bold"), justify='center', text_color="#ffffff")
        self.pir_cf.grid(row=0, column=0, padx=10, columnspan=2, pady=(5,0))
        
        # Добавляем label
        self.pir_cf_l = customtkinter.CTkLabel(self.pir_cf_form, text="       N =   ", font=customtkinter.CTkFont(size=10, weight="bold"), justify='center', text_color="#ffffff")
        self.pir_cf_l.grid(row=1, column=0, padx=(10, 0), pady=0)
        
        # Добавляем поле ввода
        self.pir_cf_v = customtkinter.CTkEntry(self.pir_cf_form, height=20, width=150)
        self.pir_cf_v.grid(row=1, column=1, padx=(0, 10), pady=0)

        # Ввод температуры подогрева воздуха
        self.t_air_form = customtkinter.CTkFrame(self, fg_color='transparent')
        self.t_air_form.grid(row=1, column=0, padx=0, pady=0)

        self.t_air = customtkinter.CTkLabel(self.t_air_form, text="Температура подогрева воздуха, °C", font=customtkinter.CTkFont(size=10, weight="bold"), justify='center', text_color="#ffffff")
        self.t_air.grid(row=0, column=0, padx=10, columnspan=2, pady=(5,0))

        self.t_air_l = customtkinter.CTkLabel(self.t_air_form, text="     Tв = ", font=customtkinter.CTkFont(size=10, weight="bold"), justify='center', anchor='w', text_color="#ffffff")
        self.t_air_l.grid(row=1, column=0, padx=(10, 0), pady=0)

        self.t_air_v = customtkinter.CTkEntry(self.t_air_form, height=20, width=150)
        self.t_air_v.grid(row=1, column=1, padx=(0, 10), pady=0)

        # Ввод температуры смешанного газа
        self.t_gas_form = customtkinter.CTkFrame(self, fg_color='transparent')
        self.t_gas_form.grid(row=2, column=0, padx=0, pady=0)

        self.t_gas = customtkinter.CTkLabel(self.t_gas_form, text="Температура смешанного газа, °C", font=customtkinter.CTkFont(size=10, weight="bold"), justify='center', text_color="#ffffff")
        self.t_gas.grid(row=0, column=0, padx=10, columnspan=2, pady=(5,0))

        self.t_gas_l = customtkinter.CTkLabel(self.t_gas_form, text="     Tг =   ", font=customtkinter.CTkFont(size=10, weight="bold"), justify='center', anchor='w', text_color="#ffffff")
        self.t_gas_l.grid(row=1, column=0, padx=(10, 0), pady=0)

        self.t_gas_v = customtkinter.CTkEntry(self.t_gas_form, height=20, width=150)
        self.t_gas_v.grid(row=1, column=1, padx=(0, 10), pady=0)

        # Ввод коэффициента расхода воздуха
        self.air_con_form = customtkinter.CTkFrame(self, fg_color='transparent')
        self.air_con_form.grid(row=3, column=0, padx=0, pady=0)

        self.air_con = customtkinter.CTkLabel(self.air_con_form, text="Коэффициент расхода воздуха", font=customtkinter.CTkFont(size=10, weight="bold"), justify='center', text_color="#ffffff")
        self.air_con.grid(row=0, column=0, padx=10, columnspan=2, pady=(5,0))

        self.air_con_l = customtkinter.CTkLabel(self.air_con_form, text="     ld =   ", font=customtkinter.CTkFont(size=10, weight="bold"), justify='center', anchor='w', text_color="#ffffff")
        self.air_con_l.grid(row=1, column=0, padx=(10, 0), pady=(0,5))

        self.air_con_v = customtkinter.CTkEntry(self.air_con_form, height=20, width=150)
        self.air_con_v.grid(row=1, column=1, padx=(0, 10), pady=(0,5))

        self.update()

    def update(self):
        self.pir_cf_v.delete(0, 200)
        self.pir_cf_v.insert(0, self.database.get_parameters("Пирометрический коэффициент").value)
        self.t_air_v.delete(0, 200)
        self.t_air_v.insert(0, self.database.get_parameters("Температура подогрева воздуха").value)
        self.t_gas_v.delete(0, 200)
        self.t_gas_v.insert(0, self.database.get_parameters("Температура смешанного газа").value)
        self.air_con_v.delete(0, 200)
        self.air_con_v.insert(0, self.database.get_parameters("Коэффициент расхода воздуха").value) # "1.4258920266676125"
