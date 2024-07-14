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
from utils.neo4j_connector import Neo4jConnector
from utils.checkConstraints_preferred import checkConstraints
from config.movies_query import movies_queries
from config.grr_fincen_query import fincen_queries
from config.grr_stackoverflow_query import stackoverflow_query
from config.grr_wwwc2019_query import wwwc2019_query
from config.grr_sw_query import sw_queries
from config.grr_synthea_query import synthea_query
from config.rules_sw import rules as sw_rules
from config.rules_fincen import rules as fincen_rules
from config.rules_stack import rules as stack_rules
from config.rules_wwc19 import rules as wwwc19_rules
from config.rules_synthea import rules as synthea_rules

from utils.computeRepairs_preferred import computeRepairs
from utils.checkSafety3 import checkSafety
from utils.applyRepair import applyRepair
from utils.restore_graph import restore_graph
from utils.restoreConstraints import restoreConstraints
from utils.compute_metrics2 import compute_metrics
from agent.user import User
import sys
class CGREnvironment:
    def __init__(self,dataset="movies",safetiness=False,error_distribution=[0.5,0.5,0.5,0.5], SEED = 1):
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
        self.safetiness=safetiness


    def start_fixed_arrival_simulation(self):
        #print("Clearing dataset")
        self.neo4j_Connector.clearNeo4j()
        #print("Loading dataset")
        self.neo4j_Connector.loadDatasetToNeo4j(self.dataset)
        random.seed(self.SEED)
        
        
            
        self.wait_count=0
        self.iteration_count=0
        self.interaction_count=0
        time1 = time.time()
        injectSyntheticData(self.neo4j_Connector)
        
        to_inject=injectInconsistencies(self.neo4j_Connector,self.constraints[0],self.error_distribution,self.SEED)
        
        
        graphInconsistent = True
        # t0 = time.time()
        timedOut=False
        #print("Starting CGR")


        
        violations_ids = checkConstraints(self.constraints[0],self.neo4j_Connector)
        violations_ids = [v['v1'].element_id.split(":")[-1] for v in violations_ids] 
        while graphInconsistent: 
            print(self.neo4j_Connector.query("MATCH (v) RETURN COUNT(v) as count"))
            self.iteration_count=+1
            print(self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) RETURN COUNT(v) as count"))
            if(self.iteration_count>10):
                timedOut=True
                graphInconsistent=False
                break
            else:
                for rule in self.constraints[1]['queries']:
                    self.neo4j_Connector.query(rule)
                self.neo4j_Connector.query("MATCH (v:Violation) DETACH DELETE v")
                for idx,constraint in enumerate(self.constraints[0]):
        
                    query = constraint['create_constraint']
                    try:
                        results = self.neo4j_Connector.merge_query(query)
                    except Exception as e:
                        print("Error executing query: ", query)
                        print(e)
                        continue
                if(len(self.neo4j_Connector.query("MATCH (v:Violation {solved:false}) RETURN v"))==0):
                    graphInconsistent=False
                    break
        if(timedOut):
            print("Preferred timed out")
        else:
            print("Graph is consistent")
            touched_nodes = self.neo4j_Connector.query("MATCH (n) where n.injected=True or n.updated=True return n")
            added_edges = self.neo4j_Connector.query("MATCH (n)-[r]-(m) where r.added=True return r")
            touched_edges = self.neo4j_Connector.query("MATCH (n)-[r:SYNTH]-(m) return r")
            true_positives_nodes = 0
            false_positives_nodes = 0
            false_negatives_nodes = 0
            
            true_positives_edges = 0
            false_positives_edges = 0
            false_negatives_edges = len(added_edges)
            
            for node in touched_nodes:
                properties = {}
                for l, v in node['n'].items():
                    properties[l] = v 
                if(properties['synth1']==0 and not properties['updated']):
                    false_negatives_nodes+=1   
                if(properties['synth1']==0 and properties['updated']):
                    false_positives_nodes+=1
                if(properties['synth1']==1 and properties['updated']):
                    true_positives_nodes+=1
                    
            for edge in touched_edges:
                
                properties = {}
                for l, v in edge['r'].items():
                    properties[l] = v 
                label = edge['r'].type
                if(label=='SYNTH'):            
                    if(properties['deleted']==True):
                        true_positives_edges+=1
                    else:
                        false_negatives_edges+=1
                else:
                    if(properties['deleted']==False):
                        true_negatives_edges+=1
                    else:
                        false_positives_edges+=1

            
            
            true_positives = true_positives_nodes + true_positives_edges
            false_positives = false_positives_nodes + false_positives_edges
            false_negatives = false_negatives_nodes + false_negatives_edges

            """ print("True positives: ", true_positives)
            print("False positives: ", false_positives)
            print("False negatives: ", false_negatives) """
            precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            print("Precision: ", precision)
            print("Recall: ", recall)
            print("F1 Score: ", f1_score)
            print("interaction count: ", self.interaction_count)
            print("iteration count: ", self.iteration_count)
            print("wait count: ", self.wait_count)
        
        

    def loadConstraints(self,dataset):
        if dataset == "fincen":
            return fincen_queries, fincen_rules
        if dataset == "stackoverflow":
            return stackoverflow_query, stack_rules
        if dataset == "wwwc2019":
            return wwwc2019_query, wwwc19_rules
        if dataset == "synthea":
            return synthea_query, synthea_rules
        if dataset == "sw":
            return sw_queries, sw_rules

    
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
    
    
    env = CGREnvironment(dataset=dataset,safetiness= safetiness, error_distribution=error, SEED = 1)
    #try:
    env.start_fixed_arrival_simulation()
    #except Exception as e:
    #print(e)
    
