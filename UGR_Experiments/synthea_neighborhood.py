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

import string
from math import inf




class CGREnvironment:
    def __init__(self, dataset="movies", violations=20, answer=1):
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
        self.answer_distribution=[answer,1-answer]
        self.users=self.generateUsers(20)
        self.assignment="prAsc"
        
        

    def start_fixed_arrival_simulation(self, seed):
        #print("Clearing dataset")
        constraints = []
        diramation_constraints = []
        self.neo4j_Connector.clearNeo4j()
        # #print("Loading dataset")
        self.neo4j_Connector.loadDatasetToNeo4j(self.dataset)
        if(self.neo4j_Connector.query("RETURN gds.graph.exists('grdg')")[0]["gds.graph.exists('grdg')"]):
            self.neo4j_Connector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
        """ if(self.neo4j_Connector.query("RETURN gds.graph.exists('enti')")[0]["gds.graph.exists('enti')"]):
            self.neo4j_Connector.merge_query("CALL gds.graph.drop('enti') YIELD graphName;")
        self.neo4j_Connector.merge_query("CALL gds.graph.project('enti', ['Entity', 'Filing'],['FILED', 'CONCERNS'])")
        self.neo4j_Connector.merge_query("CALL gds.degree.write('enti', { writeProperty: 'degree' }) YIELD centralityDistribution, nodePropertiesWritten RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten") """
        synthetic_properties = self.neo4j_Connector.query("MATCH (a) set a.updated=False, a.synthlabel=labels(a)[0]")
        synthetic_properties = self.neo4j_Connector.query("MATCH ()-[r]-() set r.updated=False, r.deleted=False")
        half_violations = 2
        
        p_tuples = self.neo4j_Connector.query("MATCH (e:Patient {synthlabel:'Patient'}) return ID(e) LIMIT " + str(int(half_violations)))
        payer_tuples = self.neo4j_Connector.query("MATCH (e:Payer {synthlabel:'Payer'}) return ID(e) LIMIT " + str(int(half_violations)))
        organization_tuples = self.neo4j_Connector.query("MATCH (e:Organization {synthlabel:'Organization'}) return ID(e) LIMIT " + str(int(half_violations)))
        provider_tuples = self.neo4j_Connector.query("MATCH (e:Provider {synthlabel:'Provider'}) return ID(e) LIMIT " + str(int(half_violations)))
        drug_tuples = self.neo4j_Connector.query("MATCH (e:Drug {synthlabel:'Drug'}) return ID(e) LIMIT " + str(int(half_violations)))
        condition_tuples = self.neo4j_Connector.query("MATCH (e:Condition {synthlabel:'Condition'}) return ID(e) LIMIT " + str(int(half_violations)))
        careplan_tuples = self.neo4j_Connector.query("MATCH (e:CarePlan {synthlabel:'CarePlan'}) return ID(e) LIMIT " + str(int(half_violations)))
        allergy_tuples = self.neo4j_Connector.query("MATCH (e:Allergy {synthlabel:'Allergy'}) return ID(e) LIMIT " + str(int(half_violations)))
        address_tuples = self.neo4j_Connector.query("MATCH (e:Address {synthlabel:'Address'}) return ID(e) LIMIT " + str(int(half_violations)))
        procedure_tuples = self.neo4j_Connector.query("MATCH (e:Procedure {synthlabel:'Procedure'}) return ID(e) LIMIT " + str(int(half_violations)))
        observation_tuples = self.neo4j_Connector.query("MATCH (e:Observation {synthlabel:'Observation'}) return ID(e) LIMIT " + str(int(half_violations)))

        
        for count, t in enumerate(p_tuples):
            if(count%2==0):
                self.neo4j_Connector.merge_query("MATCH (e:Patient) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Provider', e.injected=True")
            else:
                self.neo4j_Connector.merge_query("MATCH (e:Patient) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Address', e.injected=True")
        for count, t in enumerate(payer_tuples):
            if(count%2==0):
                self.neo4j_Connector.merge_query("MATCH (e:Payer) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='CarePlan', e.injected=True")
            else:
                self.neo4j_Connector.merge_query("MATCH (e:Payer) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Drug', e.injected=True")
        for count, t in enumerate(provider_tuples):
            if(count%2==0):
                self.neo4j_Connector.merge_query("MATCH (e:Provider) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Organization', e.injected=True")
            else:
                self.neo4j_Connector.merge_query("MATCH (e:Provider) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='CarePlan', e.injected=True")
        for count, t in enumerate(drug_tuples):
            if(count%2==0):
                self.neo4j_Connector.merge_query("MATCH (e:Drug) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Provider', e.injected=True")
            else:
                self.neo4j_Connector.merge_query("MATCH (e:Drug) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Address', e.injected=True")
        for count, t in enumerate(condition_tuples):
            if(count%2==0):
                self.neo4j_Connector.merge_query("MATCH (e:Condition) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Provider', e.injected=True")
            else:
                self.neo4j_Connector.merge_query("MATCH (e:Condition) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Address', e.injected=True")
        for count, t in enumerate(careplan_tuples):
            if(count%2==0):
                self.neo4j_Connector.merge_query("MATCH (e:CarePlan) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Provider', e.injected=True")
            else:
                self.neo4j_Connector.merge_query("MATCH (e:CarePlan) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Address', e.injected=True")
        for count, t in enumerate(allergy_tuples):
            if(count%2==0):
                self.neo4j_Connector.merge_query("MATCH (e:Allergy) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Address', e.injected=True")
            else:
                self.neo4j_Connector.merge_query("MATCH (e:Allergy) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Provider', e.injected=True")
        for count, t in enumerate(address_tuples):
            if(count%2==0):
                self.neo4j_Connector.merge_query("MATCH (e:Address) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Drug', e.injected=True")
            else:
                self.neo4j_Connector.merge_query("MATCH (e:Address) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Observation', e.injected=True")
        for count, t in enumerate(procedure_tuples):
            if(count%2==0):
                self.neo4j_Connector.merge_query("MATCH (e:Procedure) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Provider', e.injected=True")
            else:
                self.neo4j_Connector.merge_query("MATCH (e:Procedure) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Address', e.injected=True")
        for count, t in enumerate(observation_tuples):
            if(count%2==0):
                self.neo4j_Connector.merge_query("MATCH (e:Observation) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Address', e.injected=True")
            else:
                self.neo4j_Connector.merge_query("MATCH (e:Observation) WHERE ID(e)="+str(t['ID(e)'])+" SET e.synthlabel='Provider', e.injected=True")
        
        
        
        
        self.neo4j_Connector.merge_query("MATCH (n) set n.updated=False")
        self.neo4j_Connector.merge_query("MATCH (n)-[r]-(m) set r.deleted=False")    
        self.neo4j_Connector.merge_query("CALL apoc.export.csv.all('synthea_neighborhood.csv', {})")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Organization'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:0})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:1})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:2})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Condition'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:3})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Allergy'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:4})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'CarePlan'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:5})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Observation'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:6})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Procedure'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:7})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:8})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:9})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:10})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:11})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Observation'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:12})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Procedure'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:13})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Condition'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:14})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:15})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Organization'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:16})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Procedure'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:17})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:18})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:19})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Procedure'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:20})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Condition'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:21})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:22})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Organization'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:23})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:24})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:25})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:26})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Observation'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:27})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Condition'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:28})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:29})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Organization'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:30})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Condition'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:31})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Condition'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:32})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Condition'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:33})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Condition'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:34})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Condition'})-[r {deleted:False}]-(m {synthlabel:'Organization'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:35})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Encounter'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:36})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Encounter'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:37})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Organization'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:38})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Provider'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:39})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Provider'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:40})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Address'})-[r {deleted:False}]-(m {synthlabel:'Drugt'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:41})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Patient'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:42})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:43})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Organization'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:44})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:45})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Payer'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:46})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'CarePlan'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:47})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Observation'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:48})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:49})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Procedure'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:50})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Payer'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:51})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Provider'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:52})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Address'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:53})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Patient'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:54})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Allergy'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:55})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'CarePlan'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:56})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Provider'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:57})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Procedure'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:58})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Observation'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:59})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Drug'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:60})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Condition'})-[r {deleted:False}]-(m {synthlabel:'Condition'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:61})<-[:BELONGS]-(m)")
        self.neo4j_Connector.merge_query("match (n {synthlabel:'Organization'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:62})<-[:BELONGS]-(m)")
        
        
        
        
        self.neo4j_Connector.merge_query("MATCH (v1:Violation)<-[:BELONGS]-(a)-[:BELONGS]->(v2:Violation) WHERE id(v1)<>id(v2) and not (v1)-[:INTERSECT]-(v2) merge (v1)-[:INTERSECT]-(v2)")
        
        build_grdg =  self.neo4j_Connector.merge_query("CALL gds.graph.project('grdg', 'Violation', {INTERSECT: {orientation: 'UNDIRECTED'}})")
        compute_pr = self.neo4j_Connector.query("CALL gds.pageRank.write('grdg', { writeProperty: 'pageRank' , maxIterations: 20, dampingFactor: 0.85 }) YIELD centralityDistribution, nodePropertiesWritten RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten,centralityDistribution.max AS maximumScore")
         
        first_time= True
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
                                
        random.seed(self.SEED)
        conteggi=[]
        while graphInconsistent: 
            num_viols=self.neo4j_Connector.query("MATCH (v:Violation {solved:False}) RETURN COUNT(v) as count")
            print(num_viols)
            if(first_time):
                initial_count=num_viols[0]['count']
                first_time=False
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
            if(self.iteration_count>2*initial_count):
                timedOut=True 
                break
            else:
                self.iteration_count+=1
                chosen_repairs=[]
                chosen_violations=[]


                for u in self.users:
                    
                    if(self.assignment=="random"):
                        assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation {locked : false}) RETURN v, rand() as r ORDER BY r LIMIT 1")
                    elif self.assignment=="degreeAsc":
                        assigned_hypervertex = self.neo4j_Connector.query("MATCH (v:Violation {locked : false}) RETURN v ORDER BY v.degree LIMIT 1")
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
                        
                        violation_nodes = self.neo4j_Connector.query("MATCH (n)-[:BELONGS]->(v:Violation)<-[:BELONGS]-(m) WHERE ID(v)="+str(violation_id)+" RETURN ID(n), ID(m), labels(n) as labels_n, labels(m) as labels_m")
                        
                        violation_properties = {}
                        for l, v in assigned_hypervertex['v'].items():
                            violation_properties[l] = v 
                        possible_repair=[]
                        
                        best_repair="MATCH (n)-[:BELONGS]->(v:Violation)<-[:BELONGS]-(m) WHERE ID(v)="+str(violation_id)+" set v.solved=True, n.updated=True, m.updated=True, n.synthlabel=labels(n)[0], m.synthlabel=labels(m)[0]"
                        not_allowed=[('Payer','Organization'),('Payer','Provider'),('Payer','Address'),('Payer','Condition'),('Payer','Allergy'),('Payer','CarePlan'),('Payer','Observation'),('Payer','Procedure'),('Payer','Drug'),('CarePlan','Provider'),('CarePlan','Address'),('CarePlan','Drug'),('CarePlan','Observation'),('CarePlan','Procedure'),('CarePlan','Condition'),('CarePlan','Patient'),('CarePlan','Organization'),('Observation','Procedure'),('Observation','Address'),('Observation','Drug'),('Observation','Procedure'),('Observation','Condition'),('Observation','Patient'),('Observation','Organization'),('Procedure','Provider'),('Procedure','Address'),('Procedure','Drug'),('Procedure','Observation'),('Procedure','Condition'),('Procedure','Patient'),('Procedure','Organization'),('Condition','Provider'),('Condition','Address'),('Condition','Drug'),('Condition','Patient'),('Condition','Organization'),('Encounter','Address'),('Encounter','Provider'),('Organization','Patient'),('Provider','Patient'),('Provider','Drug'),('Address','Drugt'),('Patient','Drug'),('Allergy','Address'),('Allergy','Organization'),('Allergy','Provider'),('Allergy','Payer'),('Allergy','CarePlan'),('Allergy','Observation'),('Allergy','Drug'),('Allergy','Procedure'),('Payer','Payer'),('Provider','Drug'),('Address','Address'),('Patient','Patient'),('Allergy','Allergy'),('CarePlan','CarePlan'),('Provider','Provider'),('Procedure','Procedure'),('Observation','Observation'),('Drug','Drug'),('Condition','Condition'),('Organization','Drug')]
                        all_possibilities = [('Patient', 'Patient'), ('Patient', 'Payer'), ('Patient', 'Encounter'), ('Patient', 'Organization'), ('Patient', 'Provider'), ('Patient', 'Drug'), ('Patient', 'Condition'), ('Patient', 'CarePlan'), ('Patient', 'Allergy'), ('Patient', 'Address'), ('Patient', 'Procedure'), ('Patient', 'Observation'),
                                            ('Payer', 'Patient'), ('Payer', 'Payer'), ('Payer', 'Encounter'), ('Payer', 'Organization'), ('Payer', 'Provider'), ('Payer', 'Drug'), ('Payer', 'Condition'), ('Payer', 'CarePlan'), ('Payer', 'Allergy'), ('Payer', 'Address'), ('Payer', 'Procedure'), ('Payer', 'Observation'),
                                            ('Encounter', 'Patient'), ('Encounter', 'Payer'), ('Encounter', 'Encounter'), ('Encounter', 'Organization'), ('Encounter', 'Provider'), ('Encounter', 'Drug'), ('Encounter', 'Condition'), ('Encounter', 'CarePlan'), ('Encounter', 'Allergy'), ('Encounter', 'Address'), ('Encounter', 'Procedure'), ('Encounter', 'Observation'),
                                            ('Organization', 'Patient'), ('Organization', 'Payer'), ('Organization', 'Encounter'), ('Organization', 'Organization'), ('Organization', 'Provider'), ('Organization', 'Drug'), ('Organization', 'Condition'), ('Organization', 'CarePlan'), ('Organization', 'Allergy'), ('Organization', 'Address'), ('Organization', 'Procedure'), ('Organization', 'Observation'),
                                            ('Provider', 'Patient'), ('Provider', 'Payer'), ('Provider', 'Encounter'), ('Provider', 'Organization'), ('Provider', 'Provider'), ('Provider', 'Drug'), ('Provider', 'Condition'), ('Provider', 'CarePlan'), ('Provider', 'Allergy'), ('Provider', 'Address'), ('Provider', 'Procedure'), ('Provider', 'Observation'),
                                            ('Drug', 'Patient'), ('Drug', 'Payer'), ('Drug', 'Encounter'), ('Drug', 'Organization'), ('Drug', 'Provider'), ('Drug', 'Drug'), ('Drug', 'Condition'), ('Drug', 'CarePlan'), ('Drug', 'Allergy'), ('Drug', 'Address'), ('Drug', 'Procedure'), ('Drug', 'Observation'),
                                            ('Condition', 'Patient'), ('Condition', 'Payer'), ('Condition', 'Encounter'), ('Condition', 'Organization'), ('Condition', 'Provider'), ('Condition', 'Drug'), ('Condition', 'Condition'), ('Condition', 'CarePlan'), ('Condition', 'Allergy'), ('Condition', 'Address'), ('Condition', 'Procedure'), ('Condition', 'Observation'),
                                            ('CarePlan', 'Patient'), ('CarePlan', 'Payer'), ('CarePlan', 'Encounter'), ('CarePlan', 'Organization'), ('CarePlan', 'Provider'), ('CarePlan', 'Drug'), ('CarePlan', 'Condition'), ('CarePlan', 'CarePlan'), ('CarePlan', 'Allergy'), ('CarePlan', 'Address'), ('CarePlan', 'Procedure'), ('CarePlan', 'Observation'),
                                            ('Allergy', 'Patient'), ('Allergy', 'Payer'), ('Allergy', 'Encounter'), ('Allergy', 'Organization'), ('Allergy', 'Provider'), ('Allergy', 'Drug'), ('Allergy', 'Condition'), ('Allergy', 'CarePlan'), ('Allergy', 'Allergy'), ('Allergy', 'Address'), ('Allergy', 'Procedure'), ('Allergy', 'Observation'),
                                            ('Address', 'Patient'), ('Address', 'Payer'), ('Address', 'Encounter'), ('Address', 'Organization'), ('Address', 'Provider'), ('Address', 'Drug'), ('Address', 'Condition'), ('Address', 'CarePlan'), ('Address', 'Allergy'), ('Address', 'Address'), ('Address', 'Procedure'), ('Address', 'Observation'),
                                            ('Procedure', 'Patient'), ('Procedure', 'Payer'), ('Procedure', 'Encounter'), ('Procedure', 'Organization'), ('Procedure', 'Provider'), ('Procedure', 'Drug'), ('Procedure', 'Condition'), ('Procedure', 'CarePlan'), ('Procedure', 'Allergy'), ('Procedure', 'Address'), ('Procedure', 'Procedure'), ('Procedure', 'Observation'),
                                            ('Observation', 'Patient'), ('Observation', 'Payer'), ('Observation', 'Encounter'), ('Observation', 'Organization'), ('Observation', 'Provider'), ('Observation', 'Drug'), ('Observation', 'Condition'), ('Observation', 'CarePlan'), ('Observation', 'Allergy'), ('Observation', 'Address'), ('Observation', 'Procedure'), ('Observation', 'Observation')]
                        
                        
                        possibilities=[(p[0],p[1]) for p in all_possibilities]
                        
                        na = not_allowed[violation_properties['type']]
                        
                        if(na[0]==na[1]):
                            possibilities.remove(na)
                        else:
                            possibilities.remove(na)
                            possibilities.remove((na[1],na[0]))    

                        for p in possibilities:
                            possible_repair.append("MATCH (n)-[:BELONGS]->(v:Violation)<-[:BELONGS]-(m)-[r]-(n) WHERE ID(v)="+str(violation_id)+" SET v.solved=True, m.updated=True, n.updated=True, n.synthlabel='"+p[0]+"', m.synthlabel='"+p[1]+"', r.deleted=True")
                            possible_repair.append("MATCH (n)-[:BELONGS]->(v:Violation)<-[:BELONGS]-(m)-[r]-(n) WHERE ID(v)="+str(violation_id)+" SET v.solved=True, m.updated=True, n.updated=True, n.synthlabel='"+p[0]+"', m.synthlabel='"+p[1]+"'")      
                        possible_repair.append("MATCH (n)-[:BELONGS]->(v:Violation)<-[:BELONGS]-(m)-[r]-(n) WHERE ID(v)="+str(violation_id)+" SET v.solved=True, r.deleted=True") 
                        
                        
                        
                        u.set_actions(possible_repair)
                        u.set_best_repair(best_repair)
                        
                        chosen_repair = u.select_action_by_policy(self.answer_distribution,seed)
                        
                        chosen_repairs.append(chosen_repair)
                        chosen_violations.append(assigned_hypervertex)
                    
                print("Chosen repairs: ", len(chosen_repairs))
                
                solved_count = 0 
                t31 = time.time()
                
                for i in range(len(chosen_repairs)):
                    applyRepair(chosen_repairs[i],self.neo4j_Connector)
                    solved_count+=1
                    self.interaction_count+=1
                t32 = time.time()
                print("Time to delete: ", t32-t31)

                #delete all violations
                
                self.neo4j_Connector.merge_query("MATCH (v:Violation) detach delete v")
                #rerun constraints 
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Organization'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:0})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:1})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:2})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Condition'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:3})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Allergy'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:4})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'CarePlan'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:5})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Observation'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:6})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Procedure'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:7})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:8})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:9})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:10})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:11})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Observation'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:12})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Procedure'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:13})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Condition'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:14})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:15})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'Organization'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:16})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Procedure'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:17})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:18})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:19})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Procedure'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:20})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Condition'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:21})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:22})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Organization'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:23})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:24})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:25})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:26})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Observation'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:27})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Condition'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:28})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:29})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Organization'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:30})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Condition'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:31})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Condition'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:32})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Condition'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:33})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Condition'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:34})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Condition'})-[r {deleted:False}]-(m {synthlabel:'Organization'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:35})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Encounter'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:36})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Encounter'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:37})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Organization'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:38})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Provider'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:39})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Provider'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:40})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Address'})-[r {deleted:False}]-(m {synthlabel:'Drugt'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:41})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Patient'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:42})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:43})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Organization'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:44})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:45})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Payer'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:46})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'CarePlan'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:47})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Observation'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:48})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:49})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Procedure'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:50})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Payer'})-[r {deleted:False}]-(m {synthlabel:'Payer'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:51})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Provider'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:52})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Address'})-[r {deleted:False}]-(m {synthlabel:'Address'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:53})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Patient'})-[r {deleted:False}]-(m {synthlabel:'Patient'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:54})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Allergy'})-[r {deleted:False}]-(m {synthlabel:'Allergy'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:55})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'CarePlan'})-[r {deleted:False}]-(m {synthlabel:'CarePlan'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:56})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Provider'})-[r {deleted:False}]-(m {synthlabel:'Provider'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:57})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Procedure'})-[r {deleted:False}]-(m {synthlabel:'Procedure'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:58})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Observation'})-[r {deleted:False}]-(m {synthlabel:'Observation'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:59})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Drug'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:60})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Condition'})-[r {deleted:False}]-(m {synthlabel:'Condition'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:61})<-[:BELONGS]-(m)")
                self.neo4j_Connector.merge_query("match (n {synthlabel:'Organization'})-[r {deleted:False}]-(m {synthlabel:'Drug'}) MERGE (n)-[:BELONGS]->(v1:Violation {solved:false, locked:false, type:62})<-[:BELONGS]-(m)")

                if(len(self.neo4j_Connector.query("MATCH (v:Violation {solved:false}) RETURN v"))==0):
                    graphInconsistent=False
                else:
                    
                    self.neo4j_Connector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
                    self.neo4j_Connector.merge_query("MATCH (v1:Violation)<-[:BELONGS]-(a)-[:BELONGS]->(v2:Violation) WHERE id(v1)<>id(v2) and not (v1)-[:INTERSECT]-(v2) merge (v1)-[:INTERSECT]-(v2)")
                
                    
                    t0 = time.time()
                    build_grdg =  self.neo4j_Connector.merge_query("CALL gds.graph.project('grdg', 'Violation', {INTERSECT: {orientation: 'UNDIRECTED'}})")
                    compute_pr = self.neo4j_Connector.query("CALL gds.pageRank.write('grdg', { writeProperty: 'pageRank' , maxIterations: 20, dampingFactor: 0.85 }) YIELD centralityDistribution, nodePropertiesWritten RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten,centralityDistribution.max AS maximumScore")
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

        # print("True positives: ", true_positives)
        # print("False positives: ", false_positives)
        # print("False negatives: ", false_negatives)
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            
        # print("Precision: ", precision)
        # print("Recall: ", recall)
        # print("F1: ", f1_score)
        
        
        # print("interaction count: ", self.interaction_count)
        # print("iteration count: ", self.iteration_count)
        # print("wait count: ", self.wait_count)
        self.avg_interaction_count+=self.interaction_count
        self.avg_wait_count+=self.wait_count
        self.avg_iteration_count+=self.iteration_count

        time2 = time.time()
        if(timedOut):
            return -1,-1,-1
        else:
            return f1_score, self.iteration_count, self.interaction_count
         
    def generateUsers(self,max_users):
        users = []
        for i in range(max_users):
            users.append(User("tutti"))
        return users


# Example Usage
if __name__ == "__main__":
    dataset = 'synthea'
    violations = '1000'
    for answer in [1,0.75,0.5,0.25,0]:
        env = CGREnvironment(dataset=dataset, violations=int(violations), answer=answer)
        #try:
        f1s = []
        iterationss = []
        interactionss = []
        for i in range(10):
            print("Starting simulation:", i)
            f1,iterations,interactions=env.start_fixed_arrival_simulation(seed=i)
            if(f1>=0):
                f1s.append(f1)
                iterationss.append(iterations)
                interactionss.append(interactions)
        print("----")
        print(answer)
        print("----")
        if(len(f1s)>0):
            print("F1: ", np.mean(f1s))
            print("Iterations: ", np.mean(iterationss))
            print("Interactions: ", np.mean(interactionss))
    
