import re
from itertools import combinations
import random
import math
import numpy as np
def computeRepairs(assigned_hypervertex,nodes_dict, user_type, constraints,SEED):
    random.seed(SEED)
    possible_repairs=[]
    policy = []

    repairs ={}
    for constraint in constraints:
        if constraint['constraint'] == assigned_hypervertex:
            repairs = constraint

    nodes_filter=""
    for node in list(nodes_dict.keys()):
        if(nodes_filter==""):
            nodes_filter+= "id("+node+")="+str(nodes_dict[node])+" " 
        else: 
            nodes_filter+= "AND id("+node+")="+str(nodes_dict[node])+" "

    if user_type == 'Oracle':
        try:
            formatted_repair = repairs['best_repair'].replace("FILTRI",nodes_filter)
            possible_repairs.append(formatted_repair)
            policy.append(1)
        except:
            print("ERRORE")
            print(repairs['best_repair'])

    elif user_type == 'Expert':
        pr = repairs['possible_repairs']
        pr = [r.replace("FILTRI",nodes_filter) for r in pr]
        best_repair =pr.pop(0)        
        random.shuffle(pr)
        pr.insert(0,best_repair)

        pr=pr[::-1]
        for i in range(int((len(pr)-1)/2)): 
            policy.append(math.exp(2*i*0.1))
            policy.append(math.exp((2*i+1)*0.1))       
        while(len(policy)<len(pr)):
            policy.append(1)

        possible_repairs = pr
        policy = np.array(policy)
        
        policy = softmax(policy)
        
        policy = policy.tolist()
        
    else:
        for possible_repair in repairs['possible_repairs']:
            formatted_repair = possible_repair.replace("FILTRI",nodes_filter) 
            possible_repairs.append(formatted_repair)
            policy.append(1/len(repairs['possible_repairs']))
    

    return possible_repairs, policy

    # possible_repairs=[]
    # possible_deletion = []
    # edges_regEx1= r'\([A-Za-z]:[A-Za-z]+\)<-\[[A-Za-z]:[A-Za-z]+\]-\([A-Za-z]:[A-Za-z]+\)'
    # edges_regEx2= r'\([A-Za-z]:[A-Za-z]+\)-\[[A-Za-z]:[A-Za-z]+\]->\([A-Za-z]:[A-Za-z]+\)'
    # nodes_regEx = r'\([A-Za-z]:[A-Za-z]+\)'
    # edges = re.findall(edges_regEx1, assigned_hypervertex)+re.findall(edges_regEx2, assigned_hypervertex)
    
    # nodes_filter=""
    # for node in list(ids.keys()):
    #     nodes_filter+= "AND id("+node+")="+str(ids[node])+" " 
    # for edge in edges:
    #     splitted = assigned_hypervertex.split("RETURN")[0]
    #     variable = edge.split("[")[1].split(":")[0]
    #     repair_query =splitted +nodes_filter + " DELETE "+ variable
    #     possible_deletion.append(repair_query)

    # filters = assigned_hypervertex.split("WHERE")[1].split("RETURN")[0].split("AND")
    # filters = [f.strip() for f in filters]

    # possible_updates={}
    
    # for f in filters:
        
    #     splitted = assigned_hypervertex.split("RETURN")[0]
    #     theta_regEx = r'[<>!=]+'
    #     theta = re.findall(theta_regEx, f)[0]
    #     node1 = f.split(theta)[0].split(".")[0]
        
    #     property1 = f.split(theta)[0].split(".")[1]
        
    #     node2 = f.split(theta)[1].split(".")[0]
        
    #     property2 = f.split(theta)[1].split(".")[1]
        
    #     possible_updates[f.split(theta)[0]]=[]
    #     for vals in property_values[property1]:
    #         repair_query = splitted +nodes_filter + " SET "+ node1+"."+property1+"="+str(vals)
    #         possible_updates[ f.split(theta)[0]].append(repair_query)
    #     possible_updates[f.split(theta)[1]]=[]
    #     for vals in property_values[property2]:
    #         repair_query = splitted +nodes_filter + " SET "+ node2+"."+property2+"="+str(vals)
    #         possible_updates[f.split(theta)[1]].append(repair_query)

    # delete_combs=[]

    # for counter in range(len(edges)):
    #     for comb in list(combinations(possible_deletion, counter+1)):
    #         delete_combs.append(comb)
        
    # update_combs=[]
    # for counter in range(len(filters)):
    #     for comb in list(combinations(list(possible_updates.keys()), counter+1)):
    #         #(k1) (k2) (k3)(k1,k2)(k2,k3) (k1,k3)(k1,k2,k3) 
    #         #TODO io ho delle combinazioni di chiavi e devo sostituire i valori di quelle chiavi (tutte le combinazioni possibili)
    #         possibilities = []

    # #TODO SCrivi a mano tutte le query nel file delle query. con il repair ottimo

    # for pu in possible_updates:
    #     for p in possible_updates[pu]:
    #         possible_repairs.append([p])
    
    




def softmax(x):
    exp_x = np.exp(x - np.max(x))  # subtracting np.max(x) for numerical stability
    return exp_x / exp_x.sum(axis=0, keepdims=True)