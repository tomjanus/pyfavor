# `pyfavor` - A Python package automating the execution of EPANET and EFAVOR

## Short description
This repository contains the source code for automating the interoperability between water distribution network (WDN) simulation with WNTR and EFAVOR - a software written in C# for locating bursts in water distribution networks.

WNTR (https://github.com/USEPA/WNTR) uses the EPANET solver to calculate water distribution networks.

EFAVOR is a software suite for locating bursts by active identification via monitoring of pressures in selected nodes and flows in the inlet node while pressure nsp and down in a controlled manner, e.g. 1 meter every hour. EFAVOR selects best pressure measurement locations for active identification and uses the recorded data for locating bursts.

This repository facilitates testing performance of EFAVOR on different network structures and experiment designs, where the actual network is replaced by a simulator.

## Disclaimer
This repository has been written to aide analysis in an engineering project where the users need to use a simulator in place of a real water distribution netowrk to evaluate the efficacy of an active burst detection method prior to real-world deployment. For such an analysis we need to automate some of the steps that would normally be done manually, such as recording pressures and flows in the experiment in excel tables, etc. and interact with EPANET simulator as if it were a physical network with/without bursts. 

Since the aim was to quickly automate the analysis process, this source code is not finished. In particular, the command line functionality has not been implemented. The use of the software is permitted for everyone but I cannot guarantee its correctness. It may be buggy and incomplete in places.

## Usage
The tool can be used either as a library (collection of functions) or as a command-line application. In the latter case, the library requires prior installation; see the next section.

In order to run command-line functions (provided that the application had been installed) type the following:
```sh
run-pyfavor --help
```
This command will provide usage instructions and execution options.

The package comes with example code in the Jupyter Notebook:`create_efavor_inputs_demo.ipynb`

## Installation
In order to use command-line functions, install the package by typing
```
pip install -e .
```
or
```
pip install .
```
in the root folder where files `setup.py` and `setup.cfg` are located. The first command installs the package in editable format by creating links between installation directory in your Python virtual environment and the source code repository. In this way, any changes made to the source-code have automatic effect on code execution, without needing any prior re-installation. On contrary, the second command copies and builds the package inside the virtual environment and thus, the source-code and the running version of the package are decoupled.

The installation step is not required to import and execute any of the library functions and to run `create_efavor_inputs_demo.ipynb`.
