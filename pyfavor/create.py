""" """
from typing import List, Dict, Any, Literal, Tuple, Optional
import pandas as pd
import wntr
from .utils import hr_to_sec, hr_to_min, find_os, install_package
from .simulate import get_junction_pressures


WNTRSimulationResults = wntr.sim.results.SimulationResults


def get_logger_info(efavor_logger_file: str) -> pd.DataFrame:
    return pd.read_excel(efavor_logger_file, sheet_name="loggers")
    
    
def get_notes(efavor_logger_file: str) -> pd.DataFrame:
    notes = pd.read_excel(efavor_logger_file, sheet_name = "notes", header=None)
    return notes


def create_times_df(start_time: int, measurement_time: int) -> pd.DataFrame:
    """Create a dataframe with start time and the measurement times for efavor"""
    data = {
        'name': ["Start time (minutes after midnight)", "Measurements time step (minutes)"],
        'value': [start_time, measurement_time]}
    return pd.DataFrame(data)
    
    
def create_flows_df(
        inlet_logger_id: int, 
        flows: List[float], 
        flow_setting: Literal["15min", "1hr"],
        n_meas: int) -> pd.DataFrame:
    """Create a dataframe of flows from inlet loggers
    Args:
        inlet_logger_id: Value of inner logger required to name the column
        flows: List of flows recorded from the logger
        flow_setting: If 1hr then flow is recorded as first value from the list
            of four values for each our taken at 15 min intervals. If 15min
            then all flows at 15 min intervals for each our are used in the
            dataframe.
        n_meas: number of flow measurements in a pressure step.
    Returns:
        A dataframe to be entered into the (multi-sheet) Excel file
    """
    column_names = ['Flowmeter ID → Set of inlets ↓']
    column_names.append(inlet_logger_id)
    data = {}
    if flow_setting == "1hr":
        data[column_names[0]] = ["A" for _ in flows]
    elif flow_setting == "15min":
        data[column_names[0]] = [
            "A" if not index % n_meas else "" for index, _ in enumerate(flows)]
    else:
        raise ValueError(
            f"Flow setting has to be '1hr' or '15min'. '{flow_setting}' given.")     
    data[column_names[1]] = flows
    df = pd.DataFrame(data)
    return df


def create_inlets_df(
        inlet_junction_id: Any, 
        id_to_junction_map: Dict[int, int], 
        valve_id: Any,
        pressure_setpoints: Optional[List[float]] = None) -> pd.DataFrame:
    """Create a dataframe containing information for efavor about inlets
    Args:
        inlet_junction_id: 
        id_to_junction_map:
        valve_id:
        pressure_setpoints: list of pressure setpoints
    """
    epanet_ids = [junction_id for junction_id in [inlet_junction_id]]
    flowmeter_ids = [id_to_junction_map.get(value, value) for value in epanet_ids]
    set_of_inlets = ["A" for _ in flowmeter_ids]
    data = {
        'Flowmeter ID': flowmeter_ids,
        'EPANET valve ID': [valve_id],
        'Set of inlets': set_of_inlets}
    if pressure_setpoints is None:
        setpoints = ["!!!TO BE SET MANUALLY!!!" for _ in flowmeter_ids]
    else:
        # Consider numerical values
        try:
            num_pressure_setpoints = len(pressure_setpoints)
        except TypeError:
            print(f"pressure_setpoints must be a list or None {type(pressure_setpoints)} given.")
        if len(pressure_setpoints) == 1:
            setpoints = [pressure_setpoints[0] for _ in flowmeter_ids]
            data.update({'PRV pressure setpoints [m]': setpoints})
        else: # len > 1
            for ix, item in enumerate(pressure_setpoints):
                setpoints = [item for _ in flowmeter_ids]
                if ix == 0:
                    data.update({'PRV pressure setpoints [m]': setpoints})
                else:
                    added_col_name = "p_"+str(ix+1)
                    data.update({added_col_name: setpoints})
    return pd.DataFrame(data)


def create_pressures_df(
        junction_ids: List[str], 
        results, 
        n_meas: int,
        start_time: int,
        end_time: int,
        epanet_to_logger_id_map: dict) -> pd.DataFrame:
    """ """
    
    pressure_data = get_junction_pressures(junction_ids, results, start_time, end_time)
    # Create a Pandas DataFrame from the extracted pressures
    # Remove last row, i.e. exclude the last hour
    pressure_df = pd.concat(pressure_data, axis=1, keys=junction_ids).iloc[:-1]
    # Create a new column with the specified name
    first_column_name = "Logger ID → Set of inlets ↓"
    pressure_df[first_column_name] = ''
    pressure_df = pressure_df[
        pressure_df.columns[-1:].tolist() + 
        pressure_df.columns[:-1].tolist()
    ]
    for num_entries, i in enumerate(range(0, len(pressure_df))):
        if not i % n_meas:
            pressure_df.iloc[i,0] = 'A'
    # Rename the column headers from EPANET Ids to EFavor Logger IDs
    pressure_df = pressure_df.rename(columns=epanet_to_logger_id_map)
    return pressure_df
    
    
def read_pressure_setpoints(pressure_df: pd.DataFrame) -> List[float]:
    """Reads pressure setpoints from pressure dataframe"""
    first_column_name = "Logger ID → Set of inlets ↓"
    # Find pressure setpoints - supports different step/measurement arrangments
    filtered_df = pressure_df[
        pressure_df[first_column_name].notna() & 
        pressure_df[first_column_name].astype(bool)]
    # Get values from the first column
    pressure_setpoints = filtered_df.iloc[:,1].tolist()
    return pressure_setpoints


def write_efavor_pressures(
        efavor_pressure_file: str,
        logger_info: pd.DataFrame,
        inlets_df: pd.DataFrame,
        pressure_df: pd.DataFrame,
        flows_df: pd.DataFrame,
        times_df: pd.DataFrame,
        notes: pd.DataFrame) -> None:
    """Create the Excel file for efavor"""
    with pd.ExcelWriter(efavor_pressure_file) as writer:
        logger_info.to_excel(writer, sheet_name="loggers", index=False)
        inlets_df.to_excel(writer, sheet_name = "inlets", index = False)
        pressure_df.to_excel(writer, sheet_name = "pressure_measurements", index = False)
        flows_df.to_excel(writer, sheet_name = "flow_measurements", index = False)
        times_df.to_excel(writer, sheet_name = "times", index=False, header=False)
        notes.to_excel(writer, sheet_name="notes", index=False, header=False)
    if find_os != "windows":
        return
    print("For windows system we're rewriting the Excel file from Pandas info FileFormat=56")
    try:
        from win32com.client import Dispatch
    except ModuleNotFoundError:
        try:
            install_package(package_name='pywin32')
        except subprocess.CalledProcessError:
            print("Cannot install pywin32. Not available in pip.")
            print("Saving to Excel fileformat 56 not possible.")
            return
    # Rewrite the excel file to work with FileFormat 56
    xl = Dispatch('Excel.Application')
    wb = xl.Workbooks.Add(efavor_pressure_file.as_posix())
    wb.SaveAs(efavor_pressure_file.as_posix()[:-1], FileFormat=56)
    wb.SaveAs(efavor_pressure_file.as_posix(), FileFormat=56)
    xl.Quit() 
