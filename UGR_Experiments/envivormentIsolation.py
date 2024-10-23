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
from utils.checkConstraints5 import checkConstraints
from config.movies_query import movies_queries
from config.fincen_query import fincen_queries
from config.stackoverflow_query import stackoverflow_query
from config.wwwc2019_query import wwwc2019_query
from utils.computeRepairs4 import computeRepairs
from utils.checkSafety3 import checkSafety
from utils.applyRepair import applyRepair
from utils.restore_graph import restore_graph
from config.sw_query import sw_queries
from utils.restoreConstraints3 import restoreConstraints
from utils.compute_metrics2 import compute_metrics
from agent.user2 import User
from config.synthea_query import synthea_query
from utils.computeRepairs_preferred import computeRepairs as computeRepairs_preferred
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
        
        firstTime = True
        to_inject=[]
        violations_ids = []
        violations = []
        
        injectSyntheticData(self.neo4j_Connector)
        to_inject=injectInconsistencies(self.neo4j_Connector,self.constraints,self.error_distribution,self.SEED)
        time1 = time.time()
        for idx,constraint in enumerate(self.constraints):
                    
            query = constraint['create_constraint']
            try:
                results = self.neo4j_Connector.merge_query(query)
            except Exception as e:
                print("Check constraints error: ", query)
                print(e)
                continue
        t0 = time.time()
        print("Time to detect violations: ", t0-time1)
        try:        
            results = self.neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.id)")
            results = self.neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.solved)")
            violations = self.neo4j_Connector.query("MATCH (v:Violation) return ID(v) as id")
        except Exception as e:
            print("interect violation error: ", query)
            print(e)

        violations_ids = [v['id'] for v in violations]
        firstTime=False
        
        
        
        for seed2 in range(10):        
            random.seed(self.SEED)
            u = User("tutti")
                
            for vid in violations_ids:
                assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation) where id(v)="+str(vid)+" RETURN v")
        
                assigned_hypervertex = assigned_hypervertex[0]                        

                repairs = computeRepairs(assigned_hypervertex, self.constraints,self.SEED)

                u.set_actions(repairs['possible_repairs'])
                u.set_best_repair(repairs['best_repair'])
                chosen_repair = u.select_action_by_policy([0,1],seed2)
                applyRepair(chosen_repair,self.neo4j_Connector) 
            
            solved_violations = self.neo4j_Connector.query("MATCH (v:Violation {solved:true}) RETURN v")
            precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
            print("Precision UGR 0: ", precision)
            print("Recall UGR 0: ",recall)
            print("F1 UGR 0: ", f1) 
            
            for const in self.constraints:
                vios=self.neo4j_Connector.query(const['constraint'])
                print("Introduced violations UGR 0: ", len(vios))
                
            self.neo4j_Connector.merge_query("MATCH (v:Violation {solved:true}) SET v.solved=false")
            restore_graph(self.neo4j_Connector,to_inject,self.SEED,self.constraints)
            
            
            for vid in violations_ids:
                assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation) where id(v)="+str(vid)+" RETURN v")
        
                assigned_hypervertex = assigned_hypervertex[0]                        

                repairs = computeRepairs(assigned_hypervertex, self.constraints,self.SEED)

                u.set_actions(repairs['possible_repairs'])
                u.set_best_repair(repairs['best_repair'])
                chosen_repair = u.select_action_by_policy([0.25,0.75],seed2)
                applyRepair(chosen_repair,self.neo4j_Connector) 
            
            solved_violations = self.neo4j_Connector.query("MATCH (v:Violation {solved:true}) RETURN v")
            precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
            print("Precision UGR 25: ", precision)
            print("Recall UGR 25: ",recall)
            print("F1 UGR 25: ", f1) 
            
            for const in self.constraints:
                vios=self.neo4j_Connector.query(const['constraint'])
                print("Introduced violations UGR 25: ", len(vios))
                
            self.neo4j_Connector.merge_query("MATCH (v:Violation {solved:true}) SET v.solved=false")
            restore_graph(self.neo4j_Connector,to_inject,self.SEED,self.constraints)
            
            
            for vid in violations_ids:
                assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation) where id(v)="+str(vid)+" RETURN v")
        
                assigned_hypervertex = assigned_hypervertex[0]                        

                repairs = computeRepairs(assigned_hypervertex, self.constraints,self.SEED)

                u.set_actions(repairs['possible_repairs'])
                u.set_best_repair(repairs['best_repair'])
                chosen_repair = u.select_action_by_policy([0.5,0.5],seed2)
                applyRepair(chosen_repair,self.neo4j_Connector) 
            
            solved_violations = self.neo4j_Connector.query("MATCH (v:Violation {solved:true}) RETURN v")
            precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
            print("Precision UGR 50: ", precision)
            print("Recall UGR 50: ",recall)
            print("F1 UGR 50: ", f1) 
            
            for const in self.constraints:
                vios=self.neo4j_Connector.query(const['constraint'])
                print("Introduced violations UGR 50: ", len(vios))
                
            self.neo4j_Connector.merge_query("MATCH (v:Violation {solved:true}) SET v.solved=false")
            restore_graph(self.neo4j_Connector,to_inject,self.SEED,self.constraints)
            
            
            for vid in violations_ids:
                assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation) where id(v)="+str(vid)+" RETURN v")
        
                assigned_hypervertex = assigned_hypervertex[0]                        

                repairs = computeRepairs(assigned_hypervertex, self.constraints,self.SEED)

                u.set_actions(repairs['possible_repairs'])
                u.set_best_repair(repairs['best_repair'])
                chosen_repair = u.select_action_by_policy([0.75,0.25],seed2)
                applyRepair(chosen_repair,self.neo4j_Connector) 
            
            solved_violations = self.neo4j_Connector.query("MATCH (v:Violation {solved:true}) RETURN v")
            precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
            print("Precision UGR 75: ", precision)
            print("Recall UGR 75: ",recall)
            print("F1 UGR 75: ", f1) 
            
            for const in self.constraints:
                vios=self.neo4j_Connector.query(const['constraint'])
                print("Introduced violations UGR 75: ", len(vios))
                
            self.neo4j_Connector.merge_query("MATCH (v:Violation {solved:true}) SET v.solved=false")
            restore_graph(self.neo4j_Connector,to_inject,self.SEED,self.constraints)
            
            
            for vid in violations_ids:
                assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation) where id(v)="+str(vid)+" RETURN v")
        
                assigned_hypervertex = assigned_hypervertex[0]                        

                repairs = computeRepairs(assigned_hypervertex, self.constraints,self.SEED)

                u.set_actions(repairs['possible_repairs'])
                u.set_best_repair(repairs['best_repair'])
                chosen_repair = u.select_action_by_policy([1,0],seed2)
                applyRepair(chosen_repair,self.neo4j_Connector) 
            
            solved_violations = self.neo4j_Connector.query("MATCH (v:Violation {solved:true}) RETURN v")
            precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
            print("Precision UGR 1: ", precision)
            print("Recall UGR 1: ",recall)
            print("F1 UGR 1: ", f1) 
            
            for const in self.constraints:
                vios=self.neo4j_Connector.query(const['constraint'])
                print("Introduced violations UGR 1: ", len(vios))
                
            self.neo4j_Connector.merge_query("MATCH (v:Violation {solved:true}) SET v.solved=false")
            restore_graph(self.neo4j_Connector,to_inject,self.SEED,self.constraints)
            
            for vid in violations_ids:
                assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation) where id(v)="+str(vid)+" RETURN v")
        
                assigned_hypervertex = assigned_hypervertex[0]
                properties = {}
                for l, v in assigned_hypervertex['v'].items():
                    properties[l] = v 
                configs = self.constraints[properties['type']]
                possible_repairs=[]
                
                for c in configs["delete_preferred"]:
                    possible_repairs.append(c)
                
                    

                sorted(possible_repairs, key=lambda d: d['score']) 
                grouped_repairs = [[x for x in possible_repairs if x['score']==i] for i in range(1,10)]
                    
                chosen_repair = random.choice(grouped_repairs[0])
                chosen_repair=computeRepairs_preferred(assigned_hypervertex['v'],properties,chosen_repair['repair'])
                applyRepair(chosen_repair,self.neo4j_Connector)  
                
            solved_violations = self.neo4j_Connector.query("MATCH (v:Violation {solved:true}) RETURN v")
            precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
            print("Precision D: ", precision)
            print("Recall D: ",recall)
            print("F1 D: ", f1) 
            
            for const in self.constraints:
                vios=self.neo4j_Connector.query(const['constraint'])
                print("Introduced violations D: ", len(vios))
                
            self.neo4j_Connector.merge_query("MATCH (v:Violation {solved:true}) SET v.solved=false")
            restore_graph(self.neo4j_Connector,to_inject,self.SEED,self.constraints)
            
            
            for vid in violations_ids:
                assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation) where id(v)="+str(vid)+" RETURN v")
        
                assigned_hypervertex = assigned_hypervertex[0]
                properties = {}
                for l, v in assigned_hypervertex['v'].items():
                    properties[l] = v 
                configs = self.constraints[properties['type']]
                possible_repairs=[]
                
                for c in configs["update_preferred"]:
                    possible_repairs.append(c)
                
                    

                sorted(possible_repairs, key=lambda d: d['score']) 
                grouped_repairs = [[x for x in possible_repairs if x['score']==i] for i in range(1,10)]
                    
                chosen_repair = random.choice(grouped_repairs[0])
                chosen_repair=computeRepairs_preferred(assigned_hypervertex['v'],properties,chosen_repair['repair'])
                applyRepair(chosen_repair,self.neo4j_Connector)  
                
            solved_violations = self.neo4j_Connector.query("MATCH (v:Violation {solved:true}) RETURN v")
            precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
            print("Precision U: ", precision)
            print("Recall U: ",recall)
            print("F1 U: ", f1) 
            
            for const in self.constraints:
                vios=self.neo4j_Connector.query(const['constraint'])
                print("Introduced violations U: ", len(vios))
                
            self.neo4j_Connector.merge_query("MATCH (v:Violation {solved:true}) SET v.solved=false")
            restore_graph(self.neo4j_Connector,to_inject,self.SEED,self.constraints)
            
            
            
            for vid in violations_ids:
                assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation) where id(v)="+str(vid)+" RETURN v")
        
                assigned_hypervertex = assigned_hypervertex[0]
                properties = {}
                for l, v in assigned_hypervertex['v'].items():
                    properties[l] = v 
                configs = self.constraints[properties['type']]
                possible_repairs=[]
                
                for c in configs["num_op_preferred"]:
                    possible_repairs.append(c)
                
                    

                sorted(possible_repairs, key=lambda d: d['score']) 
                grouped_repairs = [[x for x in possible_repairs if x['score']==i] for i in range(1,10)]
                    
                chosen_repair = random.choice(grouped_repairs[0])
                chosen_repair=computeRepairs_preferred(assigned_hypervertex['v'],properties,chosen_repair['repair'])
                applyRepair(chosen_repair,self.neo4j_Connector)  
                
            solved_violations = self.neo4j_Connector.query("MATCH (v:Violation {solved:true}) RETURN v")
            precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
            print("Precision N: ", precision)
            print("Recall N: ",recall)
            print("F1 N: ", f1) 
            
            for const in self.constraints:
                vios=self.neo4j_Connector.query(const['constraint'])
                print("Introduced violations N: ", len(vios))
                
            self.neo4j_Connector.merge_query("MATCH (v:Violation {solved:true}) SET v.solved=false")
            restore_graph(self.neo4j_Connector,to_inject,self.SEED,self.constraints)
            
            
            for vid in violations_ids:
                assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation) where id(v)="+str(vid)+" RETURN v")
        
                assigned_hypervertex = assigned_hypervertex[0]
                properties = {}
                for l, v in assigned_hypervertex['v'].items():
                    properties[l] = v 
                configs = self.constraints[properties['type']]
                possible_repairs=[]
                
                for c in configs["schema_preferred"]:
                    possible_repairs.append(c)
                
                    

                sorted(possible_repairs, key=lambda d: d['score']) 
                grouped_repairs = [[x for x in possible_repairs if x['score']==i] for i in range(1,10)]
                    
                chosen_repair = random.choice(grouped_repairs[0])
                chosen_repair=computeRepairs_preferred(assigned_hypervertex['v'],properties,chosen_repair['repair'])
                applyRepair(chosen_repair,self.neo4j_Connector)  
                
            solved_violations = self.neo4j_Connector.query("MATCH (v:Violation {solved:true}) RETURN v")
            precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
            print("Precision S: ", precision)
            print("Recall S: ",recall)
            print("F1 S: ", f1) 
            
            for const in self.constraints:
                vios=self.neo4j_Connector.query(const['constraint'])
                print("Introduced violations S: ", len(vios))
                
            self.neo4j_Connector.merge_query("MATCH (v:Violation {solved:true}) SET v.solved=false")
            restore_graph(self.neo4j_Connector,to_inject,self.SEED,self.constraints)

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
        if dataset == "synthea50":
            return synthea_query
        if dataset == "synthea25":
            return synthea_query
        if dataset == "synthea75":
            return synthea_query
        if dataset == "synthea100":
            return synthea_query
        if dataset == "synthea125":
            return synthea_query
        if dataset == "synthea150":
            return synthea_query
        if dataset == "synthea200":
            return synthea_query
        if dataset == "synthea500":
            return synthea_query
        if dataset == "synthea1000":
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
    if dataset == "synthea50":
        error = [1,1,2,1500,2,2] 
    if dataset == "synthea25":
        error = [2000,1,1,2500,2,2] 
    if dataset == "synthea75":
        error = [1,1,2,1500,2,2] 
    if dataset == "synthea100":
        error = [1,1,4,3000,4,4] 
    if dataset == "synthea150":
        error = [1,1,4,3000,4,4]
    if dataset == "synthea125":
        error = [1,1,4,3000,4,4] 
    if dataset == "synthea200":
        error = [2,2,8,6000,8,8]
    if dataset == "synthea500":
        error = [4,4,20,10000,20,20] 
    if(dataset=="sw"):
        error = [3,1,9,41]
    answer = float(argv[4])
    
    env = CGREnvironment(max_users=users, dataset=dataset,safetiness= safetiness, timeout=3600, assignment=assignment,error_distribution=error, SEED = 1, user_distribution=[1,1,1], answer_distribution=[answer,1-answer])
    #try:
    env.start_fixed_arrival_simulation()
    #except Exception as e:
    #   print(e)
    
