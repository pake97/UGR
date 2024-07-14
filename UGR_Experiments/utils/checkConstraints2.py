import time
def checkConstraints(constraints,neo4j_Connector,violation_dict):
    violations = []
    for idx,constraint in enumerate(constraints):
        violation_dict[str(idx)]=[]
        query = constraint['constraint']
        try:
            distinct_results = []
            final_results = []
            index = 0
            while True:
                t0 = time.time()
                results, meta = neo4j_Connector.query_id(query+ " SKIP "+str(index*100)+" LIMIT 100")
                t1=time.time()
                #print("Query time: ",t1-t0)
                for res in results:
                    nodes = set(res)
                    if nodes in distinct_results:
                        continue
                    else:
                        distinct_results.append(nodes)
                        res_dict = {}
                        for i in range(len(meta)):
                            res_dict[meta[i]]=res[i]
                        violations.append({'query':idx,'graph':res_dict})
                        violation_dict[str(idx)].append(res)
                if(len(results)<100):
                    break
                index+=1
            
        except Exception as e:
            print("Error executing query: ", query)
            print(e)
            continue
        
    return violations, violation_dict