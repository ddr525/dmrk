import customtkinter as ctk
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utilities import toFixed

class GraphView(ctk.CTkScrollableFrame):

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

        if "График" not in self.page.get_heating_data():
            return

        graph = self.page.get_heating_data()["График"]
        
        # Преобразование данных в numpy массивы
        t = np.array(graph["t"])
        time_H = float(graph["время"])  # Преобразуем в float для надежности
        twG = np.array(graph["Печь (верх)"])
        twnG = np.array(graph["Печь (низ)"])
        tmvG = np.array(graph["Металл (верх)"])
        tmcG = np.array(graph["Металл (центр)"])
        tmnG = np.array(graph["Металл (низ)"])

        # Создание фигуры
        fig, ax = plt.subplots(figsize=(5, 7), dpi=100)
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)

        # Построение графиков
        ax.plot(t, twG, label="Печь (верх)", color="red", linewidth=1.5)
        ax.plot(t, twnG, label="Печь (низ)", color="orange", linewidth=1.5)
        ax.plot(t, tmvG, label="Металл (верх)", color="green", linewidth=1.5)
        ax.plot(t, tmcG, label="Металл (центр)", color="purple", linewidth=1.5)
        ax.plot(t, tmnG, label="Металл (низ)", color="blue", linewidth=1.5)

        # Настройки графика
        ax.set_xlabel("Время нагрева (мин)", fontsize=12)
        ax.set_ylabel("Температура (°C)", fontsize=12)
        ax.set_title("Температурный режим нагрева", fontsize=14)
        ax.legend(fontsize=10, loc='best')
        ax.grid(True, linestyle="--", alpha=0.5)

        # Настройки осей с проверкой данных
        ax.set_xticks(np.arange(0, time_H + 1, 10))
        ax.set_yticks(np.arange(0, max(1500, int(max(twG.max(), twnG.max(), 
                                                    tmvG.max(), tmcG.max(), 
                                                    tmnG.max())) + 100), 100))
        
        # Автоматическая подстройка пределов
        ax.set_xlim(0, time_H)
        ax.set_ylim(0, None)

        # Вставка графика в интерфейс
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=(50, 0), padx=50)
        self.canvas.draw()
            
