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
        results = neo4j_Connector.query("MATCH (v1:Violation) RETURN v1")
        for res in results:
            violations.append(res)
        results = neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.id)")
        results = neo4j_Connector.merge_query("CREATE INDEX FOR (n:Violation) ON (n.solved)")
    except Exception as e:
        print("DIOCANE Error executing query: ", query)
        print(e)
        
    return violations