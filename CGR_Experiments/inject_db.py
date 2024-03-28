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
from utils.checkConstraints4 import checkConstraints
from config.movies_query import movies_queries
from config.sw_query import sw_queries
from config.sw_demo_query import sw_demo_query
from config.fincen_query import fincen_queries
from config.synthea_query import synthea_query
from config.stackoverflow_query import stackoverflow_query
from config.wwwc2019_query import wwwc2019_query
from utils.computeRepairs3 import computeRepairs
from utils.checkSafety2 import checkSafety
from utils.applyRepair import applyRepair
from utils.restore_graph import restore_graph
from utils.restoreConstraints import restoreConstraints
from utils.compute_metrics2 import compute_metrics
from agent.user import User
import sys
class CGREnvironment:
    def __init__(self, dataset="movies"):
        self.counter = 0
        self.running = False
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
        self.violation_dict={}
        self.error_distribution = [3,1,9,41]
        self.SEED=1
        

    def start_fixed_arrival_simulation(self):
        #print("Clearing dataset")
        self.neo4j_Connector.clearNeo4j()
        # #print("Loading dataset")
        self.neo4j_Connector.loadDatasetToNeo4j(self.dataset)
        #if(self.neo4j_Connector.query("RETURN gds.graph.exists('grdg')")[0]["gds.graph.exists('grdg')"]):
        #    self.neo4j_Connector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
        # node_ids={}
        # i = 0
        # res=[]
        # mat = np.zeros((7399,7399), dtype=int)
        # # while True:
        # #     rels = self.neo4j_Connector.query("MATCH ()-[r]->() return distinct r SKIP "+str(i*100)+" LIMIT 100")
        # #     res.extend(rels)
        # #     print(i)
        # #     i+=1
        # #     if(len(res)<100):
        # #         break
        # res = self.neo4j_Connector.query("MATCH ()-[r]->() return distinct r")
        # counter = 0
        # for r in res:
        #     id1 = r['r'].nodes[0].element_id.split(":")[-1]
        #     id2 = r['r'].nodes[1].element_id.split(":")[-1]
        #     if(id1 not in node_ids):
        #         node_ids[id1]=counter
        #         counter+=1
        #     if(id2 not in node_ids):
        #         node_ids[id2]=counter
        #         counter+=1
        #     mat[node_ids[id1]][node_ids[id2]]=1
        # stelle=0
        # for i in range(7399):
        #     riga =mat[i]
        #     unique, counts = np.unique(riga, return_counts=True)
        #     counts = dict(zip(unique, counts))
        #     try:
        #         uni = counts[1]
        #     except:
        #         uni=0
        #     if(uni>2):
        #         comb = math.factorial(uni)/(math.factorial(uni-3))
        #         stelle+=comb

        # print(stelle)
        #injectSyntheticData(self.neo4j_Connector)
        
        #to_inject=injectInconsistencies(self.neo4j_Connector,self.constraints,self.error_distribution,self.SEED)
        #violations = checkConstraints(self.constraints,self.neo4j_Connector)
        # firstTime = True
        # to_inject=[]
        # violations_ids = []
        # n_violations = []
        # for seed2 in range(1,10):
        #     t0 = time.time()
        #     injectSyntheticData(self.neo4j_Connector)
        #     if(firstTime):
        #         to_inject=injectInconsistencies(self.neo4j_Connector,self.constraints,self.error_distribution,self.SEED)
        #     else:
        #         restore_graph(self.neo4j_Connector,to_inject,self.SEED,self.constraints)
        #     #print("Injecting inconsistencies")
        #     #nodes = self.neo4j_Connector.query("MATCH (n) RETURN n")
        #     #injectFixedInconsistencies(self.neo4j_Connector,self.error_distribution,self.SEED)
        #     #edges = self.neo4j_Connector.query("MATCH ()-[r]->() RETURN r")
            
        #     graphInconsistent = True
        #     # t0 = time.time()
        #     timedOut=False
        #     #print("Starting CGR")


        #     if(firstTime):
        #         violations = checkConstraints(self.constraints,self.neo4j_Connector)
        #         self.grdg.build(violations)
        #         for node in self.grdg.graph.vs:
        #             violations_ids.append(node['name'])
        #         firstTime=False
        #     else:
        #         violations = restoreConstraints(self.neo4j_Connector,n_violations)
        #         self.grdg.restore()                
        #     #print(self.grdg.graph.get_adjacency())
        #     #print(self.grdg.plot())
        #     #print(len(violations))
        #     #print(self.grdg.graph.vcount())
            
        #     random.seed(self.SEED)
        #     while graphInconsistent: 
        #         #print(self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) RETURN COUNT(v) as count"))
        #         print(self.grdg.graph.vcount())
        #         if(time.time()-t0>self.timeout):

        #             timedOut=True
        #             break
                
        #         if(self.grdg.graph.vcount()==0):
        #             graphInconsistent=False
        #         else:
        #             self.iteration_count+=1
        #             chosen_repairs=[]
        #             chosen_violations=[]
        #             for u in self.users:
                        

        #                 if(self.assignment=="random"):
        #                     assigned_hypervertex = self.grdg.getViolationToRepairRandom()
        #                 else:
        #                     assigned_hypervertex = self.grdg.getViolationToRepairBetweenness()
                
        #                 #print("assigned",assigned_hypervertex)

        #                 if assigned_hypervertex is not None:
                            
        #                     repairs = computeRepairs(assigned_hypervertex, self.constraints,self.SEED)


        #                     u.set_actions(repairs['possible_repairs'])
        #                     u.set_best_repair(repairs['best_repair'])
        #                     chosen_repair = u.select_action_by_policy(self.answer_distribution,seed2)
        #                     #print(chosen_repair)
                            

        #                     if(self.safetiness):
        #                         while(True):
        #                             if(checkSafety(chosen_repair,self.neo4j_Connector,self.constraints)):
        #                                 chosen_repairs.append(chosen_repair)
        #                                 chosen_violations.append(assigned_hypervertex['name'])
        #                                 break
        #                             else:       
        #                                 u.remove_action(chosen_repair)
        #                                 if(len(u.actions)==0):
        #                                     self.wait_count+=1
        #                                     break
        #                                 else:
        #                                     chosen_repair = u.select_action_by_policy(self.answer_distribution,seed2)

        #                     else:
        #                         chosen_repairs.append(chosen_repair)
        #                         chosen_violations.append(assigned_hypervertex['name'])
        #                 else:
        #                     self.wait_count+=1

        #             to_delete=[]
        #             for i in range(len(chosen_repairs)):
        #                 applyRepair(chosen_repairs[i],self.neo4j_Connector)
        #                 self.interaction_count+=1
        #                 violation_node = self.grdg.graph.vs.find(name=chosen_violations[i])
        #                 for nodo in self.grdg.graph.neighbors(violation_node):
        #                     nod = self.grdg.graph.vs.select(nodo)[0]
        #                     nodi=nod['properties']['nodes'].split(",")
        #                     labels=nod['properties']['labels'].split(",")
        #                     violation_type = nod['properties']['type']
        #                     filters =""
        #                     for i in range(len(nodi)):
        #                         if(filters==""):
        #                             filters+="ID("+labels[i]+")="+nodi[i]
        #                         else:
        #                             filters+=" AND ID("+labels[i]+")="+nodi[i]
        #                     query = self.constraints[violation_type]['constraint']
        #                     if("WHERE" in query):
        #                         query = query.replace("RETURN", "AND "+filters + " RETURN")
        #                     else:
        #                         query = query.replace("RETURN", "WHERE "+filters + " RETURN")
        #                     if(self.neo4j_Connector.query(query)==[]):
        #                         to_delete.append(nod)
        #                         self.neo4j_Connector.merge_query("MATCH (v:Violation) WHERE ID(v)= "+str(nod['name'])+" SET v.solved=True")
        #                 to_delete.append(violation_node)
        #             self.grdg.graph.delete_vertices(to_delete)  
                            

        #             introduced_violations = []
        #             for constraint in self.constraints:
        #                 viols=self.neo4j_Connector.query(constraint['constraint'])   
                        
        #                 for viol in viols:
        #                     filters =""                                    
        #                     for nodes in viol.keys():
        #                         if(filters==""):
        #                             filters+=nodes + "="+str(viol[nodes])
        #                         else:
        #                             filters+=" AND "+nodes + "="+str(viol[nodes])
        #                     # query = self.constraints[violation_type]['constraint']
        #                     # if(self.neo4j_Connector.query(query.replace("RETURN", filters + " RETURN"))==[]):
        #                     if(len(self.neo4j_Connector.query(constraint['check_new_violation'].replace("FILTRI",filters)))==0):
                                
        #                         new_violations = self.neo4j_Connector.query(constraint['create_new_violation'].replace("FILTRI",filters))
        #                         for v in new_violations:
                                    
        #                             id_v = v['v1'].element_id.split(":")[-1]
        #                             self.grdg.add_node(v) 
        #                             if(id_v not in violations_ids):
        #                                 n_violations.append(id_v)
                                        
        #                         for v in new_violations:
        #                             id_v = v['v1'].element_id.split(":")[-1]
        #                             new_edges=self.neo4j_Connector.query("MATCH (v1:Violation {solved:False})<-[:BELONGS]-(a)-[:BELONGS]-(v2:Violation {solved:False}) WHERE ID(v1)="+str(id_v)+" AND ID(v2)<>"+str(id_v)+" return v1,v2")
                                
        #                             for e in new_edges:
        #                                 self.grdg.add_edge(e)


        #             if(self.grdg.graph.vcount()==0):
        #                 graphInconsistent=False
        #             else:
        #                 self.grdg.compute_betweenness()


        #     t1 = time.time()
        #     if(timedOut):
        #         print("CGR timed out")
        #     else:
        #         print("Graph is consistent")
        #         print("Time elapsed: ", t1-t0)
        #         solved_violations = self.neo4j_Connector.query("MATCH (v:Violation) RETURN v")
        #         precision,recall,f1 = compute_metrics(solved_violations,self.neo4j_Connector)
        #         if(seed2==0):
        #             self.avg_precision=precision
        #             self.avg_recall=recall
        #             self.avg_f1=f1
        #         else:
        #             self.avg_precision=(self.avg_precision*(seed2)+precision)/(seed2+1)
        #             self.avg_recall=(self.avg_recall*(seed2)+recall)/(seed2+1)
        #             self.avg_f1=(self.avg_f1*(seed2)+f1)/(seed2+1)

        #     self.avg_interaction_count=(self.avg_interaction_count*(seed2)+self.interaction_count)/(seed2+1)
        #     self.avg_wait_count=(self.avg_wait_count*(seed2)+self.wait_count)/(seed2+1)
        #     self.avg_iteration_count=(self.avg_iteration_count*(seed2)+self.iteration_count)/(seed2+1)

        # print("Precision: ", self.avg_precision)
        # print("Recall: ",self.avg_recall)
        # print("F1: ", self.avg_f1)
        
        # print("Number of iterations: ", self.avg_iteration_count)
        # print("Number of interactions: ", self.avg_interaction_count)
        # print("Number of waitings: ", self.avg_wait_count)
        # self.neo4j_Connector.merge_query("CALL apoc.export.csv.all('"+self.dataset+"-"+str(self.max_users)+"-"+self.assignment+"-"+str(self.safetiness)+"-"+str(self.error_distribution)+"-"+str(self.answer_distribution)+".csv', {})")
        

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
    
    env = CGREnvironment(dataset=dataset)
    #try:
    env.start_fixed_arrival_simulation()
    #except Exception as e:
    #    print(e)
    
