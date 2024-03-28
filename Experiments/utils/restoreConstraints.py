import time
def restoreConstraints(neo4j_Connector,n_violations):
    violations = []
    
    results = neo4j_Connector.merge_query("MATCH (a:Violation) SET a.solved=False")    
    for id in n_violations:
        results = neo4j_Connector.merge_query("MATCH (a:Violation) WHERE ID(a)="+str(id)+" detach delete a")
    # try:
    #     results = neo4j_Connector.query("MATCH (v1:Violation)<-[:BELONGS]-(a)-[:BELONGS]->(v2:Violation) RETURN v1,v2")
    #     for res in results:
    #         violations.append(res)
    #     results = neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.id)")
    #     results = neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.solved)")
    # except Exception as e:
    #     print("DIOCANE Error executing query: ", query)
    #     print(e)
        
    # return violations, violation_dict
    return True