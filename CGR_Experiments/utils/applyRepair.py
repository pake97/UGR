def applyRepair(selected_repair,neo4j_connector):
    #print("applico : ",selected_repair)
    neo4j_connector.query(selected_repair)