def checkSafety(selected_repair,neo4j_Connector,constraints):

    safe = True
    neo4j_Connector.db.begin()
    

    num_violation_pre = neo4j_Connector.query("MATCH (v:Violation {solved:false}) RETURN COUNT(v) as count")

    neo4j_Connector.query(selected_repair)
    for idx,constraint in enumerate(constraints):
        query = constraint['create_constraint']
        try:
            results= neo4j_Connector.merge_query(query)
        except Exception as e:
            print("Error executing query: ", query)
            print(e)
            continue
        
    num_violation_post = neo4j_Connector.query("MATCH (v:Violation {solved:false}) RETURN COUNT(v) as count")
    if(num_violation_post[0]['count']>num_violation_pre[0]['count']):
        safe=False
                
    neo4j_Connector.db.rollback()
    return safe
    