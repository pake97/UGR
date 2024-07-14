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
        firstTime = True
        to_inject=[]
        violations_ids = []
        n_violations = []
        time1 = time.time()
        for seed2 in range(1):
            self.wait_count=0
            self.iteration_count=0
            self.interaction_count=0
            conteggi=[]
            t0 = time.time()
            injectSyntheticData(self.neo4j_Connector)
            if(firstTime):
                to_inject=injectInconsistencies(self.neo4j_Connector,self.constraints,self.error_distribution,self.SEED)
            else:
                restore_graph(self.neo4j_Connector,to_inject,self.SEED,self.constraints)
            
            
            #nodes = self.neo4j_Connector.query("MATCH (n) RETURN n")
            #injectFixedInconsistencies(self.neo4j_Connector,self.error_distribution,self.SEED)
            #edges = self.neo4j_Connector.query("MATCH ()-[r]->() RETURN r")
            
            graphInconsistent = True
            # t0 = time.time()
            timedOut=False
            #print("Starting CGR")


            if(firstTime):                
                violations_ids = checkConstraints(self.constraints,self.neo4j_Connector, self.assignment)
                violations_ids = [v['id'] for v in violations_ids]
                firstTime=False
            else:
                restoreConstraints(self.neo4j_Connector,n_violations,self.assignment)
                                    
            random.seed(self.SEED)

            while graphInconsistent: 
                num_viols=self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) RETURN COUNT(v) as count")
                print(num_viols)
                if(len(conteggi)>0):
                    if(num_viols[0]['count']==conteggi[-1]):
                        conteggi.append(num_viols[0]['count'])
                    else:
                        conteggi=[]
                        conteggi.append(num_viols[0]['count'])
                else:
                    conteggi.append(num_viols[0]['count'])
                if(len(conteggi)==20):
                    timedOut=True
                    break
                if(self.iteration_count>2*len(violations_ids)):
                    timedOut=True 
                    break
                else:
                    self.iteration_count+=1
                    chosen_repairs=[]
                    chosen_violations=[]


                    for u in self.users:
                        
                        if(self.assignment=="random"):
                            assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation {locked : false}) RETURN v, rand() as r ORDER BY r LIMIT 1")
                        elif self.assignment=="betweennessDesc":
                            assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation {locked : false}) RETURN v ORDER BY v.betweenness DESC LIMIT 1")
                        elif self.assignment=="betweennessAsc":
                            assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation {locked : false}) RETURN v ORDER BY v.betweenness LIMIT 1")
                        elif self.assignment=="degreeDesc":
                            assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation {locked : false}) RETURN v ORDER BY v.degree DESC LIMIT 1")
                        elif self.assignment=="degreeAsc":
                            assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation {locked : false}) RETURN v ORDER BY v.degree LIMIT 1")
                        elif self.assignment=="prDesc":
                            assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation {locked : false}) RETURN v ORDER BY v.pageRank DESC LIMIT 1")
                        elif self.assignment=="prAsc":
                            assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation {locked : false}) RETURN v ORDER BY v.pageRank LIMIT 1")
                    
                        if(len(assigned_hypervertex)==0):
                            self.wait_count+=1
                        else:
                            assigned_hypervertex = assigned_hypervertex[0]
                            violation_id=assigned_hypervertex['v'].element_id.split(":")[-1]                        
                            #lock the violation
                            self.neo4j_Connector.merge_query("MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.locked = true")
                            #lock thr neighbors
                            self.neo4j_Connector.merge_query("MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" CALL apoc.neighbors.athop(v, 'INTERSECT', 1) YIELD node SET node.locked = true")
                            #print("assigned",assigned_hypervertex)
                            repairs = computeRepairs(assigned_hypervertex, self.constraints,self.SEED)

                            u.set_actions(repairs['possible_repairs'])
                            u.set_best_repair(repairs['best_repair'])
                            chosen_repair = u.select_action_by_policy(self.answer_distribution,seed2)
                            
                            stopped=0
                            if(self.safetiness):
                                while(True):
                                    if(checkSafety(chosen_repair,assigned_hypervertex,self.neo4j_Connector,self.constraints)):
                                        chosen_repairs.append(chosen_repair)
                                        chosen_violations.append(assigned_hypervertex)
                                        break
                                    else:       
                                        stopped+=1
                                        u.remove_action(chosen_repair)
                                        if(len(u.actions)==0):
                                            self.wait_count+=1
                                            break
                                        else:
                                            chosen_repair = u.select_action_by_policy(self.answer_distribution,seed2)
                            else:
                                chosen_repairs.append(chosen_repair)
                                chosen_violations.append(assigned_hypervertex)
                            print("Stopped: ", stopped)
                    print("Chosen repairs: ", len(chosen_repairs))
                    solved_count = 0 
                    t31 = time.time()
                    track=[]
                    for i in range(len(chosen_repairs)):
                        applyRepair(chosen_repairs[i],self.neo4j_Connector)
                        solved_count+=1
                        self.interaction_count+=1
                        properties = {}
                        for l, v in chosen_violations[i]['v'].items():
                            properties[l] = v 
                        violation_nodes =properties['nodes'].split(",")                        
                        violation_labels =properties['labels'].split(",")                
                        track.append((violation_nodes,violation_labels))
                        violation_id = chosen_violations[i]['v'].element_id.split(":")[-1] 
                        neighbors=self.neo4j_Connector.query("MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" CALL apoc.neighbors.athop(v, 'INTERSECT', 1) YIELD node RETURN ID(node) as id, node.nodes as nodes, node.labels as labels, node.type as type")
                        for ngh in neighbors:
                            ngh_id = ngh['id']
                            nodi=ngh['nodes'].split(",")
                            labels=ngh['labels'].split(",")
                            violation_type = ngh['type']
                            filters =""
                            for i in range(len(nodi)):
                                if(filters==""):
                                    filters+="ID("+labels[i]+")="+nodi[i]
                                else:
                                    filters+=" AND ID("+labels[i]+")="+nodi[i]
                            query = self.constraints[violation_type]['constraint']
                            if("WHERE" in query):
                                query = query.replace("RETURN", "AND "+filters + " RETURN")
                            else:
                                query = query.replace("RETURN", "WHERE "+filters + " RETURN")
                            if(self.neo4j_Connector.query(query)==[]):
                                solved_count+=1
                                self.neo4j_Connector.merge_query("MATCH (v:Violation) WHERE ID(v)= "+str(ngh_id)+" SET v.solved=True")
                    print("Solved count: ", solved_count)
                    t32 = time.time()
                    print("Time to delete: ", t32-t31)
                    
                    t21 = time.time()
                    added_count = 0
                    if(not self.safetiness):        
                        for constraint in self.constraints:
                            allowed_nodes = constraint['ids']
                            viols =[]
                            for i in range(len(track)):
                                nodi=track[i][0]
                                labels=track[i][1]
                                for j in range(len(nodi)):
                                    if('ID('+labels[j]+')' in allowed_nodes):
                                        filters="ID("+labels[j]+")="+nodi[j]
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
                                    
                                    new_violations = self.neo4j_Connector.query(constraint['create_new_violation'].replace("FILTRI",filters))
                                    added_count+=len(new_violations)
                                    for v in new_violations:    
                                        id_v = v['v1'].element_id.split(":")[-1]
                                        if(id_v not in violations_ids):
                                            n_violations.append(id_v)
                                            
                                    for v in new_violations:
                                        id_v = v['v1'].element_id.split(":")[-1]
                                        new_edges=self.neo4j_Connector.merge_query("MATCH (v1:Violation {solved:False})<-[:BELONGS]-(a)-[:BELONGS]-(v2:Violation {solved:False}) WHERE ID(v1)="+str(id_v)+" AND ID(v2)<>"+str(id_v)+" AND NOT (v1)-[:INTERSECT]-(v2) MERGE (v1)-[:INTERSECT]-(v2)")
                    print("Added count: ", added_count)
                    if(len(self.neo4j_Connector.query("MATCH (v:Violation {solved:false}) RETURN v"))==0):
                        graphInconsistent=False
                    else:
                        solvedViolations = self.neo4j_Connector.query("MATCH (v:Violation {solved:true}) RETURN ID(v) as id")
                        for v in solvedViolations:
                            self.neo4j_Connector.query("MATCH (v:Violation) WHERE ID(v)="+str(v['id'])+" CALL apoc.refactor.rename.label('Violation', 'SolvedViolation', [v]) YIELD committedOperations RETURN committedOperations")
                        self.neo4j_Connector.merge_query("MATCH (sv:SolvedViolation)-[r:INTERSECT]-() DELETE r")
                        self.neo4j_Connector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
                        self.neo4j_Connector.merge_query("MATCH (v:Violation {solved:false}) SET v.locked=false")
                        
                        t0 = time.time()
                        build_grdg =  self.neo4j_Connector.merge_query("CALL gds.graph.project('grdg', 'Violation', {INTERSECT: {orientation: 'UNDIRECTED'}})")
                        t1 = time.time()
                        print("Time to update grdg: ", t1-t0)
                        t2 = time.time()
                        compute_btw = self.neo4j_Connector.query("CALL gds.pageRank.write('grdg', { writeProperty: 'pageRank' , maxIterations: 20, dampingFactor: 0.85 }) YIELD centralityDistribution, nodePropertiesWritten RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten,centralityDistribution.max AS maximumScore")
                        t3 = time.time()
                        
                        print("Time to compute pr: ", t3-t2)
                                    
                    t22 = time.time()
                    print("Time diramation: ", t22-t21)

            t1 = time.time()
            if(timedOut):
                print("CGR timed out")
            else:
                print("Graph is consistent")
                solved_violations = self.neo4j_Connector.query("MATCH (v:SolvedViolation) RETURN v")
                precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
                if(seed2==0):
                    self.avg_precision=precision
                    self.avg_recall=recall
                    self.avg_f1=f1
                else:
                    self.avg_precision+=precision
                    self.avg_recall+=recall
                    self.avg_f1+f1
            print("interaction count: ", self.interaction_count)
            print("iteration count: ", self.iteration_count)
            print("wait count: ", self.wait_count)
            self.avg_interaction_count+=self.interaction_count
            self.avg_wait_count+=self.wait_count
            self.avg_iteration_count+=self.iteration_count

        time2 = time.time()
        print("AVG Time elapsed: ", (time2-time1)/10)
        print("Precision: ", self.avg_precision/10)
        print("Recall: ",self.avg_recall/10)
        print("F1: ", self.avg_f1/10) 
        
        print("Number of iterations: ", self.avg_iteration_count/10)
        print("Number of interactions: ", self.avg_interaction_count/10)
        print("Number of waitings: ", self.avg_wait_count/10)

        

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
    
