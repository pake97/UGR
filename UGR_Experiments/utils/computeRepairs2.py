import re
from itertools import combinations
import random
import math
import numpy as np
def computeRepairs(assigned_hypervertex,nodes_dict, user_type, constraints,SEED):
    random.seed(SEED)
    possible_repairs=[]
    policy = []

    repairs =constraints[assigned_hypervertex]
    
    nodes_filter=""
    for node in list(nodes_dict.keys()):
        if(nodes_filter==""):
            nodes_filter+= node+"="+str(nodes_dict[node])+" " 
        else: 
            nodes_filter+= "AND "+node+"="+str(nodes_dict[node])+" "
    
  
    for possible_repair in repairs['possible_repairs']:
        formatted_repair = possible_repair.replace("FILTRI",nodes_filter) 
        possible_repairs.append(formatted_repair)
        policy.append(1/len(repairs['possible_repairs']))
    
    best_repair = repairs['best_repair'].replace("FILTRI",nodes_filter)
    return possible_repairs, best_repair



def softmax(x):
    exp_x = np.exp(x - np.max(x))  # subtracting np.max(x) for numerical stability
    return exp_x / exp_x.sum(axis=0, keepdims=True)