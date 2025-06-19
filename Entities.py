from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# Создаем базу данных
Base = declarative_base()

# Таблица gases
class Gas(Base):
    __tablename__ = "gases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    mixed_percentage = Column(Float, nullable=False)

    components = relationship("GasComponent", back_populates="gas")

# Таблица gas_components
class GasComponent(Base):
    __tablename__ = "gas_components"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gas_id = Column(Integer, ForeignKey("gases.id"), nullable=False)
    component = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    units = Column(String, nullable=False)

    gas = relationship("Gas", back_populates="components")

# Таблица global_parameters
class GlobalParameter(Base):
    __tablename__ = "global_parameters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parameter = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    units = Column(String, nullable=False)
    value_str = Column(String, nullable=True)

class MetalResults(Base):
    __tablename__ = 'metal_results'
    id = Column(Integer, primary_key=True)

    experiment_id = Column(Integer, ForeignKey("experiment.id"), nullable=False)

    experiment = relationship("Experiment", back_populates="metal_results")

    zones = relationship("HeatingZone", back_populates="metal")

    parameters = relationship("OverallHeatingData", back_populates="metal")

# Таблица зон нагрева
class HeatingZone(Base):
    __tablename__ = 'heating_zones'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    parameters = relationship("HeatingParameter", back_populates="zone")
    
    metal_id = Column(Integer, ForeignKey("metal_results.id"), nullable=False)
    metal = relationship("MetalResults", back_populates="zones")

# Таблица параметров нагрева в зонах
class HeatingParameter(Base):
    __tablename__ = 'heating_parameters'

    id = Column(Integer, primary_key=True)
    zone_id = Column(Integer, ForeignKey('heating_zones.id'), nullable=False)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    units = Column(String, nullable=False)

    zone = relationship("HeatingZone", back_populates="parameters")

# Таблица общих характеристик нагрева
class OverallHeatingData(Base):
    __tablename__ = 'overall_heating_data'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    units = Column(String, nullable=False)

    metal_id = Column(Integer, ForeignKey("metal_results.id"), nullable=False)
    metal = relationship("MetalResults", back_populates="parameters")

class FurnaceBalance(Base):
    __tablename__ = 'balances'

    id = Column(Integer, primary_key=True)

    experiment_id = Column(Integer, ForeignKey("experiment.id"), nullable=False)

    experiment = relationship("Experiment", back_populates="balance_results")

    zones = relationship("ZoneResult", back_populates="balance")

class ZoneResult(Base):
    __tablename__ = 'zones'

    id = Column(Integer, primary_key=True)
    
    name = Column(String, nullable=False)

    params = relationship("HeatParameter", back_populates="zone")
    heat_flows = relationship("HeatFlow", back_populates="zone")

    balance_id = Column(Integer, ForeignKey("balances.id"), nullable=False)
    balance = relationship("FurnaceBalance", back_populates="zones")

class HeatParameter(Base):
    __tablename__ = 'heat_param'
    id = Column(Integer, primary_key=True)
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=False)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    units = Column(String, nullable=False)

    zone = relationship("ZoneResult", back_populates="params")

class HeatFlow(Base):
    __tablename__ = 'heat_flows'

    id = Column(Integer, primary_key=True)
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=False)
    type = Column(String, nullable=False)  # "Приход тепла" или "Расход тепла"

    details = relationship("HeatFlowDetail", back_populates="heat_flow")
    zone = relationship("ZoneResult", back_populates="heat_flows")

class HeatFlowDetail(Base):
    __tablename__ = 'heat_flow_details'

    id = Column(Integer, primary_key=True)
    heat_flow_id = Column(Integer, ForeignKey('heat_flows.id'), nullable=False)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    units = Column(String, nullable=False)

    heat_flow = relationship("HeatFlow", back_populates="details")

class HeatGraph(Base):
    __tablename__ = "heat_graph"

    id = Column(Integer, primary_key=True)

    experiment_id = Column(Integer, ForeignKey("experiment.id"), nullable=False)

    experiment = relationship("Experiment", back_populates="heat_graphs")

    params = relationship("GraphParam", back_populates="heat_graph")
    dots = relationship("GraphDots", back_populates="heat_graph")

class GraphParam(Base):
    __tablename__ = "graph_param"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)

    heat_graph_id = Column(Integer, ForeignKey('heat_graph.id'), nullable=False)
    heat_graph = relationship("HeatGraph", back_populates="params")

class GraphDots(Base):
    __tablename__ = "graph_dots"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    heat_graph_id = Column(Integer, ForeignKey('heat_graph.id'), nullable=False)
    heat_graph = relationship("HeatGraph", back_populates="dots")

    data = relationship("GraphData", back_populates="dot")

class GraphData(Base):
    __tablename__ = "graph_data"

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)

    dot_id = Column(Integer, ForeignKey('graph_dots.id'), nullable=False)
    dot = relationship("GraphDots", back_populates="data")


# Таблица Experiment
class Experiment(Base):
    __tablename__ = "experiment"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    created = Column(DateTime, default=func.now())

    results = relationship("ExperimentResult", back_populates="experiment")

    metal_results = relationship("MetalResults", back_populates="experiment")

    balance_results = relationship("FurnaceBalance", back_populates="experiment")

    heat_graphs = relationship("HeatGraph", back_populates="experiment")

    history_gases = relationship("HistoryGas", back_populates="experiment")
    history_parameters = relationship("HistoryGlobalParameter", back_populates="experiment")

# Таблица ExperimentResult
class ExperimentResult(Base):
    __tablename__ = "experiment_result"

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiment.id"), nullable=False)
    parameter = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    units = Column(Float, nullable=True)

    experiment = relationship("Experiment", back_populates="results")

class GasMetalParameter(Base):
    __tablename__ = "gas_metal_params"

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiment.id"), nullable=False)
    parameter = Column(String, nullable=False)
    value = Column(Float, nullable=False)

# Связь между Experiment и HistoryGas
class HistoryGas(Base):
    __tablename__ = "history_gases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    experiment_id = Column(Integer, ForeignKey("experiment.id"))
    name = Column(String, nullable=False)
    mixed_percentage = Column(Float, nullable=False)

    components = relationship("HistoryGasComponent", back_populates="gas")
    experiment = relationship("Experiment", back_populates="history_gases")

class HistoryGasComponent(Base):
    __tablename__ = "history_gas_components"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gas_id = Column(Integer, ForeignKey("history_gases.id"))
    component = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    units = Column(String, nullable=False)

    gas = relationship("HistoryGas", back_populates="components")

# Связь между Experiment и HistoryGlobalParameter
class HistoryGlobalParameter(Base):
    __tablename__ = "history_global_parameters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    experiment_id = Column(Integer, ForeignKey("experiment.id"))
    parameter_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    units = Column(String, nullable=False)
    value_str = Column(String, nullable=False)

    experiment = relationship("Experiment", back_populates="history_parameters")


    