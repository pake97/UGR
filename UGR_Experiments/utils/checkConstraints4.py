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
        t4 = time.time()
        compute_btw = neo4j_Connector.query("CALL gds.degree.write('grdg', { writeProperty: 'degree' }) YIELD centralityDistribution, nodePropertiesWritten RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten")
        t5 = time.time()
        print("Time to compute degree: ", t5-t4)
        print(neo4j_Connector.query("CALL gds.degree.stats('grdg') YIELD centralityDistribution RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, centralityDistribution.max AS maximumScore"))
        num_v = neo4j_Connector.query("MATCH (v:Violation) RETURN COUNT(v) as count")
        num_e = neo4j_Connector.query("MATCH (v1:Violation)-[p:INTERSECT]-(v2:Violation) RETURN COUNT(p) as count")
        print("Density of grdg: ", num_e[0]['count']/(num_v[0]['count']*(num_v[0]['count']-1)))
        results = neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.id)")
        results = neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.solved)")
        violations = neo4j_Connector.query("MATCH (v:Violation) return ID(v) as id")
    except Exception as e:
        print("Error Inject inconsistencies: ", query)
        print(e)

    return violations
        
