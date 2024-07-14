import threading
import random
import time
import math
import numpy as np
from config.synthea_query import synthea_query
from cgr.grdg3 import GRDG
from utils.injectInconsistencies2 import injectInconsistencies
from utils.injectFixedInconsistencies import injectFixedInconsistencies
from utils.injectSyntheticData import injectSyntheticData
from config.config import DATABASE_URL
from utils.neo4j_connector_auradb import Neo4jConnector
from utils.checkConstraints_preferred import checkConstraints
from config.movies_query import movies_queries
from config.fincen_query import fincen_queries
from config.stackoverflow_query import stackoverflow_query
from config.wwwc2019_query import wwwc2019_query
from config.sw_demo_query import sw_demo_query
from utils.computeRepairs_preferred_auradb import computeRepairs
from utils.checkSafety3 import checkSafety
from utils.applyRepair import applyRepair
from utils.restore_graph import restore_graph
from utils.restoreConstraints import restoreConstraints
from utils.compute_metrics2_auradb import compute_metrics
from agent.user import User
import sys
class CGREnvironment:
    def __init__(self,dataset="movies",safetiness=False,error_distribution=[0.5,0.5,0.5,0.5], SEED = 1, mode="delete"):
        self.counter = 0
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
        self.neo4j_Connector = Neo4jConnector(DATABASE_URL)
        self.error_distribution = error_distribution
        self.SEED = SEED
        self.mode=mode
        self.safetiness=safetiness


    def start_fixed_arrival_simulation(self):
        #print("Clearing dataset")
        
        #print("Loading dataset")
        #self.neo4j_Connector.loadDatasetToNeo4j(self.dataset)
        random.seed(self.SEED)
        firstTime = True
        to_inject=[]
        violations_ids = []
        n_violations = []
        
            
        self.wait_count=0
        self.iteration_count=0
        self.interaction_count=0
        time1 = time.time()
        
        graphInconsistent = True
        # t0 = time.time()
        timedOut=False
        #print("Starting CGR")


        
        
        
        
        while graphInconsistent: 
            print(self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) RETURN COUNT(v) as count"))
            #quante = self.neo4j_Connector.query("MATCH (v1:Violation {solved:False}) RETURN COUNT(v1) as count")
            #print(quante[0]['count'])
            assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation {solved : false}) RETURN v LIMIT 1")
            print(assigned_hypervertex)
            self.iteration_count+=1        
            solved_count = 0 
            added_count = 0
            t31 = time.time()
            track=[]        
            if(len(assigned_hypervertex)==0):
                graphInconsistent=False
            else:
                assigned_hypervertex = assigned_hypervertex[0]
                properties = {}
                for l, v in assigned_hypervertex['v'].items():
                    properties[l] = v 
                configs = self.constraints[properties['type']]
                possible_repairs=[]
                if(self.mode=="delete"):
                    for c in configs["delete_preferred"]:
                        possible_repairs.append(c)
                if(self.mode=="update"):
                    for c in configs["update_preferred"]:
                        possible_repairs.append(c)
                    
                if(self.mode=="number"):
                    for c in configs["num_op_preferred"]:
                        possible_repairs.append(c)
                        
                if(self.mode=="schema"):
                    for c in configs["schema_preferred"]:
                        possible_repairs.append(c)

                sorted(possible_repairs, key=lambda d: d['score']) 
                grouped_repairs = [[x for x in possible_repairs if x['score']==i] for i in range(1,10)]
                
                chosen_repair = random.choice(grouped_repairs[0])
                chosen_repair=computeRepairs(assigned_hypervertex['v'],properties,chosen_repair['repair'])
                applyRepair(chosen_repair,self.neo4j_Connector)  
                
                self.interaction_count+=1      
                
                self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) detach delete v")
                self.neo4j_Connector.query("MATCH (a:Character)-[p:PILOT {deleted:false}]->(b:Starship)-[r:APPEARED_IN {deleted:false}] ->(c:Film) WHERE not (a)-[:APPEARED_IN {deleted:false}]->(c) MERGE (a)-[:BELONGS]->(v1:Violation {solved:false, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:0})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c);")
                self.neo4j_Connector.query("MATCH (a:Character)-[p:PILOT {deleted:false}]->(b:Vehicle)-[r:APPEARED_IN {deleted:false}] ->(c:Film) WHERE not (a)-[:APPEARED_IN {deleted:false}]->(c) MERGE (a)-[:BELONGS]->(v1:Violation {solved:false, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:1})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c);")
                self.neo4j_Connector.query("MATCH (a:Species)<-[p:OF {deleted:false}]-(b:Character)-[r:PILOT {deleted:false}]->(c:Starship) WHERE a.average_height>c.height MERGE (a)-[:BELONGS]->(v1:Violation {solved:false, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:2})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c);")
                self.neo4j_Connector.query("MATCH (v1:Violation)<-[:BELONGS]-(a)-[:BELONGS]->(v2:Violation) WHERE id(v1)<>id(v2) and not (v1)-[:INTERSECT]-(v2) merge (v1)-[:INTERSECT]-(v2)")


        if(timedOut):
            print("Preferred timed out")
        else:
            print("Graph is consistent")
            solved_violations = self.neo4j_Connector.query("MATCH (v:Violation) RETURN v")
            precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
            
            self.avg_precision=precision
            self.avg_recall=recall
            self.avg_f1=f1
        time2 = time.time()
        print("AVG Time elapsed: ", (time2-time1)/10)
        print("Precision: ", self.avg_precision)
        print("Recall: ",self.avg_recall)
        print("F1: ", self.avg_f1)
        
        print("Number of iterations: ", self.avg_iteration_count)
        print("Number of interactions: ", self.avg_interaction_count)
        print("Number of waitings: ", self.avg_wait_count)
        

    def loadConstraints(self,dataset):
        if dataset == "sw_demo":
            return sw_demo_query

    
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
    mode = argv[2]
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
    if(dataset=="sw_demo"):
        error = [3,1,9,41]
    
    
    env = CGREnvironment(dataset=dataset,safetiness= safetiness, error_distribution=error, SEED = 1, mode=mode)
    #try:
    env.start_fixed_arrival_simulation()
    #except Exception as e:
    #print(e)
    
