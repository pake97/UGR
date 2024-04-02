# CGR_Experiments

Code for the simulations of the Paper Collaborative Graph Repair under Denial Constraints.

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

Download and configure [neo4j-community-5.12.0](https://neo4j.com/deployment-center/).

Download and install the [GDS (Graph Data science) plugin](https://neo4j.com/docs/graph-data-science/current/installation/).

Download and install the [Apoc plugin](https://neo4j.com/labs/apoc/4.1/installation/).

Download and install the [Apoc extended](https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases).


Inside utils > neo4j_connector.py, set your DB Connection string : 
```python
config.DATABASE_URL = #your neo4j conenction string "bolt://username:password@localhost:7687/DBNAME"
```
and set the path to your local neo4j community directory for automatic dataset loading.
```python
 try:
     os.system('PATH_TO_NEO4J_COMMUNITY/bin/cypher-shell -u YOUR_USERNAME -p YOUR_PASSWORD -f ./config/'+dataset+'.cypher')
 except Exception as e:
     print(e)
```

**Inside the neo4j-community folder:**

Add file conf > apoc.conf

```bash
apoc.export.file.enabled=true
apoc.import.file.enabled=true 
```

Update neo4j.conf and neo4j-admin.conf for memory configuration. Example:

```bash
server.memory.heap.initial_size=64g
server.memory.heap.max_size=64g

...

server.memory.pagecache.size=48g
```

update neo4j.conf for allowing apoc and gds plugins : 

```bash
dbms.security.allow_csv_import_from_file_urls=true

...

dbms.security.procedures.unrestricted=gds.*,apoc.monitor.kernel,apoc.*

dbms.security.procedures.allowlist=gds.*,apoc.*,apoc.load.*,apoc.load.csv,apoc.data.*,apoc.coll.*,apoc.import.file,apoc.cypher.parallel,apoc.cypher.*,apoc.monitor.*,apoc.monitor.kernel,algo.*,algo.betweenness.stream

```
## Dataset configuration

### StarWars, Stackoverflow , wwc2019 , Fincen ###

Move the files from the Dataset_files folder into neo4j-community > import folder 

### Synthea ###





To load synthea in Neo4j, set the config file : config > synthea.yml : 
```yml
server_uri: bolt://localhost:7687/
admin_user: YOUR_NEO4J_USERNAME
admin_pass: YOUR_NEO4J_PASSWORD

files:
  # payers
  - url: file://PATH_TO_THIS_DIRECTORY/config/output/csv/payers.csv # repeat for every url
```
## Run a simulation


```bash
python3 environment.py dataset safety assignment users answer
```
**params :** \
dataset : sw (StarWars), stackoverflow, wwc2019, synthea, fincen.


safety: True, False.


assignment: random, betweennessDesc (betweenness descending order), betweennessAsc (betweenness ascending order), degreeDesc (degree descending order), degreeAsc (degree ascending order), prDesc(PageRank descending order) prAsc (PageRank ascending order).


users : 5,10,15,20,....

answer : [0,1]

## Run the entire experiment

A premade bash script run all the simulations of the paper.

```bash
./run.sh > ouput.txt
```

## Run a simulation with preferred repair


```bash
python3 preferred_environment.py dataset safety mode	
```
**params :** \
dataset : sw (StarWars), stackoverflow, wwc2019, synthea, fincen.


safety: True, False.


mode : 'label'(Label preferred repair),  'delete'(Delete preferred repair),  'update'(Update preferred repair),  'number'(Number of operations preferred repair).

## Run the entire experiment for preferred repairs

A premade bash script run all the simulations of the paper.

```bash
./run_preferred.sh > ouput_preferred.txt
```

## Parse the results

To parse the resuls, inside the parser script change the filename for your output file and run: 

```bash
python3 parser.py
python3 preferred_parser.py
```


To plot the results, use the plot scripts by updating the file to read your outup file.