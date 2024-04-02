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
from config.fincen_query import fincen_queries
from config.stackoverflow_query import stackoverflow_query
from config.wwc2019_query import wwc2019_query
from config.sw_query import sw_queries
from utils.computeRepairs_preferred import computeRepairs
from utils.checkSafety3 import checkSafety
from utils.applyRepair import applyRepair
from utils.restore_graph import restore_graph
from utils.restoreConstraints import restoreConstraints
from utils.compute_metrics2 import compute_metrics
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
        self.neo4j_Connector.clearNeo4j()
        #print("Loading dataset")
        self.neo4j_Connector.loadDatasetToNeo4j(self.dataset)
        random.seed(self.SEED)
        firstTime = True
        to_inject=[]
        violations_ids = []
        n_violations = []
        for seed2 in range(1,11):
            
            self.wait_count=0
            self.iteration_count=0
            self.interaction_count=0
            time1 = time.time()
            injectSyntheticData(self.neo4j_Connector)
            if(firstTime):
                to_inject=injectInconsistencies(self.neo4j_Connector,self.constraints,self.error_distribution,self.SEED)
            else:
                restore_graph(self.neo4j_Connector,to_inject,self.SEED,self.constraints)
            
            graphInconsistent = True
            # t0 = time.time()
            timedOut=False
            #print("Starting CGR")


            if(firstTime):
                violations_ids = checkConstraints(self.constraints,self.neo4j_Connector)
                violations_ids = [v['v1'].element_id.split(":")[-1] for v in violations_ids]
                firstTime=False
            else:
                violations = restoreConstraints(self.neo4j_Connector,n_violations)
            
            random.seed(seed2)
            while graphInconsistent: 
                print(self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) RETURN COUNT(v) as count"))
                if(self.iteration_count>2*len(violations_ids)):
                    timedOut=True
                    break
                #quante = self.neo4j_Connector.query("MATCH (v1:Violation {solved:False}) RETURN COUNT(v1) as count")
                #print(quante[0]['count'])
                assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) RETURN v LIMIT 1")
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
                            
                    if(self.mode=="label"):
                        for c in configs["schema_preferred"]:
                            possible_repairs.append(c)

                    sorted(possible_repairs, key=lambda d: d['score']) 
                    grouped_repairs = [[x for x in possible_repairs if x['score']==i] for i in range(1,10)]
                    if(self.safetiness):
                        chosen_repair=""
                        while(True):
                            i=0
                            while True:
                                if(len(grouped_repairs[i])==0):
                                    i+=1
                                else:
                                    chosen_repair = random.choice(grouped_repairs[i])
                                    index = grouped_repairs[i].index(chosen_repair)
                                    grouped_repairs[i].pop(index)
                                    break
                            
                            chosen_repair=computeRepairs(assigned_hypervertex['v'],properties,chosen_repair['repair'])
                            
                            if(checkSafety(chosen_repair,assigned_hypervertex,self.neo4j_Connector,self.constraints)):
                                #print(chosen_repair)
                                applyRepair(chosen_repair,self.neo4j_Connector)  
                                self.interaction_count+=1      
                                break
   
                    else:
                        chosen_repair = random.choice(grouped_repairs[0])
                        chosen_repair=computeRepairs(assigned_hypervertex['v'],properties,chosen_repair['repair'])
                        applyRepair(chosen_repair,self.neo4j_Connector)  
                        self.interaction_count+=1      
                    solved_count=+1
                    
                    violation_nodes =properties['nodes'].split(",")                        
                    violation_labels =properties['labels'].split(",")                
                    
                    #find violations that contains the same node 
                    old_violation_ids = []
                    all_violations= self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) RETURN v")
                    for vio in all_violations:
                        old_violation_ids.append(vio['v'].element_id.split(":")[-1])
                        properties = {}
                        for l, v in vio['v'].items():
                            properties[l] = v 
                        query =self.constraints[properties['type']]
                        filters =""
                        violation_type = properties['type']
                        violation_nodes =properties['nodes'].split(",")                        
                        violation_labels =properties['labels'].split(",")   
                        for i in range(len(violation_nodes)):
                            if(filters==""):
                                filters+="ID("+violation_labels[i]+")="+violation_nodes[i]
                            else:
                                filters+=" AND ID("+violation_labels[i]+")="+violation_nodes[i]
                        query = self.constraints[violation_type]['constraint']
                        if("WHERE" in query):
                            query = query.replace("RETURN", "AND "+filters + " RETURN")
                        else:
                            query = query.replace("RETURN", "WHERE "+filters + " RETURN")
                        if(self.neo4j_Connector.query(query)==[]):
                            solved_count+=1
                            self.neo4j_Connector.merge_query("MATCH (v:Violation) WHERE ID(v)= "+vio['v'].element_id.split(":")[-1]+" SET v.solved=True")

                    introduced_violations = []
                    for constraint in self.constraints:
                        allowed_nodes = constraint['ids']
                        viols =[]                                                                                        
                        for j in range(len(violation_nodes)):
                            if('ID('+violation_labels[j]+')' in allowed_nodes):
                                filters="ID("+violation_labels[j]+")="+violation_nodes[j]
                                vios=self.neo4j_Connector.query(constraint['new_constraint'].replace("FILTRI",filters))   
                                viols.extend(vios)                            
                    for viol in viols:
                        filters =""                                    
                        for nodes in viol.keys():
                            if(filters==""):
                                filters+=nodes + "="+str(viol[nodes])
                            else:
                                filters+=" AND "+nodes + "="+str(viol[nodes])
                        # query = self.constraints[violation_type]['constraint']
                        # if(self.neo4j_Connector.query(query.replace("RETURN", filters + " RETURN"))==[]):
                        if(len(self.neo4j_Connector.query(constraint['check_new_violation'].replace("FILTRI",filters)))==0):
                            #print(constraint['create_new_violation'].replace("FILTRI",filters))
                            new_violations = self.neo4j_Connector.query(constraint['create_new_violation'].replace("FILTRI",filters))
                            #print("new",len(new_violations))
                            for v in new_violations:
                                added_count+=1
                                id_v = v['v1'].element_id.split(":")[-1]
                                if(id_v not in violations_ids):
                                    n_violations.append(id_v)
                    print("Introduced count: ", added_count)
                    print("Solved count: ", solved_count)
            if(timedOut):
                print("Preferred timed out")
            else:
                print("Graph is consistent")
                solved_violations = self.neo4j_Connector.query("MATCH (v:Violation) RETURN v")
                precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
                if(seed2==0):
                    self.avg_precision=precision
                    self.avg_recall=recall
                    self.avg_f1=f1
                else:
                    self.avg_precision=(self.avg_precision*(seed2)+precision)/(seed2+1)
                    self.avg_recall=(self.avg_recall*(seed2)+recall)/(seed2+1)
                    self.avg_f1=(self.avg_f1*(seed2)+f1)/(seed2+1)
            print("interaction count: ", self.interaction_count)
            print("iteration count: ", self.iteration_count)
            print("wait count: ", self.wait_count)
            self.avg_interaction_count=(self.avg_interaction_count*(seed2)+self.interaction_count)/(seed2+1)
            self.avg_wait_count=(self.avg_wait_count*(seed2)+self.wait_count)/(seed2+1)
            self.avg_iteration_count=(self.avg_iteration_count*(seed2)+self.iteration_count)/(seed2+1)
        time2 = time.time()
        print("AVG Time elapsed: ", (time2-time1)/10)
        print("Precision: ", self.avg_precision)
        print("Recall: ",self.avg_recall)
        print("F1: ", self.avg_f1)
        
        print("Number of iterations: ", self.avg_iteration_count)
        print("Number of interactions: ", self.avg_interaction_count)
        print("Number of waitings: ", self.avg_wait_count)
        self.neo4j_Connector.merge_query("CALL apoc.export.csv.all('"+self.dataset+"-"+str(self.safetiness)+"-"+self.mode+"-Pref.csv', {})")
        

    def loadConstraints(self,dataset):
        if dataset == "movies":
            return movies_queries
        if dataset == "fincen":
            return fincen_queries
        if dataset == "stackoverflow":
            return stackoverflow_query
        if dataset == "wwc2019":
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
    mode = argv[2]
    error=[]
    if(dataset=="movies"):
        error=[1,5,1,29]
    if(dataset=="fincen"):
        error = [150,200,6,300,0]
    if(dataset=="stackoverflow"):
        error = [1,1,2,277]
    if(dataset=="wwc2019"):
        error = [9,21,6,300,0]
    if(dataset=="synthea"):
        error = [1,1,1,1000,1,1]
    if(dataset=="sw"):
        error = [3,1,9,41]
    
    
    env = CGREnvironment(dataset=dataset,safetiness= safetiness, error_distribution=error, SEED = 1, mode=mode)
    #try:
    env.start_fixed_arrival_simulation()
    #except Exception as e:
    #print(e)
    
