import math
import random 
import time
def restore_graph(neo4j_Connector,to_inject,SEED,constraints):
    random.seed(SEED)
    partialSum = 0
    for idx,constraint in enumerate(constraints):
        inject_errors = constraint['inject_errors']
        try:
            meta = to_inject[idx]['meta']
            for res in to_inject[idx]['ids']:
                result = neo4j_Connector.query(inject_errors.replace("FILTRI",meta+"="+str(res)))
            #print("Injected inconsistencies in ",t3-t2," seconds")
        except Exception as e:
            print("Error executing query: ")
            print(e)
            continue
    #print(partialSum)
    return True