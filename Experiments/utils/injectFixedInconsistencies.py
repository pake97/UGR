import math
import random 
import time
def injectFixedInconsistencies(neo4j_Connector,error_distribution,SEED):  
    random.seed(SEED)
    try:
        nodes,meta = neo4j_Connector.query_id("MATCH (n) RETURN ID(n)")

        to_inject = random.choices(nodes,k=math.floor(len(nodes)*error_distribution[0]))
        
        for res in to_inject:
            result = neo4j_Connector.query("MATCH (n) WHERE ID(n)="+str(res[0])+" SET n.synth1 = 0")

        edges,meta = neo4j_Connector.query_id("MATCH ()-[r]->() RETURN ID(r)")
        to_inject = random.choices(edges,k=math.floor(len(edges)*error_distribution[1]))
       
        for res in to_inject:
            result = neo4j_Connector.query("MATCH (a)-[r]->(b) WHERE ID(r)="+str(res[0])+" CREATE (a)-[:SYNTH {deleted:false}]->(b)")
    except Exception as e:
        print("Error executing query: ")
        print(e)
    return True