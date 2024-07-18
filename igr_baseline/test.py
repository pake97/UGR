import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from igr import *



dataset = "sw"


def getConstraintGraph(dataset):
    S=nx.Graph()
    if(dataset=="sw"):
        S.add_node('Species')
        S.add_node('Planet')
        S.add_node('Character')
        S.add_node('Film')
        S.add_node('Vehicle')
        S.add_node('Starship')
        
        S.add_edge('Species', 'Planet')
        S.add_edge('Species', 'Character')
        S.add_edge('Species', 'Film')
        S.add_edge('Film', 'Planet')
        S.add_edge('Character', 'Planet')
        S.add_edge('Character', 'Film')
        S.add_edge('Character', 'Vehicle')
        S.add_edge('Character', 'Starship')
        S.add_edge('Film', 'Vehicle')
        S.add_edge('Film', 'Starship')
        
    if(dataset=="fincen"):
        S.add_node('Filing')
        S.add_node('Entity')
        S.add_node('Country')
        
        
        S.add_edge('Entity', 'Entity')
        S.add_edge('Entity', 'Country')
        S.add_edge('Entity', 'Filing')
        
    
    if(dataset=="wwc19"):
        S.add_node('Person')
        S.add_node('Squad')
        S.add_node('Team')
        S.add_node('Match')
        S.add_node('Tournament')
        
        
        S.add_edge('Team', 'Person')
        S.add_edge('Team', 'Squad')
        S.add_edge('Team', 'Match')
        S.add_edge('Team', 'Tournament')
        S.add_edge('Squad', 'Person')
        S.add_edge('Tournament', 'Squad')
        S.add_edge('Person', 'Match')
        S.add_edge('Match', 'Tournament')
        
    if(dataset=="stackoverflow"):
        S.add_node('User')
        S.add_node('Comment')
        S.add_node('Answer')
        S.add_node('Question')
        S.add_node('Tag')
        
        
        S.add_edge('Question', 'User')
        S.add_edge('Question', 'Comment')
        S.add_edge('Question', 'Match')
        S.add_edge('Question', 'Tag')
        S.add_edge('User', 'Comment')
        S.add_edge('User', 'Answer')
    
    
    if(dataset=="synthea"):
        S.add_node('Provider')
        S.add_node('Organization')
        S.add_node('Payer')
        S.add_node('Patient')
        S.add_node('Encounter')
        S.add_node('CarePlan')
        S.add_node('Observation')
        S.add_node('Procedure')
        S.add_node('Condition')
        S.add_node('Drug')
        S.add_node('Allergy')
        S.add_node('Address')
        
        
        S.add_edge('Encounter', 'Payer')
        S.add_edge('Encounter', 'Patient')
        S.add_edge('Encounter', 'CarePlan')
        S.add_edge('Encounter', 'Encounter')
        S.add_edge('Encounter', 'Observation')
        S.add_edge('Encounter', 'Procedure')
        S.add_edge('Encounter', 'Drug')
        S.add_edge('Encounter', 'Allergy')
        S.add_edge('Encounter', 'Tag')
        S.add_edge('Encounter', 'Organization')
        S.add_edge('Organization', 'Address')
        S.add_edge('Organization', 'Provider')
        S.add_edge('Provider', 'Address')
        S.add_edge('Patient', 'Payer')
        S.add_edge('Patient', 'Address')

    return S



    
G = nx.Graph()
G_opt = nx.Graph()
df = pd.read_csv("data/"+dataset+"_neighborhood.csv")
df.fillna("", inplace=True)
list_nodes = df.to_numpy().tolist()



indexes ={}
for index, row in df.iterrows():
    if(row['_id']!=""):
        
        G_opt.add_node(index)
        G_opt.nodes[index]['label'] = row['_labels']
        G_opt.nodes[index]['id'] = row['_id']
        G.add_node(index)
        G.nodes[index]['label'] = row["synthlabel"]
        G.nodes[index]['id'] = row['_id']
        indexes[int(row['_id'])] = index
        
    else:
        G.add_edge(indexes[int(row['_start'])], indexes[int(row['_end'])])
        G_opt.add_edge(indexes[int(row['_start'])], indexes[int(row['_end'])])

print(df.head()) 



S=getConstraintGraph(dataset)


x = []

for i in range(10):
    
    
    #generate repairs
    df = generate_all_repairs(G_opt, S, G, repair(G.copy(),S), steps=len(G)*2)
    df["noise"] = 0
    df["dataset"] = dataset
    
    x.append(df.copy())
        
df = pd.concat(x)


df["V"] = df["G"].apply(lambda g: len(g.nodes))
df = df.reset_index()
df.head()


df["G'"].isna().sum()

nones = []
for i,g in df.groupby(["dataset", "noise", "user", "framework"]):
    
    na_sum = g["G'"].isna().sum()
    na_ratio = na_sum / len(g.index)
    mean_interactions = np.mean(g["Answers"].apply(len))
    if(i[0] == "generated"):
        interaction_budget_consumed = mean_interactions / g["V"].mean()
    else:
        interaction_budget_consumed = mean_interactions / (2 * g["V"].mean())
    
    nones.append((i, [na_ratio, interaction_budget_consumed]))
   
non_terminating = []
print("non terminating: \n")
for (group, values) in nones:
    if(values[0] > 0.5 and group[1] == "(0.27, 0.33)"):
        print(group, "failure ratio: ", round(values[0], 1), " | mean share of budget consumed: ", round(values[1], 3))
        non_terminating.append(group)
        
print("\n\nother failures that do not qualify as non terminating\n")
for (group, values) in nones:
    if(values[0] > 0 and values[0] <= 0.5 and group[1] == "(0.27, 0.33)"):
        print(group, "failure ratio: ", round(values[0], 1), " | mean share of budget consumed: ", round(values[1], 3))



for group in non_terminating:
    non_terminating_index = df.query("dataset == '"  + group[0] + "' & " + \
                                     "noise == '"    + group[1] + "' & " + \
                                     "user == '"     + group[2] + "' & " + \
                                     "framework == '"+ group[3] + "'").index.values
    df = df.drop(non_terminating_index)
    
df = df.dropna(subset = "G'")


def truth(G_opt, G):
    truth = set()
    
    for u in G.nodes:
        if(G.nodes[u]['label'] != G_opt.nodes[u]['label']):
            truth.add((u, G_opt.nodes[u]['label']))
    
    return truth

df["truth"] = df.apply(lambda x: truth(x["G_opt"], x["G"]), axis=1)

def modified(G, R):
    modified = set()
    
    for u in G.nodes:
        if(G.nodes[u]['label'] != R.nodes[u]['label']):
            modified.add((u, R.nodes[u]['label']))
    
    return modified

df["modified"] = df.apply(lambda x: modified(x["G"], x["G'"]), axis=1)

def tp(truth, modified):    
    return truth & modified

df["tp"] = df.apply(lambda x: tp(x["truth"], x["modified"]), axis=1)

def fp(modified, tp):
    return modified - tp
                         
df["fp"] = df.apply(lambda x: fp(x["modified"], x["tp"]), axis=1)


def fn(truth, fp, tp):
    return ((truth - fp) - tp)
df["fn"] = df.apply(lambda x: fn(x["truth"], x["fp"], x["tp"]), axis=1)
                         
#sanity check:
print(df.apply(lambda x: len(x["tp"] & x["fp"] & x["tp"]), axis=1).sum() == 0)


df["precision"] = df.apply(lambda x: len(x["tp"]) / ( len(x["tp"]) + len(x["fp"])), axis=1)
df["recall"] = df.apply(lambda x: len(x["tp"]) / ( len(x["tp"]) + len(x["fn"])), axis=1)

df["f1"] = df.apply(lambda x: 2*len(x["tp"]) / ( 2*len(x["tp"]) + len(x["fp"]) + len(x["fn"])), axis=1) 

for framework in ['term','gree','perm']:
    for user in ['userOracle','userGreedy','userGreedy']:
        print(framework, user, df.query("user == '"     + user+ "' & " + "framework == '"+framework + "'")['f1'].describe())