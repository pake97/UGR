import re
from itertools import combinations
import random
import math
import json
import numpy as np
def computeRepairs(assigned_hypervertex, properties, query):
    
    
    violation_id = assigned_hypervertex.element_id.split(":")[-1]
    
    nodes_ids = properties['nodes'].split(",")
    
    node_labels = properties['labels'].split(",")
    type = properties['type']

    formatted_repair=""
    repair = query.split("UNION")
    if type == 2:
        for rep in repair:
            if('ID(a)' in rep or 'ID(b)' in rep or 'ID(c)' in rep):
                indexa = node_labels.index('a')
                indexb = node_labels.index('b')
                indexc = node_labels.index('c')
                formatted_repair+=rep.replace('FILTRIA',nodes_ids[indexa]).replace('FILTRIB',nodes_ids[indexb]).replace('FILTRIC',nodes_ids[indexc])+" UNION "
            if('ID(p)' in rep):
                index = node_labels.index('p')
                formatted_repair+=rep.replace('FILTRI',nodes_ids[index])+" UNION "
            if('ID(r)' in rep):
                index = node_labels.index('r')
                formatted_repair+=rep.replace('FILTRI',nodes_ids[index])+" UNION "
            if('ID(q)' in rep):
                index = node_labels.index('q')
                formatted_repair+=rep.replace('FILTRI',nodes_ids[index])+" UNION "
       
    else:
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
    formatted_repair= formatted_repair + "MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
    
    return formatted_repair
