def compute_metrics(nodes,edges, repaired_nodes, repaired_edges):


    true_positives_nodes = sum(tp_nodes(a,p) for a, p in zip(nodes, repaired_nodes))
    false_positives_nodes = sum(fp_nodes(a,p) for a, p in zip(nodes, repaired_nodes))
    false_negatives_nodes = sum(fn_nodes(a,p) for a, p in zip(nodes, repaired_nodes))
    true_positives_edges = sum(tp_edges(a,p) for a, p in zip(edges, repaired_edges))
    false_positives_edges = sum(fp_edges(a,p) for a, p in zip(edges, repaired_edges))
    false_negatives_edges = sum(fn_edges(a,p) for a, p in zip(edges, repaired_edges))

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

def tp_nodes(n1,n2):
    p1={}
    p2={}
    for k,l in n1['n'].items():
        if(k=='synth1'or k=='synth2'or k=='synth3'):
            p1[k]=l
    for k,l in n2['n'].items():
        if(k=='synth1'or k=='synth2'or k=='synth3'):
            p2[k]=l
    
    return p1['synth1']==p2['synth1'] and p1['synth2']==p2['synth2'] and p1['synth3']==p2['synth3']
    
def fp_nodes(n1,n2):
    p1={}
    p2={}
    for k,l in n1['n'].items():
        if(k=='synth1'or k=='synth2'or k=='synth3'):
            p1[k]=l
    for k,l in n2['n'].items():
        if(k=='synth1'or k=='synth2'or k=='synth3'):
            p2[k]=l

    return p2['synth1']!=1 or p2['synth2']!=1 or p2['synth3']!=1

def fn_nodes(n1,n2):
    p1={}
    p2={}
    for k,l in n1['n'].items():
        if(k=='synth1'or k=='synth2'or k=='synth3'):
            p1[k]=l
    for k,l in n2['n'].items():
        if(k=='synth1'or k=='synth2'or k=='synth3'):
            p2[k]=l

    return p1['synth1']!=p2['synth1'] or p1['synth2']!=p2['synth2'] or p1['synth3']!=p2['synth3']


def tp_edges(e1,e2):
    p1={}
    p2={}
    for k,l in e1['r'].items():
        if(k=='deleted'):
            p1[k]=l
    for k,l in e2['r'].items():
        if(k=='deleted'):
            p2[k]=l
    if(e1['r'].type=='SYNTH'):
        return p2['deleted']=='true'
    else:
        return p2['deleted']=='false'
    
def fp_edges(e1,e2):
    p1={}
    p2={}
    for k,l in e1['r'].items():
        if(k=='deleted'):
            p1[k]=l
    for k,l in e2['r'].items():
        if(k=='deleted'):
            p2[k]=l
    if(e1['r'].type=='SYNTH'):
        return False
    else:
        return p2['deleted']=='true'

def fn_edges(e1,e2):
    p1={}
    p2={}
    for k,l in e1['r'].items():
        if(k=='deleted'):
            p1[k]=l
    for k,l in e2['r'].items():
        if(k=='deleted'):
            p2[k]=l
    if(e1['r'].type=='SYNTH'):
        return p2['deleted']=='false'
    else:
        return False