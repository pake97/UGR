import time
def checkConstraints(constraints,neo4j_Connector):
    violations = []
    for idx,constraint in enumerate(constraints):
        
        query = constraint['create_constraint']
        try:
            results = neo4j_Connector.merge_query(query)
        except Exception as e:
            print("DIOBOIA Error executing query: ", query)
            print(e)
            continue
    try:        
        t0 = time.time()
        results = neo4j_Connector.merge_query("MATCH (v1:Violation)<-[:BELONGS]-(a)-[:BELONGS]->(v2:Violation) WHERE id(v1)<>id(v2) and not (v1)-[:INTERSECT]-(v2) merge (v1)-[:INTERSECT]-(v2)")
        build_grdg =  neo4j_Connector.merge_query("CALL gds.graph.project('grdg', 'Violation', {INTERSECT: {orientation: 'UNDIRECTED'}})")
        t1 = time.time()
        print("Time to build grdg: ", t1-t0)
        t2 = time.time()
        compute_btw = neo4j_Connector.query("CALL gds.pageRank.write('grdg', { writeProperty: 'pageRank' , maxIterations: 20, dampingFactor: 0.85 }) YIELD centralityDistribution, nodePropertiesWritten RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten,centralityDistribution.max AS maximumScore")
        t3 = time.time()
        print("Time to compute pr: ", t3-t2)
        results = neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.id)")
        results = neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.solved)")
        violations = neo4j_Connector.query("MATCH (v:Violation) return ID(v) as id")
    except Exception as e:
        print("Error Inject inconsistencies: ", query)
        print(e)

    return violations
        
