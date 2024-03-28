import threading
import random
import time
import math
import numpy as np
from cgr.grdg3 import GRDG
from utils.injectInconsistencies2 import injectInconsistencies
from utils.injectFixedInconsistencies import injectFixedInconsistencies
from utils.injectSyntheticData import injectSyntheticData
from config.config import DATABASE_URL
from utils.neo4j_connector import Neo4jConnector
from utils.checkConstraintsM import checkConstraints
from config.movies_query import movies_queries
from config.fincen_query import fincen_queries
from config.stackoverflow_query import stackoverflow_query
from config.wwwc2019_query import wwwc2019_query
from utils.computeRepairs4 import computeRepairs
from utils.checkSafety3 import checkSafety
from utils.applyRepair import applyRepair
from utils.restore_graph import restore_graph
from config.sw_query import sw_queries
from utils.restoreConstraints2 import restoreConstraints
from utils.compute_metrics2 import compute_metrics
from agent.user2 import User
from config.synthea_query import synthea_query
import sys
class CGREnvironment:
    def __init__(self, max_users=5, dataset="movies",safetiness= False, timeout=3600, assignment="random",error_distribution=[0.5,0.5,0.5,0.5], SEED = 1, user_distribution=[0.3,0.2,0.5], answer_distribution=[1,0]):
        self.max_users = max_users
        self.users = self.generateUsers(max_users)
        self.counter = 0
        self.lock = threading.Lock()
        self.running = False
        self.grdg = GRDG(SEED, assignment)
        self.dataset = dataset
        self.constraints = self.loadConstraints(dataset)
        self.wait_count=0
        self.iteration_count=0
        self.interaction_count=0
        self.avg_wait_count=0
        self.avg_iteration_count=0
        self.avg_interaction_count=0
        self.avg_recall=0
        self.avg_precision=0
        self.avg_f1=0
        self.safetiness = safetiness
        self.timeout = timeout
        self.neo4j_Connector = Neo4jConnector(DATABASE_URL)
        self.violation_dict={}
        self.assignment = assignment
        self.error_distribution = error_distribution
        self.SEED = SEED
        self.answer_distribution=answer_distribution

    def start_fixed_arrival_simulation(self):
        #print("Clearing dataset")
        self.neo4j_Connector.clearNeo4j()
        #print("Loading dataset")
        self.neo4j_Connector.loadDatasetToNeo4j(self.dataset)
        if(self.neo4j_Connector.query("RETURN gds.graph.exists('grdg')")[0]["gds.graph.exists('grdg')"]):
            self.neo4j_Connector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
        for seed2 in range(1,11):
            self.wait_count=0
            self.iteration_count=0
            self.interaction_count=0
            t0 = time.time()
            injectSyntheticData(self.neo4j_Connector)
            
            to_inject=injectInconsistencies(self.neo4j_Connector,self.constraints,self.error_distribution,self.SEED)
            
            
            
            
            violations_ids = checkConstraints(self.constraints,self.neo4j_Connector)
            

    def loadConstraints(self,dataset):
        if dataset == "movies":
            return movies_queries
        if dataset == "fincen":
            return fincen_queries
        if dataset == "stackoverflow":
            return stackoverflow_query
        if dataset == "wwwc2019":
            return wwwc2019_query
        if dataset == "synthea":
            return synthea_query
        if dataset == "sw":
            return sw_queries
    
    def generateUsers(self,max_users):
        users = []
        for i in range(max_users):
            users.append(User("tutti"))
        return users


# Example Usage
if __name__ == "__main__":
    argv = sys.argv[1:]
    #python3 environment3.py $dataset $safety $assignment $users $error $answer
    dataset = argv[0]
    safetiness = argv[1]=="True"
    assignment = argv[2]
    users = int(argv[3])
    error=[]
    if(dataset=="movies"):
        error=[1,5,1,29]
    if(dataset=="fincen"):
        error = [150,200,6,300,0]
    if(dataset=="stackoverflow"):
        error = [1,1,2,277]
    if(dataset=="wwwc2019"):
        error = [9,21,6,300,0]
    if(dataset=="synthea"):
        error = [1,1,1,1000,1,1]
    if(dataset=="sw"):
        error = [3,1,9,41]
    answer = float(argv[4])
    
    env = CGREnvironment(max_users=users, dataset=dataset,safetiness= safetiness, timeout=3600, assignment=assignment,error_distribution=error, SEED = 1, user_distribution=[1,1,1], answer_distribution=[answer,1-answer])
    #try:
    env.start_fixed_arrival_simulation()
    #except Exception as e:
    #   print(e)
    
