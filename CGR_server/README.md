# CGR_server

Code for the user study of the Paper Collaborative Graph Repair under Denial Constraints.

## Installation

Navigate into the repository and create a python virtual environment.

```bash
python3 -m venv env
#activate
source env/bin/activate
#stop it
deactivate
```
Then install the python requirements

```bash
pip3 install -r /path/to/requirements.txt
```
## Requirements and Setup

Create an instance on AuraDB and get the connection string.


Inside app > app, set your DB Connection string : 
```python
config.DATABASE_URL = "YOUR AURADB CONNECTION STRING" 
```
## Dataset configuration

### StarWars ###
On the AuraDB panel, run the cypher script in the config folder (sw.cypher).
Then, Run the update.cypher script to inject the inconsistencies.
## Run the experiment


```bash
python3 app.py 
```

Visit localhost:5000 to access the interface.

