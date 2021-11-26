# Microtransat Simulator

## Getting started

### Prerequisites

* Python >= 3.8
* Latest version of Pip
* Simpylc >= 3.8.4

- pip uninstall pyopengl
- pip install PyOpenGL-3.1.5-cp39-cp39-win_amd64.whl --force-reinstall
- pip install PyOpenGL_accelerate-3.1.5-cp39-cp39-win_amd64.whl --force-reinstall
- restart pc

### Installation

#### Windows
1. Create a new virtual environment.
```bash
python -m venv env
```
2. Activate the virtual environment.
```bash
.\env\Scripts\activate
```
3. Clone the repository.
```bash
git clone git@github.com:S-Vrijenhoek/Microtransat-Sim.git
``` 
4. Install the specified library that is required to run this project.
```bash
pip install simpylc
``` 

### Usage

1. To add a new file to the simulator it needs to be imported inside world.py and added to line 7

2. To add objects to the world, they need to be added in visualisation.py

3. In the simpylc library folder there are multiple examples that can be used to create different functionality within the simulation.
