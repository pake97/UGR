import time
def restoreConstraints(neo4j_Connector,n_violations):
    violations = []
    results = neo4j_Connector.merge_query("MATCH (v:SolvedViolation {solved:true}) WITH collect(v) AS violations CALL apoc.refactor.rename.label('SolvedViolation', 'Violation', violations) YIELD committedOperations RETURN committedOperations")    
    results = neo4j_Connector.merge_query("MATCH (a:Violation) SET a.solved=False")    
    for id in n_violations:
        results = neo4j_Connector.merge_query("MATCH (a:Violation) WHERE ID(a)="+str(id)+" detach delete a")
    try:        
        t0 = time.time()
        if(neo4j_Connector.query("RETURN gds.graph.exists('grdg')")[0]["gds.graph.exists('grdg')"]):
            neo4j_Connector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
        results = neo4j_Connector.merge_query("MATCH (v1:Violation)<-[:BELONGS]-(a)-[:BELONGS]->(v2:Violation) WHERE id(v1)<>id(v2) and not (v1)-[:INTERSECT]-(v2) merge (v1)-[:INTERSECT]-(v2)")
        build_grdg =  neo4j_Connector.merge_query("CALL gds.graph.project('grdg', 'Violation', {INTERSECT: {orientation: 'UNDIRECTED'}})")
        t1 = time.time()
        print("Time to build grdg: ", t1-t0)
        t2 = time.time()
        compute_btw = neo4j_Connector.query("CALL gds.pageRank.write('grdg', { writeProperty: 'pageRank' , maxIterations: 20, dampingFactor: 0.85 }) YIELD centralityDistribution, nodePropertiesWritten RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten,centralityDistribution.max AS maximumScore")
        t3 = time.time()
        print("Time to compute pr: ", t3-t2)
    # try:
    #     results = neo4j_Connector.query("MATCH (v1:Violation)<-[:BELONGS]-(a)-[:BELONGS]->(v2:Violation) RETURN v1,v2")
    #     for res in results:
    #         violations.append(res)
    #     results = neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.id)")
    #     results = neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.solved)")
    except Exception as e:
        print("Error restoring graph")
        print(e)
        
    # return violations, violation_dict
    return True