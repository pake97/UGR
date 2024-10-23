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
from utils.computeRepairsRealPreferred import computeRepairs
from utils.checkSafetyReal import checkSafety
from utils.applyRepair import applyRepair
from utils.restore_graph import restore_graph
from config.sw_query import sw_queries
from utils.restoreConstraints3 import restoreConstraints
from utils.compute_metrics2 import compute_metrics
from agent.user2 import User
from config.synthea_query import synthea_query
from config.icij_query import icij_queries
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
        
        if(self.neo4j_Connector.query("RETURN gds.graph.exists('grdg')")[0]["gds.graph.exists('grdg')"]):
            self.neo4j_Connector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
        time1 = time.time()
        for safetiness in [True,False]:
        #for safetiness in [False]:
            #for mode in ["schema","number","update","delete"]:
            for mode in ["schema"]:
                print("Running icij "+str(mode)+" " +str(safetiness))        
                self.wait_count=0
                self.iteration_count=0
                self.interaction_count=0
                self.users = self.generateUsers(users)
                self.answer_distribution=[answer,1-answer]
                self.safetiness = safetiness
                self.mode=mode
                if(self.neo4j_Connector.query("RETURN gds.graph.exists('grdg')")[0]["gds.graph.exists('grdg')"]):
                    self.neo4j_Connector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
                build_grdg =  self.neo4j_Connector.merge_query("CALL gds.graph.project('grdg', 'Violation', {INTERSECT: {orientation: 'UNDIRECTED'}})")                
                initial_violations=self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) RETURN COUNT(v) as count")[0]['count']
                
                conteggi=[]
                t0 = time.time()
                graphInconsistent = True
                timedOut=False

                #violations_ids = checkConstraints(self.constraints,self.neo4j_Connector, self.assignment)
                #violations_ids = [v['id'] for v in violations_ids]
                random.seed(self.SEED)
                for seed2 in range(10):
                    tstart=time.time()
                    while graphInconsistent: 
                        num_viols=self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) RETURN COUNT(v) as count")
                        print("Num violations:",num_viols)
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
                        if(self.iteration_count>2*initial_violations):
                            timedOut=True 
                            break
                        else:
                            self.iteration_count+=1
                            chosen_repairs=[]
                            chosen_violations=[]


                            
                                
                        assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation {locked : false, solved:false}) RETURN v, rand() as r ORDER BY r LIMIT 1")
                        
                        
                        assigned_hypervertex = assigned_hypervertex[0]
                        
                        violation_id=assigned_hypervertex['v'].element_id.split(":")[-1]                        
                        properties = {}
                        for l, v in assigned_hypervertex['v'].items():
                            properties[l] = v
                        type = int(properties['type'])
                        
                        configs = self.constraints[properties['type']]
                        possible_repairs=[]
                        if(mode=="delete"):
                            for c in configs["delete_preferred"]:
                                possible_repairs.append(c)
                        if(mode=="update"):
                            for c in configs["update_preferred"]:
                                possible_repairs.append(c)
                            
                        if(mode=="number"):
                            for c in configs["num_op_preferred"]:
                                possible_repairs.append(c)
                                
                        if(mode=="schema"):
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
                                
                                chosen_repair=computeRepairs(assigned_hypervertex,properties,chosen_repair['repair'])
                                if(checkSafety(chosen_repair,assigned_hypervertex,self.neo4j_Connector,self.constraints)):
                                    #print(chosen_repair)
                                    applyRepair(chosen_repair,self.neo4j_Connector)  
                                    self.interaction_count+=1      
                                    break
    
                        else:
                            chosen_repair = random.choice(grouped_repairs[0])
                            chosen_repair=computeRepairs(assigned_hypervertex,properties,chosen_repair['repair'])
                            applyRepair(chosen_repair,self.neo4j_Connector)  
                            self.interaction_count+=1      
                        solved_count=+1
                        
                
                            
                            
                        self.interaction_count+=1
                        properties = {}
                        for l, v in assigned_hypervertex['v'].items():
                            properties[l] = v 
                        violation_nodes =str(properties['nodes']).split(",")                        
                        violation_labels =properties['labels'].split(",")
                        type = int(properties['type'])
                        t31 = time.time()         
                        if(type==1):
                            violation_id = assigned_hypervertex['v'].element_id.split(":")[-1] 
                            neighbors=self.neo4j_Connector.query("MATCH (v:Violation)-[:INTERSECT]-(v1:Violation {solved:False}) WHERE ID(v)="+str(violation_id)+" RETURN ID(v1) as id, v1.nodes as nodes, v1.labels as labels, v1.type as type")
                            for ngh in neighbors:
                                ngh_id = ngh['id']
                                nodes_ids=str(ngh['nodes']).split(",")
                                labels=ngh['labels'].split(",")
                                violation_type = int(ngh['type'])
                                if(violation_type==1):
                                    # viol1 = self.neo4j_Connector.query("MATCH (b:Entity)<-[r:officer_of {deleted:false}]-(a)-[p:officer_of {deleted:false}]->(b) where r.link=p.link and apoc.date.parse(r.start_date, 's','MM-dd-yyyy')<apoc.date.parse(p.start_date, 's','MM-dd-yyyy') and (r.end_date is null or r.end_date='' or apoc.date.parse(r.end_date, 's','MM-dd-yyyy')>apoc.date.parse(p.start_date, 's','MM-dd-yyyy')) and ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" RETURN ID(a),ID(b)")
                                    # if(len(viol1)==0):
                                    #     solved_count+=1
                                    #     self.neo4j_Connector.merge_query("MATCH (v:Violation) WHERE ID(v)= "+str(ngh_id)+" SET v.solved=True")
                                    viol1 = self.neo4j_Connector.query("MATCH (a:Other)-[p:same_name_as {deleted:false}]-(b:Entity) where a.name<>b.name and a.name is not null and b.name is not null and ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" RETURN ID(a),ID(b)")
                                    if(len(viol1)==0):
                                        solved_count+=1
                                        self.neo4j_Connector.merge_query("MATCH (v:Violation) WHERE ID(v)= "+str(ngh_id)+" SET v.solved=True")
                                        
                        if(type==2):
                            violation_id = assigned_hypervertex['v'].element_id.split(":")[-1] 
                            neighbors=self.neo4j_Connector.query("MATCH (v:Violation)-[:INTERSECT]-(v1:Violation {solved:False}) WHERE ID(v)="+str(violation_id)+" RETURN ID(v1) as id, v1.nodes as nodes, v1.labels as labels, v1.type as type")
                            for ngh in neighbors:
                                ngh_id = ngh['id']
                                nodes_ids=str(ngh['nodes']).split(",")
                                labels=ngh['labels'].split(",")
                                violation_type = int(ngh['type'])
                                if(violation_type==2):
                                    # viol1 = self.neo4j_Connector.query("MATCH (b:Entity)<-[r:officer_of {deleted:false}]-(a)-[p:officer_of {deleted:false}]->(b) where r.link=p.link and apoc.date.parse(r.start_date, 's','MM-dd-yyyy')<apoc.date.parse(p.start_date, 's','MM-dd-yyyy') and (r.end_date is null or r.end_date='' or apoc.date.parse(r.end_date, 's','MM-dd-yyyy')>apoc.date.parse(p.start_date, 's','MM-dd-yyyy')) and ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" RETURN ID(a),ID(b)")
                                    # if(len(viol1)==0):
                                    #     solved_count+=1
                                    #     self.neo4j_Connector.merge_query("MATCH (v:Violation) WHERE ID(v)= "+str(ngh_id)+" SET v.solved=True")
                                    viol1 = self.neo4j_Connector.query("MATCH (a:Address)-[p:registered_address {deleted:false}]-(b) where apoc.text.indexOf(b.country_codes,a.country_codes)<0 and a.country_codes is not null and b.country_codes is not null and ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" RETURN ID(a),ID(b)")
                                    if(len(viol1)==0):
                                        solved_count+=1
                                        self.neo4j_Connector.merge_query("MATCH (v:Violation) WHERE ID(v)= "+str(ngh_id)+" SET v.solved=True")
                                        
                        if(type==3):
                            violation_id = assigned_hypervertex['v'].element_id.split(":")[-1] 
                            neighbors=self.neo4j_Connector.query("MATCH (v:Violation)-[:INTERSECT]-(v1:Violation {solved:False}) WHERE ID(v)="+str(violation_id)+" RETURN ID(v1) as id, v1.nodes as nodes, v1.labels as labels, v1.type as type")
                            for ngh in neighbors:
                                ngh_id = ngh['id']
                                nodes_ids=str(ngh['nodes']).split(",")
                                labels=ngh['labels'].split(",")
                                violation_type = int(ngh['type'])
                                if(violation_type==3):
                                    # viol1 = self.neo4j_Connector.query("MATCH (b:Entity)<-[r:officer_of {deleted:false}]-(a)-[p:officer_of {deleted:false}]->(b) where r.link=p.link and apoc.date.parse(r.start_date, 's','MM-dd-yyyy')<apoc.date.parse(p.start_date, 's','MM-dd-yyyy') and (r.end_date is null or r.end_date='' or apoc.date.parse(r.end_date, 's','MM-dd-yyyy')>apoc.date.parse(p.start_date, 's','MM-dd-yyyy')) and ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" RETURN ID(a),ID(b)")
                                    # if(len(viol1)==0):
                                    #     solved_count+=1
                                    #     self.neo4j_Connector.merge_query("MATCH (v:Violation) WHERE ID(v)= "+str(ngh_id)+" SET v.solved=True")
                                    viol1 = self.neo4j_Connector.query("MATCH (b:Entity)<-[r:officer_of {deleted:false}]-(a)-[p:officer_of {deleted:false}]->(b) where r.link=p.link and apoc.date.parse(r.start_date, 's','MM-dd-yyyy')<apoc.date.parse(p.start_date, 's','MM-dd-yyyy') and (r.end_date is null or r.end_date='' or apoc.date.parse(r.end_date, 's','MM-dd-yyyy')>apoc.date.parse(p.start_date, 's','MM-dd-yyyy')) and ID(p)="+str(nodes_ids[2])+" and ID(r)="+str(nodes_ids[3])+" RETURN ID(a),ID(b)")
                                    if(len(viol1)==0):
                                        solved_count+=1
                                        self.neo4j_Connector.merge_query("MATCH (v:Violation) WHERE ID(v)= "+str(ngh_id)+" SET v.solved=True")
                        
                        if(not self.safetiness and type>0):    
                            introduced_violations=[]
                            viol11 = self.neo4j_Connector.query("MATCH (a:Other)-[p:same_name_as {deleted:false}]-(b:Entity) where a.name<>b.name and a.name is not null and b.name is not null and ID(a)="+str(violation_nodes[0])+" and ID(b)<>"+str(violation_nodes[1])+" RETURN ID(a),ID(b)")
                            viol12 = self.neo4j_Connector.query("MATCH (a:Other)-[p:same_name_as {deleted:false}]-(b:Entity) where a.name<>b.name and a.name is not null and b.name is not null and ID(a)<>"+str(violation_nodes[0])+" and ID(b)="+str(violation_nodes[1])+" RETURN ID(a),ID(b)")
                            if(len(viol11)>0):    
                                for v in viol11:
                                    if(len(self.neo4j_Connector.query("MATCH (a)-[:BELONGS]->(v:Violation {solved:False})<-[:BELONGS]-(b) where id(a)="+str(v['ID(a)'])+" and id(b)="+str(v['ID(b)'])+" return id(v)"))==0):
                                        new_violations = self.neo4j_Connector.query("MATCH (a:Other)-[p:same_name_as {deleted:false}]-(b:Entity) where a.name<>b.name and a.name is not null and b.name is not null and id(a)="+str(v['ID(a)'])+" and id(b)="+str(v['ID(b)'])+" CREATE (a)-[:BELONGS]->(v1:Violation {solved:False,introduced:True, locked:false, nodes: ID(a)+','+ID(b)+','+ID(p),labels:'a,b,p', type:1})<-[:BELONGS]-(b) RETURN v1")
                                        introduced_violations.extend(new_violations)
                            if(len(viol12)>0):
                                
                                for v in viol12:
                                    if(len(self.neo4j_Connector.query("MATCH (a)-[:BELONGS]->(v:Violation {solved:False})<-[:BELONGS]-(b) where id(a)="+str(v['ID(a)'])+" and id(b)="+str(v['ID(b)'])+" return id(v)"))==0):
                                        new_violations = self.neo4j_Connector.query("MATCH (a:Other)-[p:same_name_as {deleted:false}]-(b:Entity) where a.name<>b.name and a.name is not null and b.name is not null and id(a)="+str(v['ID(a)'])+" and id(b)="+str(v['ID(b)'])+" CREATE (a)-[:BELONGS]->(v1:Violation {solved:False,introduced:True, locked:false, nodes: ID(a)+','+ID(b)+','+ID(p),labels:'a,b,p', type:1})<-[:BELONGS]-(b) RETURN v1")
                                        introduced_violations.extend(new_violations)

                            viol21 = self.neo4j_Connector.query("MATCH (a:Address)-[p:registered_address {deleted:false}]-(b) where apoc.text.indexOf(b.country_codes,a.country_codes)<0 and a.country_codes is not null and b.country_codes is not null and ID(a)="+str(violation_nodes[0])+" and ID(b)<>"+str(violation_nodes[1])+" RETURN ID(a),ID(b)")
                            viol22 = self.neo4j_Connector.query("MATCH (a:Address)-[p:registered_address {deleted:false}]-(b) where apoc.text.indexOf(b.country_codes,a.country_codes)<0 and a.country_codes is not null and b.country_codes is not null and ID(a)<>"+str(violation_nodes[0])+" and ID(b)="+str(violation_nodes[1])+" RETURN ID(a),ID(b)")
                            if(len(viol21)>0):    
                                for v in viol21:
                                    if(len(self.neo4j_Connector.query("MATCH (a)-[:BELONGS]->(v:Violation {solved:False})<-[:BELONGS]-(b) where id(a)="+str(v['ID(a)'])+" and id(b)="+str(v['ID(b)'])+" return id(v)"))==0):
                                        new_violations = self.neo4j_Connector.query("MATCH (a:Address)-[p:registered_address {deleted:false}]-(b) where apoc.text.indexOf(b.country_codes,a.country_codes)<0 and a.country_codes is not null and b.country_codes is not null and id(a)="+str(v['ID(a)'])+" and id(b)="+str(v['ID(b)'])+" CREATE (a)-[:BELONGS]->(v1:Violation {solved:False,introduced:True, locked:false, nodes: ID(a)+','+ID(b)+','+ID(p),labels:'a,b,p', type:2})<-[:BELONGS]-(b) RETURN v1")
                                        introduced_violations.extend(new_violations)
                            if(len(viol22)>0):
                                
                                for v in viol22:
                                    if(len(self.neo4j_Connector.query("MATCH (a)-[:BELONGS]->(v:Violation {solved:False})<-[:BELONGS]-(b) where id(a)="+str(v['ID(a)'])+" and id(b)="+str(v['ID(b)'])+" return id(v)"))==0):
                                        new_violations = self.neo4j_Connector.query("MATCH (a:Address)-[p:registered_address {deleted:false}]-(b) where apoc.text.indexOf(b.country_codes,a.country_codes)<0 and a.country_codes is not null and b.country_codes is not null and id(a)="+str(v['ID(a)'])+" and id(b)="+str(v['ID(b)'])+" CREATE (a)-[:BELONGS]->(v1:Violation {solved:False,introduced:True, locked:false, nodes: ID(a)+','+ID(b)+','+ID(p),labels:'a,b,p', type:2})<-[:BELONGS]-(b) RETURN v1")
                                        introduced_violations.extend(new_violations)      

                            viol31 = self.neo4j_Connector.query("MATCH (b:Entity)<-[r:officer_of {deleted:false}]-(a)-[p:officer_of {deleted:false}]->(b) where r.link=p.link and apoc.date.parse(r.start_date, 's','MM-dd-yyyy')<apoc.date.parse(p.start_date, 's','MM-dd-yyyy') and (r.end_date is null or r.end_date='' or apoc.date.parse(r.end_date, 's','MM-dd-yyyy')>apoc.date.parse(p.start_date, 's','MM-dd-yyyy')) and ID(a)="+str(violation_nodes[0])+" and ID(a)<>"+str(violation_nodes[1])+" RETURN ID(a),ID(b),ID(r),ID(p)")
                            viol32 = self.neo4j_Connector.query("MATCH (b:Entity)<-[r:officer_of {deleted:false}]-(a)-[p:officer_of {deleted:false}]->(b) where r.link=p.link and apoc.date.parse(r.start_date, 's','MM-dd-yyyy')<apoc.date.parse(p.start_date, 's','MM-dd-yyyy') and (r.end_date is null or r.end_date='' or apoc.date.parse(r.end_date, 's','MM-dd-yyyy')>apoc.date.parse(p.start_date, 's','MM-dd-yyyy')) and ID(b)<>"+str(violation_nodes[0])+" and ID(b)="+str(violation_nodes[1])+" RETURN ID(a),ID(b),ID(r),ID(p)")
                            if(len(viol31)>0):    
                                for v in viol31:
                                    if(len(self.neo4j_Connector.query("MATCH (a)-[:BELONGS]->(v:Violation {solved:False})<-[:BELONGS]-(b) where id(a)="+str(v['ID(a)'])+" and id(b)="+str(v['ID(b)'])+" and apoc.text.indexOf(v.nodes,'"+str(v['ID(r)'])+"')<0 and apoc.text.indexOf(v.nodes,'"+str(v['ID(p)'])+"')<0 return id(v)"))==0):
                                        new_violations = self.neo4j_Connector.query("MATCH (b:Entity)<-[r:officer_of {deleted:false}]-(a)-[p:officer_of {deleted:false}]->(b) where r.link=p.link and apoc.date.parse(r.start_date, 's','MM-dd-yyyy')<apoc.date.parse(p.start_date, 's','MM-dd-yyyy') and (r.end_date is null or r.end_date='' or apoc.date.parse(r.end_date, 's','MM-dd-yyyy')>apoc.date.parse(p.start_date, 's','MM-dd-yyyy')) AND id(a)="+str(v['ID(a)'])+" and id(b)="+str(v['ID(b)'])+" AND id(r)="+str(v['ID(r)'])+" and id(p)="+str(v['ID(p)'])+" CREATE (a)-[:BELONGS]->(v1:Violation {solved:False,introduced:True, locked:false, nodes: ID(a)+','+ID(b)+','+ID(p)+','+ID(r),labels:'a,b,p,r', type:3})<-[:BELONGS]-(b) RETURN v1")
                                        introduced_violations.extend(new_violations)
                            if(len(viol32)>0):
                                
                                for v in viol32:
                                    if(len(self.neo4j_Connector.query("MATCH (a)-[:BELONGS]->(v:Violation {solved:False})<-[:BELONGS]-(b) where id(a)="+str(v['ID(a)'])+" and id(b)="+str(v['ID(b)'])+" and apoc.text.indexOf(v.nodes,'"+str(v['ID(r)'])+"')<0 and apoc.text.indexOf(v.nodes,'"+str(v['ID(p)'])+"')<0 return id(v)"))==0):
                                        new_violations = self.neo4j_Connector.query("MATCH (b:Entity)<-[r:officer_of {deleted:false}]-(a)-[p:officer_of {deleted:false}]->(b) where r.link=p.link and apoc.date.parse(r.start_date, 's','MM-dd-yyyy')<apoc.date.parse(p.start_date, 's','MM-dd-yyyy') and (r.end_date is null or r.end_date='' or apoc.date.parse(r.end_date, 's','MM-dd-yyyy')>apoc.date.parse(p.start_date, 's','MM-dd-yyyy')) AND id(a)="+str(v['ID(a)'])+" and id(b)="+str(v['ID(b)'])+" AND id(r)="+str(v['ID(r)'])+" and id(p)="+str(v['ID(p)'])+" CREATE (a)-[:BELONGS]->(v1:Violation {solved:False,introduced:True, locked:false, nodes: ID(a)+','+ID(b)+','+ID(p)+','+ID(r),labels:'a,b,p,r', type:3})<-[:BELONGS]-(b) RETURN v1")
                                        introduced_violations.extend(new_violations)
                            
                            for iv in introduced_violations:
                                id_v = iv['v1'].element_id.split(":")[-1]
                                new_edges=self.neo4j_Connector.merge_query("MATCH (v1:Violation {solved:False})<-[:BELONGS]-(a)-[:BELONGS]-(v2:Violation {solved:False}) WHERE ID(v1)="+str(id_v)+" AND ID(v2)<>"+str(id_v)+" AND NOT (v1)-[:INTERSECT]-(v2) MERGE (v1)-[:INTERSECT]-(v2)")                                                         
                        print("Solved count: ", solved_count)
                        t32 = time.time()
                        print("Diramation time: ", t32-t31)
                        
                        
                        if(self.neo4j_Connector.query("MATCH (v:Violation {solved:false}) RETURN count(v) as vcount")[0]['vcount']==0):
                            graphInconsistent=False
                        else:
                            solvedViolations = self.neo4j_Connector.query("MATCH (v:Violation {solved:true}) RETURN ID(v) as id")
                            for v in solvedViolations:
                                self.neo4j_Connector.query("MATCH (v:Violation) WHERE ID(v)="+str(v['id'])+" CALL apoc.refactor.rename.label('Violation', 'SolvedViolation', [v]) YIELD committedOperations RETURN committedOperations")
                            #self.neo4j_Connector.merge_query("CALL apoc.periodic.iterate('MATCH (sv:SolvedViolation)-[r:INTERSECT]-() return r','MATCH (a)-[r]-(b) delete r', {batchSize:10, parallel:false,iterateList:true})")
                            self.neo4j_Connector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
                            self.neo4j_Connector.merge_query("MATCH (v:Violation {locked:true}) SET v.locked=false")
                            build_grdg =  self.neo4j_Connector.merge_query("CALL gds.graph.project('grdg', 'Violation', {INTERSECT: {orientation: 'UNDIRECTED'}})")
                            t42 = time.time()
                            print("Update time: ", t42-t32)
                                
                                
                            
                    print("Finish repairing the graph")            
                    tend=time.time()
                    print("Total time: ", tend-tstart)
                    #todo:
                    
                    
                    
                    
                    #compute final metrics
                    print("Iteration count: ", self.iteration_count)
                    print("Interaction count: ", self.interaction_count)
                    self.iteration_count=0
                    self.interaction_count=0
                    
                    tp=0
                    fp=0
                    fn=0
                    tn=0
                    
                    
                    involved_s1=self.neo4j_Connector.query("match (s:SolvedViolation {type:0}) return s.nodes as ida")
                    
                    for is1 in involved_s1:
                        ida=is1['ida']
                        node_is1 = self.neo4j_Connector.query("match (n) where ID(n)="+str(ida)+" return n.status as status, n.inactivation_date as inactivation_date, n.status_gt as status_gt, n.inactivation_date_gt as inactivation_date_gt, n.initial_status as initial_status, n.initial_inactivation_date as initial_inactivation_date")[0]
                        
                        if(node_is1['status']!=node_is1['status_gt']):
                            if(node_is1['status']==node_is1['initial_status']):
                                fn+=1
                            else:
                                fp+=1
                        else:
                            if(node_is1['status']!=node_is1['initial_status']):
                                tp+=1
                            else:
                                tn+=1
                                
                        if(node_is1['inactivation_date']!=node_is1['inactivation_date_gt']):
                            if(node_is1['inactivation_date']==node_is1['initial_inactivation_date']):
                                fn+=1
                            else:
                                fp+=1
                        else:
                            if(node_is1['inactivation_date']!=node_is1['initial_inactivation_date']):
                                tp+=1    
                            else:
                                tn+=1
                        
                    
                    involved_s2=self.neo4j_Connector.query("match (s:SolvedViolation {type:1}) with split(s.nodes,',') as snodes return snodes[0] as ida, snodes[1] as idb,snodes[2] as idp")
                    for is2 in involved_s2:
                        ida=is2['ida']
                        node1_is2 = self.neo4j_Connector.query("match (n) where ID(n)="+str(ida)+" return n.name as name, n.initial_name as initial_name, n.name_gt as name_gt")[0]
                        if(node1_is2['name']!=node1_is2['name_gt']):
                            if(node1_is2['name']==node1_is2['initial_name']):
                                fn+=1
                            else:
                                fp+=1
                        else:
                            if(node1_is2['name']!=node1_is2['initial_name']):
                                tp+=1
                            else:
                                tn+=1
                                    
                        idb=is2['idb']
                        node2_is2 = self.neo4j_Connector.query("match (n) where ID(n)="+str(idb)+" return n.name as name, n.initial_name as initial_name, n.name_gt as name_gt")[0]
                        if(node2_is2['name']!=node2_is2['name_gt']):
                            if(node2_is2['name']==node2_is2['initial_name']):
                                fn+=1
                            else:
                                fp+=1
                        else:
                            if(node2_is2['name']!=node2_is2['initial_name']):
                                tp+=1  
                            else:
                                tn+=1
                        idp=is2['idp']
                        node3_is2 = self.neo4j_Connector.query("match ()-[r]-() where ID(r)="+str(idp)+" return r.deleted as deleted")[0]
                        if(node3_is2['deleted']):
                            fp+=1
                        else:
                            tn+=1
                        
                        
                    
                    involved_s3=self.neo4j_Connector.query("match (s:SolvedViolation {type:2}) with split(s.nodes,',') as snodes return snodes[0] as ida, snodes[1] as idb,snodes[2] as idp")
                    for is3 in involved_s3:
                        ida=is3['ida']
                        try:
                            node1_is3 = self.neo4j_Connector.query("match (n) where ID(n)="+str(ida)+" return n.country_codes as country_codes, n.initial_country_codes as initial_country_codes, n.country_codes_gt as country_codes_gt")[0]
                            if(node1_is3['country_codes']!=node1_is3['country_codes_gt']):
                                if(node1_is3['country_codes']==node1_is3['initial_country_codes']):
                                    fn+=1
                                else:
                                    fp+=1
                            else:
                                if(node1_is3['country_codes']!=node1_is3['initial_country_codes']):
                                    tp+=1  
                                else:
                                    tn+=1
                            idb=is3['idb']
                            node2_is3 = self.neo4j_Connector.query("match (n) where ID(n)="+str(idb)+" return n.country_codes as country_codes, n.initial_country_codes as initial_country_codes, n.country_codes_gt as country_codes_gt")[0]
                            if(node2_is3['country_codes']!=node2_is3['country_codes_gt']):
                                if(node2_is3['country_codes']==node2_is3['initial_country_codes']):
                                    fn+=1
                                else:
                                    fp+=1
                            else:
                                if(node2_is3['country_codes']!=node2_is3['initial_country_codes']):
                                    tp+=1  
                                else:
                                    tn+=1
                            idp=is3['idp']
                            node3_is3 = self.neo4j_Connector.query("match ()-[r]-() where ID(r)="+str(idp)+" return r.deleted as deleted")[0]
                            if(node3_is3['deleted']):
                                fp+=1
                            else:
                                tn+=1
                        except:
                            print("Error","match (n) where ID(n)="+str(ida)+" return n.country_codes as country_codes, n.initial_country_codes as initial_country_codes, n.country_codes_gt as country_codes_gt")
                            print(is3)
                    involved_s4=self.neo4j_Connector.query("match (s:SolvedViolation {type:3}) with split(s.nodes,',') as snodes return snodes[0] as ida, snodes[1] as idb,snodes[2] as idp,snodes[3] as idr")
                    for is4 in involved_s4:
                        idp=is4['idp']
                        try:
                            node3_is4 = self.neo4j_Connector.query("match ()-[r]-() where ID(r)="+str(idp)+" return r.deleted as deleted, r.deleted_gt as deleted_gt, r.link as link,r.link_gt as link_gt, r.initial_link as initial_link")[0]
                            if(node3_is4['deleted']):
                                if(node3_is4["deleted"]==node3_is4["deleted_gt"]):
                                    tp+=1
                                else:
                                    fp+=1
                            else:
                                if(node3_is4["link"]==node3_is4["link_gt"]):
                                    if(node3_is4["link"]!=node3_is4["initial_link"]):
                                        tp+=1
                                    else:
                                        tn+=1
                                else:
                                    if(node3_is4["link"]==node3_is4["initial_link"]):
                                        fn+=1
                                    else:
                                        fp+=1
                                    
                            idr=is4['idr']        
                            node4_is4 = self.neo4j_Connector.query("match ()-[r]-() where ID(r)="+str(idr)+" return r.deleted as deleted, r.deleted_gt as deleted_gt, r.link as link,r.link_gt as link_gt, r.initial_link as initial_link")[0]
                            if(node4_is4['deleted']):
                                if(node4_is4["deleted"]==node4_is4["deleted_gt"]):
                                    tp+=1
                                else:
                                    fp+=1
                            else:
                                if(node4_is4["link"]==node4_is4["link_gt"]):
                                    if(node4_is4["link"]!=node4_is4["initial_link"]):
                                        tp+=1
                                    else:
                                        tn+=1
                                else:
                                    if(node4_is4["link"]==node4_is4["initial_link"]):
                                        fn+=1
                                    else:
                                        fp+=1
                        except:
                            print("Error","match ()-[r]-() where ID(r)="+str(idp)+" return r.deleted as deleted, r.deleted_gt as deleted_gt, r.link as link,r.link_gt as link_gt, r.initial_link as initial_link")
                            print(is4)
                    print("TP: ", tp)
                    print("FP: ", fp)
                    print("FN: ", fn)
                    print("TN: ", tn)
                    try:
                        precision = tp/(tp+fp)
                        recall = tp/(tp+fn)
                        accuracy = (tp+tn)/(tp+fn)
                        f1 = 2*(precision*recall)/(precision+recall)
                        print("Precision: ", precision)
                        print("Recall: ", recall)
                        print("F1: ", f1)
                        print("Accuracy: ", accuracy)
                    except:
                        print("Error f1")
                    
                    
                    
                    self.neo4j_Connector.merge_query("MATCH (s:SolvedViolation {type:0})<--(a:Entity) set a.status=a.initial_status, a.inactivation_date=a.initial_inactivation_date, a.updated=False")
                    self.neo4j_Connector.merge_query("MATCH (s:SolvedViolation {type:1})<--(a:Other)-[p:same_name_as]-(b:Entity)-->(s) set a.name=a.initial_name, b.name=b.initial_name, a.updated=False, b.updated=False, p.deleted=False, p.updated=False")
                    self.neo4j_Connector.merge_query("MATCH (s:SolvedViolation {type:2})<--(a:Address)-[p:registered_address]-(b)-->(s) set a.country_codes=a.initial_country_codes,b.country_codes=b.initial_country_codes, a.updated=False, p.deleted=False, p.updated=False")
                    self.neo4j_Connector.merge_query("MATCH (s:SolvedViolation {type:3})<--(b:Entity)-[r:officer_of]-(a)-[p:officer_of]->(b), (a)--(s) set r.link=r.initial_link, p.link=p.initial_link,  p.deleted=False, p.updated=False, r.deleted=False, r.updated=False")
                    
                    
                    
                    self.neo4j_Connector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
                    self.neo4j_Connector.merge_query("CALL apoc.refactor.rename.label('SolvedViolation', 'Violation') YIELD committedOperations RETURN committedOperations")
                    solved_violations = self.neo4j_Connector.merge_query("MATCH (v {introduced:True}) detach delete v")
                    solved_violations = self.neo4j_Connector.merge_query("MATCH (v {solved:True}) set v.solved=False")
                    self.neo4j_Connector.merge_query("MATCH (v:Violation {locked:true}) SET v.locked=false")
                    
                    
                    #self.neo4j_Connector.query("MATCH (v:Violation) WHERE ID(v)="+str(v['id'])+" CALL apoc.refactor.rename.label('Violation', 'SolvedViolation', [v]) YIELD committedOperations RETURN committedOperations")
                    
                    build_grdg =  self.neo4j_Connector.merge_query("CALL gds.graph.project('grdg', 'Violation', {INTERSECT: {orientation: 'UNDIRECTED'}})")
                    
                
                    
                    conteggi=[]
                    graphInconsistent = True
                    timedOut=False
                            
                            
                            
                                
                            
                
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
        if dataset == "icij":
            return icij_queries
    
    def generateUsers(self,max_users):
        users = []
        for i in range(max_users):
            users.append(User("tutti"))
        return users


# Example Usage
if __name__ == "__main__":
    
    #python3 environment3.py $dataset $safety $assignment $users $error $answer
    dataset = 'icij'
    safetiness = "True"
    assignment = 'degreeAsc'
    users = 20
    answer = 0
    
    env = CGREnvironment(max_users=users, dataset=dataset,safetiness= safetiness, timeout=3600, assignment=assignment,error_distribution=0, SEED = 1, user_distribution=[1,1,1], answer_distribution=[answer,1-answer])
    #try:
    env.start_fixed_arrival_simulation()
    #except Exception as e:
    #   print(e)
    
