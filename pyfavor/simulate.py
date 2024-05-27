""" """
from typing import List, Literal
import wntr
WNTRSimulationResults = wntr.sim.results.SimulationResults


def simulate_network(network_file: str) -> WNTRSimulationResults:
    """ """
    wn = wntr.network.WaterNetworkModel(network_file)
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    return results
    

def get_junction_pressures(
        junction_ids: List[str], 
        results: WNTRSimulationResults, 
        start_time: int, 
        end_time: int) -> List[float]:
    """ start_time and end_time in seconds"""
    pressure_data: List[float] = []
    for node_name in junction_ids:
        node_pressures = results.node['pressure'].loc[start_time:end_time, node_name]
        pressure_data.append(node_pressures)
    return pressure_data
    

def get_inlet_flows(
        results:WNTRSimulationResults, 
        flow_setting: Literal['15min', '1hr'],
        inlet_pipe: str,
        start_time: int, 
        end_time: int) -> List[float]:
    """ start_time and end_time in seconds"""
    flow_data_df = results.link['flowrate'][inlet_pipe]\
        .loc[start_time:end_time]\
        .iloc[:-1] * 3_600 # WNTR produces flows in m3/s
    if flow_setting == "1hr":
        inlet_flows = [
            flow for iter, (_, flow) in enumerate(flow_data_df.items()) 
            if not iter % n_meas]
    elif flow_setting == "15min":
        inlet_flows = [
            flow for iter, (_, flow) in enumerate(flow_data_df.items())]
    else:
        raise ValueError(
            f"Flow setting has to be '1hr' or '15min'. '{flow_setting}' given."
        )
    return inlet_flows
