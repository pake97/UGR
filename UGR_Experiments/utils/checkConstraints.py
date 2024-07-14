def checkConstraints(constraints,neo4j_Connector,violation_dict):
    violations = []
    for idx,constraint in enumerate(constraints):
        violation_dict[str(idx)]=[]
        query = constraint['constraint']
        try:
            distinct_results = []
            results_as_dict = neo4j_Connector.query(query)
            for res in results_as_dict:
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
                            violations.append({'query':query,'graph':res})
                            violation_dict[str(idx)].append(nodes)
        except Exception as e:
            print("Error executing query: ", query)
            print(e)
            continue
        
    return violations