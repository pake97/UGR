import json
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
    def __init__(self, dataset="movies", violations=20):
        self.counter = 0
        self.running = False
        self.dataset = dataset
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
        self.SEED=1
        self.violations = violations
        self.answer_distribution=[1,0]
        self.users=self.generateUsers(1)
        self.assignment="degreeAsc"
        
        

    def start_fixed_arrival_simulation(self,seed,theta,strategy):
        #print("Clearing dataset")
        constraints = []
        allowed_neighbors = {
            'Filing': ['Entity'],
            'Entity': ['Entity', 'Country', 'Filing'],
            'Country': ['Entity']
        }
        
        all_labels=['Entity', 'Filing', 'Country']
        diramation_constraints = []
        self.neo4j_Connector.clearNeo4j()
        # #print("Loading dataset")
        self.neo4j_Connector.loadDatasetToNeo4j(self.dataset)
        if(self.neo4j_Connector.query("RETURN gds.graph.exists('grdg')")[0]["gds.graph.exists('grdg')"]):
            self.neo4j_Connector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
        if(self.neo4j_Connector.query("RETURN gds.graph.exists('enti')")[0]["gds.graph.exists('enti')"]):
            self.neo4j_Connector.merge_query("CALL gds.graph.drop('enti') YIELD graphName;")
        self.neo4j_Connector.merge_query("CALL gds.graph.project('enti', ['Entity', 'Filing'],['FILED', 'CONCERNS'])")
        self.neo4j_Connector.merge_query("CALL gds.degree.write('enti', { writeProperty: 'degree' }) YIELD centralityDistribution, nodePropertiesWritten RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten")
        labels = self.neo4j_Connector.query("CALL db.labels()")
        labels = [label['label'] for label in labels]
        synthetic_properties = self.neo4j_Connector.query("MATCH (a) set a.updated=False, a.synthlabel=labels(a)[0]")
        synthetic_properties = self.neo4j_Connector.query("MATCH ()-[r]-() set r.updated=False, r.deleted=False")
        half_violations = int(self.violations/2)
        tuples = self.neo4j_Connector.query("MATCH (e:Entity {synthlabel:'Entity'}) WHERE e.degree>0 and e.degree<10 return ID(e) LIMIT "+str(half_violations))
        c_tuples = self.neo4j_Connector.query("MATCH (e:Country {synthlabel:'Country'}) return ID(e) LIMIT "+str(int(half_violations/2)))
        f_tuples = self.neo4j_Connector.query("MATCH (e:Filing {synthlabel:'Filing'}) return ID(e) LIMIT "+str(int(half_violations/2)))
        for count, t in enumerate(tuples):
            if(count%2==0):
                self.neo4j_Connector.merge_query("MATCH (e:Entity) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Filing', e.injected=True")
            else:
                self.neo4j_Connector.merge_query("MATCH (e:Entity) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Country', e.injected=True")
        for t in c_tuples:
            self.neo4j_Connector.merge_query("MATCH (e:Country) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Entity', e.injected=True")
        for t in f_tuples:
            self.neo4j_Connector.merge_query("MATCH (e:Filing) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Entity', e.injected=True")
        
        
        
        self.neo4j_Connector.merge_query("MATCH (n) set n.updated=False")
        self.neo4j_Connector.merge_query("MATCH (n)-[r]-(m) set r.deleted=False")    
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Filing'})-[r {deleted:False}]-(m {synthlabel:'Filing'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:0})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Country'})-[r {deleted:False}]-(m {synthlabel:'Filing'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:1})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Country'})-[r {deleted:False}]-(m {synthlabel:'Country'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:2})<-[:BELONGS]-(m)")
        
        
        self.neo4j_Connector.merge_query("MATCH (v1:Violation)<-[:BELONGS]-(a)-[:BELONGS]->(v2:Violation) WHERE id(v1)<>id(v2) and not (v1)-[:INTERSECT]-(v2) merge (v1)-[:INTERSECT]-(v2)")
        
        build_grdg =  self.neo4j_Connector.merge_query("CALL gds.graph.project('grdg', 'Violation', {INTERSECT: {orientation: 'UNDIRECTED'}})")
        #compute_pr = self.neo4j_Connector.query("CALL gds.pageRank.write('grdg', { writeProperty: 'pageRank' , maxIterations: 20, dampingFactor: 0.85 }) YIELD centralityDistribution, nodePropertiesWritten RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten,centralityDistribution.max AS maximumScore")
        compute_dg = self.neo4j_Connector.query("CALL gds.degree.write('grdg', { writeProperty: 'degree' }) YIELD centralityDistribution, nodePropertiesWritten RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten") 
        
        violations_ids = []
        n_violations = []
        initial_count = 0
        time1 = time.time()
        
        self.wait_count=0
        self.iteration_count=0
        self.interaction_count=0
        
        graphInconsistent = True
        # t0 = time.time()
        timedOut=False
        #print("Starting CGR")
        first_iteration=True
        previous_count=0
        stuck=[]                        
        random.seed(seed)
        conteggi=[]
        while graphInconsistent: 
            num_viols=self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) RETURN COUNT(v) as count")
            
            #print(num_viols)
            if(first_iteration):
                initial_count=num_viols[0]['count']
                previous_count=num_viols[0]['count']
                first_iteration=False
            else:
                #print(stuck)
                if(num_viols[0]['count']==previous_count):
                    stuck.append(1)
                else:
                    stuck=[]
                previous_count=num_viols[0]['count']
            if(self.iteration_count>0.5*initial_count):
                timedOut=True 
                break
            else:
                self.iteration_count+=1
                assigned_hypervertex = self.neo4j_Connector.query("match (a)-[:BELONGS]->(q:Violation) return id(a),a.synthlabel as asynthlabel,count(q) as count order by count desc limit 1")
            
                connected_violations = self.neo4j_Connector.query("MATCH (n)-[:BELONGS]->(v:Violation) WHERE ID(n)="+str(assigned_hypervertex[0]['id(a)'])+" RETURN ID(v)")
                possible_relabels = set(all_labels)
                ng_labels=[]
                #the possible relabels for the node are the intersection of the allowed neighbors of the connected violations
                
                for cv in connected_violations:
                    ngs = self.neo4j_Connector.query("MATCH (n)-[:BELONGS]->(v:Violation)<-[:BELONGS]-(m) WHERE ID(v)="+str(cv['ID(v)'])+" AND id(n)="+str(assigned_hypervertex[0]['id(a)'])+" RETURN m.synthlabel as label")
                    ng_labels.append(ngs[0]['label'])
                    allowed_ngs_labels = set(allowed_neighbors[ngs[0]['label']])
                    possible_relabels = possible_relabels.intersection(allowed_ngs_labels)
                    
                #grepair relabels only assigned_hypervertex
                cost_relabel=1
                relabel=False
                if(len(stuck)>10):
                    relabel=False
                else:
                    if(len(list(possible_relabels))==0):
                        relabel=False
                    else:
                        #cost of deletions = number of edges = number of connected violations
                        cost_deletions = len(connected_violations)
                        choice = theta * cost_deletions > (1-theta) * cost_relabel
                        
                        if(choice):
                            relabel = True
                        else:
                            relabel = False
                    
                if(relabel):
                    new_label=""
                    self.interaction_count+=1
                   
                    new_label = random.choice(list(possible_relabels))    
                   
                    
                    self.neo4j_Connector.merge_query("MATCH (n) WHERE ID(n)="+str(assigned_hypervertex[0]['id(a)'])+" SET n.updated=True, n.synthlabel='"+new_label+"'")
                else:
                    #print("Deletion", str(assigned_hypervertex[0]['id(a)']))
                    self.interaction_count+=len(connected_violations)
                    self.neo4j_Connector.merge_query("MATCH (n)-[:BELONGS]->(v:Violation)<-[:BELONGS]-(m)-[r]-(n) WHERE id(n)="+str(assigned_hypervertex[0]['id(a)'])+" set r.deleted=True")
                

                #delete all violations
                #num_viols=self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) RETURN COUNT(v) as count")
            
                #print(num_viols)
                self.neo4j_Connector.merge_query("MATCH (v:Violation) detach delete v")
                #rerun constraints 
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Filing'})-[r {deleted:False}]-(m {synthlabel:'Filing'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:0})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Country'})-[r {deleted:False}]-(m {synthlabel:'Filing'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:1})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Country'})-[r {deleted:False}]-(m {synthlabel:'Country'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:2})<-[:BELONGS]-(m)")
        

                if(len(self.neo4j_Connector.query("MATCH (v:Violation {solved:false}) RETURN v"))==0):
                    graphInconsistent=False
                else:
                    
                    self.neo4j_Connector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
                    self.neo4j_Connector.merge_query("MATCH (v1:Violation)<-[:BELONGS]-(a)-[:BELONGS]->(v2:Violation) WHERE id(v1)<>id(v2) and not (v1)-[:INTERSECT]-(v2) merge (v1)-[:INTERSECT]-(v2)")
                
                    
                    t0 = time.time()
                    build_grdg =  self.neo4j_Connector.merge_query("CALL gds.graph.project('grdg', 'Violation', {INTERSECT: {orientation: 'UNDIRECTED'}})")
                    #compute_pr = self.neo4j_Connector.query("CALL gds.pageRank.write('grdg', { writeProperty: 'pageRank' , maxIterations: 20, dampingFactor: 0.85 }) YIELD centralityDistribution, nodePropertiesWritten RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten,centralityDistribution.max AS maximumScore")
                    compute_dg = self.neo4j_Connector.query("CALL gds.degree.write('grdg', { writeProperty: 'degree' }) YIELD centralityDistribution, nodePropertiesWritten RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten") 
                    t3 = time.time()
                                    
                t22 = time.time()
                

        t1 = time.time()
        if(timedOut):
            print("CGR timed out")
        else:
            print("Graph is consistent")
            
        touched_nodes = self.neo4j_Connector.query("MATCH (n) where n.injected=True or n.updated=true return n, labels(n)[0] as label")
        touched_edges = self.neo4j_Connector.query("MATCH (n)-[r]-(m) where r.deleted=True return r")
        true_positives_nodes = 0
        false_positives_nodes = 0
        false_negatives_nodes = 0
        true_negatives_nodes = 0
        true_positives_edges = 0
        false_positives_edges = 0
        false_negatives_edges = 0
        true_negatives_edges = 0
        for node in touched_nodes:
            properties = {}
            for l, v in node['n'].items():
                properties[l] = v 
            if(not properties['synthlabel']==node['label'] and not properties['updated']):
                false_negatives_nodes+=1   
            if(not properties['synthlabel']==node['label'] and properties['updated']):
                false_positives_nodes+=1
            if(properties['synthlabel']==node['label'] and properties['updated']):
                true_positives_nodes+=1
            if(properties['synthlabel']==node['label'] and not properties['updated']):
                true_negatives_nodes+=1
        for edge in touched_edges:
            properties = {}
            for l, v in edge['r'].items():
                properties[l] = v 
            if(properties['deleted']):
                false_positives_edges+=1

        
        
        true_positives = true_positives_nodes + true_positives_edges
        false_positives = false_positives_nodes + false_positives_edges
        false_negatives = false_negatives_nodes + false_negatives_edges

        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            
        # print("Precision: ", precision)
        # print("Recall: ", recall)
        # print("F1: ", f1_score)
        
        
        # print("interaction count: ", self.interaction_count)
        # print("iteration count: ", self.iteration_count)
        # print("wait count: ", self.wait_count)
        

        time2 = time.time()
        return (not timedOut),precision, recall, f1_score, time2-time1, self.interaction_count, self.iteration_count, self.wait_count
         
    def generateUsers(self,max_users):
        users = []
        for i in range(max_users):
            users.append(User("tutti"))
        return users


# Example Usage
if __name__ == "__main__":
    dataset = 'fincen'
    violations = '100'
    env = CGREnvironment(dataset=dataset, violations=int(violations))
    for strategy in ['base']:
        for theta in [1,0.6,0.4,0]:
        #try:
            precs = []
            recs = []
            f1s = []
            times = []
            interactions = []
            iterations = []
            waits = []
            for i in range(10):
                term,precision, recall, f1_score, t, interaction_count, iteration_count, wait_count=env.start_fixed_arrival_simulation(i,theta, strategy)
                if(term):
                    precs.append(precision)
                    recs.append(recall)
                    f1s.append(f1_score)
                    times.append(t)
                    interactions.append(interaction_count)
                    iterations.append(iteration_count)
                    waits.append(wait_count)
            print("Terminated",len(precs))
            print("Precision: ", np.mean(precs))
            print("Recall: ", np.mean(recs))
            print("F1: ", np.mean(f1s))
            print("Time: ", np.mean(times))
            print("Interactions: ", np.mean(interactions))
            print("Iterations: ", np.mean(iterations))
            print("Waits: ", np.mean(waits))
    
    #except Exception as e:
    #    print(e)
    
