from neomodel import db, config
config.DATABASE_URL = "YOUR URL"



def checkSafety(selected_repair,violation_dict,neo4j_Connector,constraints):

    new_violation_dict = {}
    safety = True
    db.begin()
    
    neo4j_Connector.query(selected_repair)
    
    for idx,constraint in enumerate(constraints):
        query = constraint['constraint']
        try:
            distinct_results = []
            index = 0
            while True:
                results, meta = neo4j_Connector.query_id(query+ " SKIP "+str(index*100)+" LIMIT 100")
                for res in results:
                    nodes = set(res)
                    if nodes in distinct_results:
                        continue
                    else:
                        distinct_results.append(nodes)
                if(len(results)<100):
                    break
                index+=1

            new_violation_dict[str(idx)]=distinct_results

        except Exception as e:
            print("Error executing query: ", query)
            print(e)
            continue

    isSafe=True
    for idx in list(violation_dict.keys()):
        if(not isSafe):
            break
        if(len(new_violation_dict[idx])>len(violation_dict[idx])):
            #print("primo errore", len(new_violation_dict[idx]), len(violation_dict[idx]))
            isSafe=False
            break
        else:
            for nv in new_violation_dict[idx]:
                if nv not in violation_dict[idx]:
                    #print("secondo errore")
                    isSafe=False
                    break         
    db.rollback()
    return safety
    