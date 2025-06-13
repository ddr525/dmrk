import customtkinter
import tksvg
from functools import partial

class ExperimentWindow(customtkinter.CTkToplevel):
    def __init__(self, database, page):
        super().__init__()

        self.title("Просмотр опытов")

        self.database = database

        self.master = page

        width = 560
        height = 640
        spawn_x = int((self.winfo_screenwidth()-width)/2) 
        spawn_y = int((self.winfo_screenheight()-height)/2)

        self.geometry(f"{width}x{height}+{spawn_x}+{spawn_y}")

        self.protocol("WM_DELETE_WINDOW", self.closed)

        self.frame = customtkinter.CTkScrollableFrame(self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame.grid(row=0, column=0, sticky="nsew")

        self.text_color = 'white'

        self.update()

    def clear_widgets(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def update(self):
        self.clear_widgets()

        title = customtkinter.CTkLabel(self.frame, text="Просмотр опытов", font=customtkinter.CTkFont(size=16, weight='bold'), text_color=self.text_color)
        title.pack(pady=10, padx=10, expand=True)

        exps = self.database.get_experiments("Расчет горения топлива")
        
        i = 1
        for e in exps:
            frame = customtkinter.CTkFrame(self.frame, fg_color="#333333")

            frame.pack(pady=10, padx=10, expand=True)
            
            num = customtkinter.CTkLabel(frame, text=f"{i})", text_color=self.text_color)
            num.grid(row=0, column=0, padx=(10), sticky="nsew")

            label = customtkinter.CTkLabel(frame, text="Опыт — " + str(e.id), text_color=self.text_color)
            label.grid(row=0, column=1, padx=(10), sticky="nsew")

            res = [result for result in e.results if result.parameter == "Доменный газ, %"][0]

            blast_gas = customtkinter.CTkLabel(frame, text=f"({res.parameter} : {str(res.value)})", text_color=self.text_color)
            blast_gas.grid(row=0, column=2, padx=(10), sticky="nsew")

            svg_image_close = tksvg.SvgImage(file="icons/close_18dp_5F6368_FILL0_wght700_GRAD200_opsz20.svg")
            svg_image_open = tksvg.SvgImage(file="icons/open_in_new_18dp_FFFFFF_FILL0_wght400_GRAD0_opsz20.svg")

            button = customtkinter.CTkButton(frame, width=20, image=svg_image_open, text="", fg_color="#4f4f4f", hover_color="gray", corner_radius=5, command=partial(self.open, e.id))
            button.grid(row=0, column=3, padx=(5, 10), pady=10)

            button = customtkinter.CTkButton(frame, width=20, image=svg_image_close, text="", fg_color="#4f4f4f", hover_color="gray", corner_radius=5, command=partial(self.delete, e.id))
            button.grid(row=0, column=4, padx=(5, 10), pady=10)

            i += 1

        clear_button = customtkinter.CTkButton(self.frame, text="Очистить все", fg_color="#4f4f4f", hover_color="gray", corner_radius=5, command=partial(self.clear_all), state='normal')
        clear_button.pack(pady=10)

    def open(self, id):
        self.master.open_exp(id)

    def delete(self, id):
        self.database.delete_exp_by_id(id)
        self.master.delete_exp_nummber(id)
        self.update()

    def clear_all(self):
        self.database.delete_all_exp()
        self.master.set_exp_number(0)
        self.closed()

    def closed(self):
        self.destroy()

