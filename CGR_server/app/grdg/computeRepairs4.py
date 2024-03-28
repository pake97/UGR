def computeRepairs(assigned_hypervertex, constraints):
    
    violation_id = assigned_hypervertex['v'].element_id.split(":")[-1]
    properties = {}
    for l, v in assigned_hypervertex['v'].items():
        properties[l] = v 
    nodes_ids =properties['nodes'].split(",")
    
    node_labels =properties['labels'].split(",")
    
    violation_type =properties['type']
    
    
    possible_repairs=[]
    best_repair=""

    repair_config =constraints[violation_type]


    for possible_repair in repair_config['possible_repairs']:
        formatted_repair=""
        repair = possible_repair['repair'].split("UNION")
        for rep in repair:
            if('ID(a)' in rep):
                index = node_labels.index('a')
                formatted_repair+=rep.replace('FILTRI',nodes_ids[index])+" UNION "
            if('ID(b)' in rep):
                index = node_labels.index('b')
                formatted_repair+=rep.replace('FILTRI',nodes_ids[index])+" UNION "
            if('ID(c)' in rep):
                index = node_labels.index('c')
                formatted_repair+=rep.replace('FILTRI',nodes_ids[index])+" UNION "
            if('ID(d)' in rep):
                index = node_labels.index('d')
                formatted_repair+=rep.replace('FILTRI',nodes_ids[index])+" UNION "
            if('ID(p)' in rep):
                index = node_labels.index('p')
                formatted_repair+=rep.replace('FILTRI',nodes_ids[index])+" UNION "
            if('ID(r)' in rep):
                index = node_labels.index('r')
                formatted_repair+=rep.replace('FILTRI',nodes_ids[index])+" UNION "
            if('ID(q)' in rep):
                index = node_labels.index('q')
                formatted_repair+=rep.replace('FILTRI',nodes_ids[index])+" UNION "
        possible_repairs.append([formatted_repair + "MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True",possible_repair['explanation']])
    
    
   
    return_object = {
        'possible_repairs':possible_repairs,
        'violation_type':violation_type,
        'node_labels':node_labels,
        'nodes_ids':nodes_ids,
        'violation_id':violation_id,
    }
    return return_object
