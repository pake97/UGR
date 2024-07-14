import math
import random 
import time
def injectInconsistencies(neo4j_Connector,constraints,error_distribution,SEED):
    random.seed(SEED)
    #num = [24,12,51,12]
    for idx,constraint in enumerate(constraints):
        #print(constraint)
        t0 = time.time()
        pattern = constraint['pattern']
        inject_errors = constraint['inject_errors']
        try:
            results_as_dict = neo4j_Connector.query(pattern)
            #results_as_dict = neo4j_Connector.query(pattern + " LIMIT "+str(num[idx]))
            #to_inject = results_as_dict
            num_inconsitencies = len(results_as_dict)
            to_inject = random.choices(results_as_dict,k=math.floor(num_inconsitencies*error_distribution[idx]))
            #print(len(to_inject))
            distinct_results = []
            for res in to_inject:
                nodes = []
                for k in list(res.keys()):
                    if(str(type(res[k]))=="<class 'neo4j.graph.Node'>"):
                        nodes.append(res[k].element_id.split(":")[2]) 
                    else:
                        continue
                nodes = set(nodes)
                if nodes in distinct_results:
                    continue
                else:
                    distinct_results.append(nodes)
                    nodes_dict = {}
                    for k in list(res.keys()):
                        if(str(type(res[k]))=="<class 'neo4j.graph.Node'>"):
                            if k not in nodes_dict:
                                nodes_dict[k]=res[k].element_id.split(":")[2]
                        else:
                            continue
                    nodes_filter=""
                    for node in list(nodes_dict.keys()):
                        if(nodes_filter==""):
                            nodes_filter+= "id("+node+")="+str(nodes_dict[node])+" " 
                        else: 
                            nodes_filter+= "AND id("+node+")="+str(nodes_dict[node])+" "
                    #print(inject_errors.format(nodes_filter))
                    result = neo4j_Connector.query(inject_errors.replace("FILTRI",nodes_filter))
            t1 = time.time()
            #print("Injected inconsistencies in ",t1-t0," seconds")
        except Exception as e:
            print("INJECT Error executing query: ", pattern)
            print(e)
            continue
    return True