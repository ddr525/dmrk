import numpy as np
import customtkinter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from tables.BalanceTableView import BalanceTableView
from tables.FuilTableView import FuilTableView
from tables.GraphView import GraphView
from tables.MetalTableView import MetalTableView

class TableViewPage(customtkinter.CTkTabview):

    def on_tab_change(self):
        if(self.get() == "Параметры горения топлива"):
            self.current_view = self.fuil
        elif(self.get() == "Параметры нагрева металла"):
            self.current_view = self.metal
        else:
            self.current_view = self.balance

        #print(self.current_view)

    def _size(self, event):
        if(event.width < 1100 and not self.small):
            self.small = True
            self.resize = True
        elif(event.width >= 1100 and self.small):
            self.small = False
            self.resize = True
            
        if(self.resize):
            if(self.small):
                self.fuil.grid_configure(padx=50, pady=50)
                self.metal.grid_configure(padx=50, pady=50)
                self.balance.grid_configure(padx=50, pady=50)
            else:
                self.fuil.grid_configure(padx=150, pady=50)
                self.metal.grid_configure(padx=150, pady=50)
                self.balance.grid_configure(padx=150, pady=50)

            self.resize = False

    def __init__(self, master, root, page, database, *args, **kwargs):
        super().__init__(master, **kwargs)

        self.database = database
        self.page = page
        self.root = root

        self.small = False
        self.resize = False

        # create tabs
        self.add("Параметры горения топлива")
        self.add("Параметры нагрева металла")
        self.add("Параметры теплового баланса")
        self.add("График")

        self.tab("Параметры горения топлива").columnconfigure((0), weight=1)
        self.tab("Параметры горения топлива").rowconfigure((0), weight=1)

        self.tab("Параметры нагрева металла").columnconfigure((0), weight=1)
        self.tab("Параметры нагрева металла").rowconfigure((0), weight=1)

        self.tab("Параметры теплового баланса").columnconfigure((0), weight=1)
        self.tab("Параметры теплового баланса").rowconfigure((0), weight=1)

        self.tab("График").columnconfigure((0), weight=1)
        self.tab("График").rowconfigure((0), weight=1)

        self.fuil = FuilTableView(master=self.tab("Параметры горения топлива"), page=page, root=master, database=self.database)
        self.metal = MetalTableView(master=self.tab("Параметры нагрева металла"), page=page, root=master, database=self.database)
        self.balance = BalanceTableView(master=self.tab("Параметры теплового баланса"), page=page, root=master, database=self.database)
        self.graph = GraphView(master=self.tab("График"), page=page, root=master, database=self.database)

        #self.table = TableViewPage(master=self.tab("Табличный вид"), page=self.cards, root=master, database=self.database)

        self.fuil.grid(row=0, column=0, sticky="nsew")
        self.metal.grid(row=0, column=0, sticky="nsew")
        self.balance.grid(row=0, column=0, sticky="nsew")
        self.graph.grid(row=0, column=0, sticky="nsew")
        #self.table.grid(row=0, column=0, sticky="nsew")

        self.columnconfigure((0), weight=1)
        #self.rowconfigure((0), weight=1)

        self.current_view = self.fuil

        # Отслеживание изменения вкладки
        self.configure(command=self.on_tab_change)

        #self.update()

    def update(self):
        self.fuil.update()
        self.metal.update()
        self.balance.update()
        self.graph.update()

