import numpy as np
import customtkinter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from utilities import split_string

class DatasetWindow(customtkinter.CTkToplevel):

    def __init__(self, frame, database, title):
        super().__init__()

        self.title("Просмотр данных")

        self.database = database

        width = 680
        height = 580
        spawn_x = int((self.winfo_screenwidth()-width)/2) 
        spawn_y = int((self.winfo_screenheight()-height)/2)

        self.geometry(f"{width}x{height}+{spawn_x}+{spawn_y}")

        self.protocol("WM_DELETE_WINDOW", self.closed)

        # Каркас для графика
        # frame = customtkinter.CTkFrame(self)
        # frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Создание фигуры
        self.fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.fig.patch.set_alpha(0)  # Прозрачный фон фигуры
        ax.patch.set_alpha(0)   # Прозрачный фон осей
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        if isinstance(title, dict):
            co2 = self.database.get_exp_result("CO2")
            n2 = self.database.get_exp_result("N2")
            h2o = self.database.get_exp_result("H2O")
            o2 = self.database.get_exp_result("O2")

            # x = np.linspace(1, len(co2), len(co2))

            x = [el.experiment_id for el in co2]

            co2 = [el.value for el in co2]
            n2 = [el.value for el in n2]
            h2o = [el.value for el in h2o]
            o2 = [el.value for el in o2]

            name = "Состав дыма"
            leg = "%"

            # Построение графика
            ax.plot(x, co2, label="CO2", color="#2196F3", linewidth=2)
            ax.plot(x, n2, label="N2", linewidth=2)
            ax.plot(x, h2o, label="H2O", linewidth=2)
            ax.plot(x, o2, label="O2", linewidth=2)

            ax.set_title("Состав дыма", fontsize=14)
            ax.set_xlabel("Опыт", fontsize=12)
            ax.set_ylabel(leg, fontsize=12)
            ax.grid(alpha=0.5, linestyle="--")
            ax.legend()

            # Вставка графика в интерфейс
            canvas = FigureCanvasTkAgg(self.fig, master=self)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()
        else:
            # Получение данных из базы
            data = self.database.get_exp_result(title)

            count = [idx.experiment_id for idx in data]
            data = [idx.value for idx in data]

            # Разделение на наименование и количественную характеристику
            name, leg = split_string(title)

            # Генерация данных
            # x = np.linspace(1, count, count)
            x = np.array(count)
            y = np.array(data)

            # Построение графика
            ax.plot(x, y, label=name, color="#2196F3", linewidth=2)
            ax.set_title(title, fontsize=14)
            ax.set_xlabel("Опыт", fontsize=12)
            ax.set_ylabel(leg, fontsize=12)
            ax.grid(alpha=0.5, linestyle="--")
            ax.legend()

            # Вставка графика в интерфейс
            canvas = FigureCanvasTkAgg(self.fig, master=self)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()

    def closed(self):
        # Очистка фигур
        plt.close(fig=self.fig)
        plt.close('all')

        self.destroy()
        




