import time
def checkConstraints(constraints,neo4j_Connector):
    edges = []
    for idx,constraint in enumerate(constraints):
        
        query = constraint['create_constraint']
        try:
            results = neo4j_Connector.merge_query(query)
        except Exception as e:
            print("DIOBOIA Error executing query: ", query)
            print(e)
            continue
    try:
        violations = neo4j_Connector.query("MATCH (v1:Violation) return v1")
        results = neo4j_Connector.query("MATCH (v1:Violation)<-[:BELONGS]-(a)-[:BELONGS]->(v2:Violation) WHERE not (v1)-[:INTERSECT]-(v2) merge (v1)-[:INTERSECT]-(v2) return v1,v2")
        for res in results:
            edges.append(res)
        results = neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.id)")
        results = neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.solved)")
    except Exception as e:
        print("DIOCANE Error executing query: ", query)
        print(e)
        
    return violations, edges