def compute_metrics(solved_violations,neo4j_Connector):

    touched_nodes = []
    touched_edges=[]

    for violation in solved_violations:
        properties = {}
        for l, v in violation['v'].items():
            properties[l] = v 
        nodes = properties['nodes'].split(",")
        labels = properties['labels'].split(",")
        for i in range(len(nodes)):
            if(labels[i]=='r' or labels[i]=='p' or labels[i]=='q'):
                
                touched_edges.append(neo4j_Connector.query("MATCH ()-[r]-() WHERE ID(r)="+str(nodes[i])+" RETURN r"))
            else:
                
                touched_nodes.append(neo4j_Connector.query("MATCH (n) WHERE ID(n)="+str(nodes[i])+" RETURN n"))

    true_positives_nodes = 0
    false_positives_nodes = 0
    false_negatives_nodes = 0
    true_negatives_nodes = 0
    true_positives_edges = 0
    false_positives_edges = 0
    false_negatives_edges = 0
    true_negatives_edges = 0

    for node in touched_nodes:
        properties = {}
        for l, v in node[0]['n'].items():
            properties[l] = v 
        labelz = node[0]['n'].labels
        label, = labelz
        if(label=='Starship'):
            if(not properties['realHeight']==properties['height'] and not properties['updated']):
                false_negatives_nodes+=1   
            if(not properties['realHeight']==properties['height'] and properties['updated']):
                false_positives_nodes+=1
            if(properties['realHeight']==properties['height'] and properties['updated']):
                true_positives_nodes+=1
            if(not properties['realHeight']==properties['height'] and not properties['updated']):
                true_negatives_nodes+=1
        if(label=='Species'):
            if(not properties['real_average_height']==properties['average_height'] and not properties['updated']):
                false_negatives_nodes+=1   
            if(not properties['real_average_height']==properties['average_height'] and properties['updated']):
                false_positives_nodes+=1
            if(properties['real_average_height']==properties['average_height'] and properties['updated']):
                true_positives_nodes+=1
            if(not properties['real_average_height']==properties['average_height'] and not properties['updated']):
                true_negatives_nodes+=1
    for edge in touched_edges:
        properties = {}
        for l, v in edge[0]['r'].items():
            properties[l] = v 
        label = edge[0]['r'].type
        if(properties['toDelete']==True):            
            if(properties['deleted']==True):
                true_positives_edges+=1
            else:
                false_negatives_edges+=1
        else:
            if(properties['deleted']==False):
                true_negatives_edges+=1
            else:
                false_positives_edges+=1


    true_positives = true_positives_nodes + true_positives_edges
    false_positives = false_positives_nodes + false_positives_edges
    false_negatives = false_negatives_nodes + false_negatives_edges

    print("True positives: ", true_positives)
    print("False positives: ", false_positives)
    print("False negatives: ", false_negatives)
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1_score
