def checkSafety(selected_repair,selected_violation,neo4j_Connector,constraints):

    safe = True
    neo4j_Connector.db.begin()
    
    neo4j_Connector.query(selected_repair)
    properties = {}
    for l, v in selected_violation['v'].items():
        properties[l] = v 
    nodi =properties['nodes'].split(",")                        
    labels =properties['labels'].split(",")  
    for constraint in constraints:
        allowed_nodes = constraint['ids']
        viols =[]
        
        
        
        
        for j in range(len(nodi)):
            if('ID('+labels[j]+')' in allowed_nodes):
                filters="ID("+labels[j]+")="+nodi[j]
                vios=neo4j_Connector.query(constraint['new_constraint'].replace("FILTRI",filters))   
                viols.extend(vios)                            
    for viol in viols:
        filters =""                                    
        for nodes in viol.keys():
            if(filters==""):
                filters+=nodes + "="+str(viol[nodes])
            else:
                filters+=" AND "+nodes + "="+str(viol[nodes])
        # query = self.constraints[violation_type]['constraint']
        # if(self.neo4j_Connector.query(query.replace("RETURN", filters + " RETURN"))==[]):
        if(len(neo4j_Connector.query(constraint['check_new_violation'].replace("FILTRI",filters)))==0):
            
            safe=False
            break
        

    neo4j_Connector.db.rollback()
    return safe
    