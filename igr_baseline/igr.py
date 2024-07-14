import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import string
from math import inf

##### LABELS AND VIOLATIONS

# A list of labels from A0000,...,Z0000,...A9999,...Z9999
alphabet = list(string.ascii_lowercase)
for i in range(1,1000):
  alphabet += [a + str(i) for a in list(string.ascii_lowercase)]


def valid_labels(v, G, S):
  """ The set of labels that respect neighborhood dependencies for v
  :param v: a vertex
  :param G: instance graph
  :param S: constraint set
  :return: a (possibly empty) set of labels
  """

  # neighbor labels
  neighbor_labels = set()
  for n in  G.neighbors(v):
    l = G.nodes[n]['label']
    if(l != None):
      neighbor_labels.add(l)
  
  # possible correct labels
  allowed_labels = set(S.nodes)
  for l in neighbor_labels:
    allowed_labels = allowed_labels.intersection(set(S.neighbors(l)))

  return allowed_labels


def isViolation(u,v, G, S):
  """ Is edge (u,v) a conflict w.r.t. S
  :return: True if (lambda(u), lambda(v)) not in N
  """
  return not ((G.nodes[u]['label'],G.nodes[v]['label']) in S.edges)

def violations(G,S):
  """ Returns the list of edges of G violating S
  :return: List of edges that violate S
  """
  violations = []
  for (u,v) in G.edges:
    if isViolation(u,v,G,S):
      violations.append((u,v))
  return violations

##### GENERATION
def label_v(v, G, S):
  """ Labels vertex v of G w.r.t. constraints S
  :param v: vertex
  :param G: instance graph
  :param S: constraints
  :return: True if the process succeeds
  """
  
  #get set of labels that respects the constraints
  allowed_labels = valid_labels(v,G,S)

  #if no label works, the process failed
  if(len(allowed_labels) == 0):
    return False
  
  G.nodes[v]['label'] = np.random.choice(list(allowed_labels))
  return True

def label_G(G,S):
  """ Labels graph G w.r.t. constraints S.
  Assigns labels randomly amongst valid ones along 
  BFS traversal of connected components with random source
  :param G: instance graph
  :param S: constraints
  :return: True if the process succeeds
  """

  nodes = dict(G.nodes(data='label'))
  while None in nodes.values():
    #   randomly select a vertex without label and label it
    to_label = [ v for (v,l) in nodes.items() if l == None]
    v = np.random.choice(to_label)
    G.nodes[v]['label'] = np.random.choice(S.nodes)

    # BFS assigning correct labels randomly
    for (_,u) in nx.bfs_edges(G, v):
      if(not label_v(u, G, S)):
        return False
    
    #update nodes
    nodes = dict(G.nodes(data='label'))
  
  return G

def generate_GS(v_size = 10, v_density = 1.5, lv_ratio = 0.5, l_density = 1.5, budget = 100):
  """ Generates an instance graph G=(V,E,lambda) and a constraint set S=(L,N)
  :param v_size: |V|, the size of G
  :param v_density: |E|/|V|, the density of G
  :param lv_ratio: |L|/|V|, the relative size of alphabet L to G
  :param l_density: |N|/|L|, the density of S
  :return: G,S, such that G respects S
  """

  # Generate G
  G = nx.Graph()

  V = np.arange(v_size)
  G.add_nodes_from(V)

  E = np.random.choice(V, size=round(v_size* v_density))
  E = [(u, np.random.choice(np.delete(V, u))) for u in E]
  G.add_edges_from(E)

  # Generate S
  S = nx.Graph()

  L = np.arange(round(lv_ratio*v_size))

  N = np.random.choice(L, size=round(len(L) * l_density))
  N = [(u, np.random.choice(np.delete(L, u))) for u in N]

  S.add_nodes_from([alphabet[l] for l in L])
  S.add_edges_from([ (alphabet[u], alphabet[v]) for (u,v) in N])
  # self_edges
  S.add_edges_from([ (alphabet[l], alphabet[l]) for l in L])

  # Label G as to respect S
  for v in G.nodes: 
    G.nodes[v]['label'] = None
  

  H = label_G(G.copy(),S)
  while(not H):
    # print("failed to label, retrying", budget)
    budget = budget - 1
    if(budget==0):
      raise TimeoutError
    H = label_G(G.copy(),S)

  return (H,S)

def inject_violation(v,G,S):
  """ Relabels v to create a violation
  :param v: vertex to relabel
  :param G: instance graph
  :param S: constraint set
  :return: True if the operation succeeds
  """
  
  allowed_labels = valid_labels(v,G,S)
  
  # incorrect labels
  violating_labels = set(S.nodes) - allowed_labels

  if(len(violating_labels) == 0):
    return False
  
  G.nodes[v]['label'] = np.random.choice(list(violating_labels))
  return True

# other version with ratio +- tolerance
def inject_violations(G, S, ratio_low = 0.18, ratio_high = 0.22, budget=100):
  """ Injects violations in G until the share of violations
   is in the given interval
  :param ratio_low: lower bound for |violations| / |E|
  :param ratio_high: upper bound for |violations| / |E|
  :param G: instance graph
  :param S: constraint set
  :return: True if the operation succeeds
  """
  
  while len(violations(G,S)) < len(G.edges) * ratio_low:
    n = np.random.choice(G.nodes)
    if(inject_violation(n, G, S) == False):
      budget = budget - 1
      if(budget==0):
        return False
    
  if(len(violations(G,S)) > len(G.edges) * ratio_high):
    return False
  
  return True

def force_inject_violations(G, S,
                            ratio_low = 0.15, ratio_high = 0.20,
                            budget = 1000, tries=10):
  """ Tries to inject_violations until succesful or budget is spent
  See inject_violations for more details
  :return: Modified G
  """
  # use a copy
  H = G.copy()

  while(not(inject_violations(H, S, ratio_low, ratio_high, budget=budget))):
    # undo injections
    H = G.copy()
    tries = tries - 1
    if tries == 0:
      raise TimeoutError

  return H

def generate_GSG(v_size=20, ratio=0.2):
    """ Generates a ground truth G, a constraint graph S, and H, a noisy version of G
    Note: this is a quick and dirty way to generate a trio. See other methods for more control
    :param v_size: the number of vertices in G and G'
    :param ratio: the noise ratio
    :return: G,S,H three graphs
    """
    G,S = generate_GS(v_size)
    H = force_inject_violations(G,S, ratio_low=ratio, ratio_high = ratio+0.03)
    return G,S,H

##### REPAIRING
def repair(G,S,verbose=False):
  """ Repairs G w.r.t. S by relabeling and deleting edges
  inspired by Neighorhoood constraints repair paper by Song et al
  """

  while len(violations(G,S)) > 0:
    # conflict participation
    conflict_participation = dict(zip(list(G.nodes), [0]*len(G.nodes)))
    all_violations = violations(G,S)
    for (u,v) in violations(G,S):
      conflict_participation[u] += 1
      conflict_participation[v] += 1
    # argmax with dict key
    candidates = [k for k,v in conflict_participation.items() if v == max(conflict_participation.values())]
    v = np.random.choice(candidates)

    allowed_labels = valid_labels(v, G, S)
    # deletion repair
    if(len(allowed_labels) == 0):
      for (x,y) in violations(G,S):
        if(x == v or y == v):
          G.remove_edge(x,y)
          if(verbose): 
            print("removing ", (x,y))
    # greedy relabelling repair
    else:
      best = G.nodes[v]['label']
      best_perf = len(violations(G,S))
      for l in allowed_labels:
        H = G.copy()
        H.nodes[v]['label'] = l
        perf = len(violations(H,S))
        if perf < best_perf:
          best = l
          best_perf = perf

      if(verbose):
        print("relabelling ", G.nodes[v]['label'], "-->", best)
      G.nodes[v]['label'] = best
  
  return G


def UserRepairWithMetadata(G,S, user, selectConflict, answers, apply, steps=1000, verbose=False):
  """ Repairs the graph G w.r.t. the constraints S by asking questions to the user using the framework
  Note: For framework definitions, see below
  :param G: Instance graph to be repaired
  :param S: Constraint graph
  :param user: a function with signature user(question, allowed answers, G, S) = answer
  :param selectConflict: a function that returns the question selected by the framework
  :param answers: a function that returns the set of allowed answers by the framework
  :param apply: a function to apply the answer to the graph
  :param steps: the maxium number of questions asked before throwing an error
  :return: the repaired graph G, the list of answers, the list of question complexities (a,b)
  """

  answer_trace = []
  question_cost = []
  while len(violations(G,S))>0:

    conflict = selectConflict(G,S)
    print(conflict)
    allowed_answers = answers(conflict, G, S)
    print(allowed_answers)
    answer = user(conflict, allowed_answers, G, S)
    print(answer)
    apply(conflict, answer, G, S)
    
    # trace
    answer_trace.append(answer)
    print(answer_trace)
    if(verbose):
      print("answer :", answer)
    
    #question cost
    question_cost.append(question_difficulty(conflict,allowed_answers,G))
    
    # force termination
    steps -= 1
    if(steps == 0):
      return None, answer_trace, question_cost

  return G, answer_trace, question_cost


def UserRepair(G,S, user, selectConflict, answers, apply, steps=1000, verbose=False):
  """ Like UserRepairWithMetadata, but without the metadata
  """ 
  return UserRepairWithMetadata(G,S,user, selectConflict, answers, apply, steps, verbose)[0]

##### QUESTION DIFFICULTY
def question_difficulty(conflict, allowed_answers, G):
    """ returns (a,b,c) to compute complexity(q) = alpha*a + beta*b
    :param conflict: the conflict formulation
    :param allowed_answers: the set of allowed answers
    :param G: the instance graph
    :return: a tuple of the components of question complexity
    """
    a = conflict_representation(conflict,G)
    b = len(allowed_answers)
    return (a,b)

def conflict_representation(conflict,G):
    """ returns the number of vertices needed to represent the conflict
    """
    #if question includes a possible repair
    if type(conflict[0]) is tuple:
        return 4
    else:
        return 2

##### INTERACTION MODELS

### F Boolean
### The framework greedily asks for a possible repair, the user answers yes or no
def selectConflictPossibleRepair(G,S):
  """ Select a possible repair for a greedily selected conflict
  """

  conflict = selectConflictGreedy(G,S)
  repairs = answersRepair(conflict, G, S)

  return (conflict, repairs[np.random.choice(len(repairs))])

def answersBoolean(conflict, G, S):
  return ["yes", "no"]

def applyBoolean(conflict, answer, G, S):
  """ If answer is "yes", apply the proposed repair 
  """
  if(answer == "yes"):
    # unpack the "conflict = (edge, proposed repair)"
    (edge, repair) = conflict
    if(repair == "delete"):
      G.remove_edge(*edge)
    else:
      (u,l) = repair
      G.nodes[u]['label'] = l
      G.nodes[u]['modified'] = True
  else:
    #answer is no, don't do anything
    pass
  return

f_bool = (selectConflictPossibleRepair, answersBoolean, applyBoolean)

### Fgreedy
### asks to repair a greedily selected conflict, user answers a possible repair

def selectConflictGreedy(G,S):
  """ Greedily select a conflict (u,v)
  """

  conflict_participation = dict(zip(list(G.nodes), [0]*len(G.nodes)))
  all_violations = violations(G,S)
  for (u,v) in all_violations:
    conflict_participation[u] += 1
    conflict_participation[v] += 1
  v = max(conflict_participation, key=conflict_participation.get)

  possible_e = [(u,w) for (u,w) in all_violations if((u == v) or (w==v))]

  return possible_e[np.random.choice(len(possible_e))]

def answersRepair(conflict, G, S):
  """ all valid repairs for conflict (u,v), 
  i.e. relabeling repairs for u or v, or delete the edge
  """
  (u,v) = conflict
  repairs = [(u,l) for l in valid_labels(u, G.subgraph([u,v]), S)] + \
            [(v,l) for l in valid_labels(v, G.subgraph([u,v]), S)] + \
            [ "delete"]
  return repairs

def applyTransformation(conflict, answer, G, S):
  if(answer == "delete"):
    G.remove_edge(*conflict)
  else:
    (u,l) = answer
    G.nodes[u]['label'] = l
    G.nodes[u]['modified'] = True
  return

f_gree = (selectConflictGreedy, answersRepair, applyTransformation)

### Fpermissive
### asks for a greedily selected conflict, the user answers any graph transformation

def answersTransformation(conflict, G, S):
  """ Any transformation on (u,v), 
  i.e. any relabeling of u or v, or delete the edge
  """
  (u,v) = conflict
  transformations = [(u,l) for l in S.nodes] + \
                    [(v,l) for l in S.nodes] + \
                    [ "delete"]
  return transformations

f_perm = (selectConflictGreedy, answersTransformation, applyTransformation)

### Fterminate
### Like Fgreedy, but only answers that decrease the total number of violations are allowed

def answersDecrease(conflict, G, S):
    """ Any transformation on (u,v) that reduces the number of conflicts in G wrt S, 
    """
    repairs = answersRepair(conflict, G, S)
    subgraph = G.subgraph(conflict_neighborhood(conflict, G))
    decreasing_repairs = []
    for r in repairs:
        modified = subgraph.copy()
        applyTransformation(conflict, r, modified, S)
        if len(violations(subgraph, S)) > len(violations(modified, S)):
            decreasing_repairs.append(r)
    return decreasing_repairs

f_term = (selectConflictGreedy, answersDecrease, applyTransformation)

### utilitaries
def conflict_neighborhood(conflict, G):
  """ returns only the subgraph around the conflict
  """

  if type(conflict[0]) is tuple:
        conflict = conflict[0]
  context = set(conflict)
  for u in conflict:
    for n in nx.neighbors(G, u):
      context.add(n)
  return context

##### USER SIMULATION

### Random
def userRandom(conflict, answers, G, S):
  """ Randomly selects amongst the answers
  """
  return answers[np.random.choice(len(answers))]

### Greedy
def userGreedy_(conflict, answers, G, S, apply):
  """ Tries all possible answers, selects the best in terms of remaining violations
  Note: needs to know the apply function to try the answers.
  See below for a version with classic apply function
  """
  # work on subgraph of interest
  context = conflict_neighborhood(conflict, G)
  sub_G = G.subgraph(context)
            
  # test all answers
  best = None
  best_perf = len(violations(sub_G,S))
  for a in answers:
    H = sub_G.copy()
    apply(conflict, a, H, S)
    current_perf = len(violations(H,S))
    if(current_perf < best_perf):
        best = a
        best_perf = current_perf

  return best if (best != None) else "delete"

def userGreedyCustomApplication(apply):
  return lambda conflict, answers, G, S: userGreedy_(conflict, answers, G, S, apply)

userGreedy = userGreedyCustomApplication(applyTransformation)
  
### Oracle

def userOracle_(conflict, answers, G, S, apply, G_opt):
  """ Tries all answers, selects the one ending closest to optimal G_opt
  Note: needs to know the apply function to try the answers, and the opt
  See below for a version with classic apply function
  """
  # work on subgraph of interest
  context = conflict_neighborhood(conflict, G)
  sub_G = G.subgraph(context)
  sub_G_opt = G_opt.subgraph(context)

  # test all answers
  best = None
  best_perf = inf

  for a in answers:
    H = sub_G.copy()
    apply(conflict, a, H, S)
    # performance is distance to searched graph
    current_perf = graph_diff(H, sub_G_opt)
    if(current_perf < best_perf):
        best = a
        best_perf = current_perf

  return best

def userOracle(G_opt, apply):
  return lambda conflict, answers, G, S: userOracle_(conflict, answers, G, S, apply, G_opt)

##### Generating repairs

def generate_all_repairs(G_opt, S, G, R, steps=1000):
    """ Generates a dataframe with repairs for every combination of framework and user
    :param G_opt: ground truth
    :param S: constraints
    :param G: instance graph
    :param R: result of automatic repair
    :return: a df with columns (G, S, G_opt, R, G', Answers, framework, user)
    """
    
    # make an empty dataframe
    df = pd.DataFrame(columns=["G", "S", "G_opt", "R", "G'", "Answers", "Q_difficulty", "framework", "user"])

    for u in ["userRandom", "userGreedy", "userOracle"]:
        for f in ["bool", "gree", "perm", "term"]:
            df = df.append(dict(zip(df.columns, [G,S,G_opt,R, None, None, None, f, u])), ignore_index=True)

    # repair the graph with all framework / user combination
    G_r_f_bool, A_r_f_bool, QD_r_f_bool = UserRepairWithMetadata(G.copy(),S,userRandom, *f_bool, steps=steps)
    G_r_f_gree, A_r_f_gree, QD_r_f_gree = UserRepairWithMetadata(G.copy(),S,userRandom, *f_gree, steps=steps)
    G_r_f_perm, A_r_f_perm, QD_r_f_perm = UserRepairWithMetadata(G.copy(),S,userRandom, *f_perm, steps=steps)
    G_r_f_term, A_r_f_term, QD_r_f_term = UserRepairWithMetadata(G.copy(),S,userRandom, *f_term, steps=steps)
    G_g_f_bool, A_g_f_bool, QD_g_f_bool = UserRepairWithMetadata(G.copy(),S,userGreedyCustomApplication(applyBoolean), *f_bool, steps=steps)
    G_g_f_gree, A_g_f_gree, QD_g_f_gree = UserRepairWithMetadata(G.copy(),S,userGreedy,                                *f_gree, steps=steps)
    G_g_f_perm, A_g_f_perm, QD_g_f_perm = UserRepairWithMetadata(G.copy(),S,userGreedy,                                *f_perm, steps=steps)
    G_g_f_term, A_g_f_term, QD_g_f_term = UserRepairWithMetadata(G.copy(),S,userGreedy,                                *f_term, steps=steps)
    G_o_f_bool, A_o_f_bool, QD_o_f_bool = UserRepairWithMetadata(G.copy(),S,userOracle(G_opt, applyBoolean),        *f_bool, steps=steps)
    G_o_f_gree, A_o_f_gree, QD_o_f_gree = UserRepairWithMetadata(G.copy(),S,userOracle(G_opt, applyTransformation), *f_gree, steps=steps)
    G_o_f_perm, A_o_f_perm, QD_o_f_perm = UserRepairWithMetadata(G.copy(),S,userOracle(G_opt, applyTransformation), *f_perm, steps=steps)
    G_o_f_term, A_o_f_term, QD_o_f_term = UserRepairWithMetadata(G.copy(),S,userOracle(G_opt, applyTransformation), *f_term, steps=steps)


    # populate the df
    # NOTE make use of column selection to edit here
    df.iloc[df.query("user == 'userRandom' & framework == 'bool'").index[0]]["G'"] = G_r_f_bool
    df.iloc[df.query("user == 'userRandom' & framework == 'gree'").index[0]]["G'"] = G_r_f_gree
    df.iloc[df.query("user == 'userRandom' & framework == 'perm'").index[0]]["G'"] = G_r_f_perm
    df.iloc[df.query("user == 'userRandom' & framework == 'term'").index[0]]["G'"] = G_g_f_term
    df.iloc[df.query("user == 'userGreedy' & framework == 'bool'").index[0]]["G'"] = G_g_f_bool
    df.iloc[df.query("user == 'userGreedy' & framework == 'gree'").index[0]]["G'"] = G_g_f_gree
    df.iloc[df.query("user == 'userGreedy' & framework == 'perm'").index[0]]["G'"] = G_g_f_perm
    df.iloc[df.query("user == 'userGreedy' & framework == 'term'").index[0]]["G'"] = G_g_f_term
    df.iloc[df.query("user == 'userOracle' & framework == 'bool'").index[0]]["G'"] = G_o_f_bool
    df.iloc[df.query("user == 'userOracle' & framework == 'gree'").index[0]]["G'"] = G_o_f_gree
    df.iloc[df.query("user == 'userOracle' & framework == 'perm'").index[0]]["G'"] = G_o_f_perm
    df.iloc[df.query("user == 'userOracle' & framework == 'term'").index[0]]["G'"] = G_o_f_term
    
    df.iloc[df.query("user == 'userRandom' & framework == 'bool'").index[0]]["Answers"] = A_r_f_bool
    df.iloc[df.query("user == 'userRandom' & framework == 'gree'").index[0]]["Answers"] = A_r_f_gree
    df.iloc[df.query("user == 'userRandom' & framework == 'perm'").index[0]]["Answers"] = A_r_f_perm
    df.iloc[df.query("user == 'userRandom' & framework == 'term'").index[0]]["Answers"] = A_r_f_term
    df.iloc[df.query("user == 'userGreedy' & framework == 'bool'").index[0]]["Answers"] = A_g_f_bool
    df.iloc[df.query("user == 'userGreedy' & framework == 'gree'").index[0]]["Answers"] = A_g_f_gree
    df.iloc[df.query("user == 'userGreedy' & framework == 'perm'").index[0]]["Answers"] = A_g_f_perm
    df.iloc[df.query("user == 'userGreedy' & framework == 'term'").index[0]]["Answers"] = A_g_f_term
    df.iloc[df.query("user == 'userOracle' & framework == 'bool'").index[0]]["Answers"] = A_o_f_bool
    df.iloc[df.query("user == 'userOracle' & framework == 'gree'").index[0]]["Answers"] = A_o_f_gree
    df.iloc[df.query("user == 'userOracle' & framework == 'perm'").index[0]]["Answers"] = A_o_f_perm
    df.iloc[df.query("user == 'userOracle' & framework == 'term'").index[0]]["Answers"] = A_o_f_term
    
    df.iloc[df.query("user == 'userRandom' & framework == 'bool'").index[0]]["Q_difficulty"] = QD_r_f_bool
    df.iloc[df.query("user == 'userRandom' & framework == 'gree'").index[0]]["Q_difficulty"] = QD_r_f_gree
    df.iloc[df.query("user == 'userRandom' & framework == 'perm'").index[0]]["Q_difficulty"] = QD_r_f_perm
    df.iloc[df.query("user == 'userRandom' & framework == 'term'").index[0]]["Q_difficulty"] = QD_r_f_term
    df.iloc[df.query("user == 'userGreedy' & framework == 'bool'").index[0]]["Q_difficulty"] = QD_g_f_bool
    df.iloc[df.query("user == 'userGreedy' & framework == 'gree'").index[0]]["Q_difficulty"] = QD_g_f_gree
    df.iloc[df.query("user == 'userGreedy' & framework == 'perm'").index[0]]["Q_difficulty"] = QD_g_f_perm
    df.iloc[df.query("user == 'userGreedy' & framework == 'term'").index[0]]["Q_difficulty"] = QD_g_f_term
    df.iloc[df.query("user == 'userOracle' & framework == 'bool'").index[0]]["Q_difficulty"] = QD_o_f_bool
    df.iloc[df.query("user == 'userOracle' & framework == 'gree'").index[0]]["Q_difficulty"] = QD_o_f_gree
    df.iloc[df.query("user == 'userOracle' & framework == 'perm'").index[0]]["Q_difficulty"] = QD_o_f_perm
    df.iloc[df.query("user == 'userOracle' & framework == 'term'").index[0]]["Q_difficulty"] = QD_o_f_term
    
    return df


##### DRAWING 

def draw_G(G, S, **kwds):
  """ Draws a labelled undirected graph with colored violations
  """
  edge_color = ["red" if isViolation(u,v,G,S) else "black" for (u,v) in G.edges]
  nx.draw(G, with_labels=True, labels=dict(G.nodes(data='label')),
          edge_color=edge_color,
          **kwds)
  return

def draw_S(S, **kwds):
  nx.draw(S, with_labels=True, node_color="green", node_shape="s", **kwds)
  return

def drawing_pos(G,S):
  """returns fixed drawing positions for G and S vertices
  """
  pos_G = nx.drawing.layout.kamada_kawai_layout(G)
  pos_S = nx.drawing.layout.kamada_kawai_layout(S)
  return (pos_G, pos_S)

def draw_GS(G,S, pos=None):
  """ draws G and S side to side
  :param G: see draw_G
  :param S: see draw_S
  :param pos: see drawing_pos
  """
  _, (ax1, ax2) = plt.subplots(1,2, figsize=(10,5))
  if(pos==None):
    draw_G(G,S,ax=ax1)
    draw_S(S,ax=ax2)
  else:
    (pos_G, pos_S) = pos
    draw_G(G,S,ax=ax1, pos=pos_G)
    draw_S(S,ax=ax2, pos=pos_S)
  return

##### LABELLED GRAPH

def graph_diff(G1, G2, theta = 0.5):
  """ diff = theta * #relabelings + (1-theta) * #deletions
  Assuming same node set
  :param theta: theta as in cost
  """
  if(G1 == None) or (G2==None):
    return None
  
  dist = 0

  # differing label is a difference
  for n in G1.nodes:
    l = G1.nodes[n]['label']
    h = G2.nodes[n]['label']
    if(l != h):
      dist = dist + theta

  # differing edges is a difference
  for e in G1.edges:
    if e not in G2.edges:
      dist = dist + 1 - theta
  for e in G2.edges:
    if e not in G1.edges:
      dist = dist + 1 - theta

  return dist





import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import string
from math import inf

##### LABELS AND VIOLATIONS

# A list of labels from A0000,...,Z0000,...A9999,...Z9999
alphabet = list(string.ascii_lowercase)
for i in range(1,1000):
  alphabet += [a + str(i) for a in list(string.ascii_lowercase)]


def valid_labels(v, G, S):
  """ The set of labels that respect neighborhood dependencies for v
  :param v: a vertex
  :param G: instance graph
  :param S: constraint set
  :return: a (possibly empty) set of labels
  """

  # neighbor labels
  neighbor_labels = set()
  for n in  G.neighbors(v):
    l = G.nodes[n]['label']
    if(l != None):
      neighbor_labels.add(l)
  
  # possible correct labels
  allowed_labels = set(S.nodes)
  for l in neighbor_labels:
    allowed_labels = allowed_labels.intersection(set(S.neighbors(l)))

  return allowed_labels


def isViolation(u,v, G, S):
  """ Is edge (u,v) a conflict w.r.t. S
  :return: True if (lambda(u), lambda(v)) not in N
  """
  return not ((G.nodes[u]['label'],G.nodes[v]['label']) in S.edges)

def violations(G,S):
  """ Returns the list of edges of G violating S
  :return: List of edges that violate S
  """
  violations = []
  for (u,v) in G.edges:
    if isViolation(u,v,G,S):
      violations.append((u,v))
  return violations

##### GENERATION
def label_v(v, G, S):
  """ Labels vertex v of G w.r.t. constraints S
  :param v: vertex
  :param G: instance graph
  :param S: constraints
  :return: True if the process succeeds
  """
  
  #get set of labels that respects the constraints
  allowed_labels = valid_labels(v,G,S)

  #if no label works, the process failed
  if(len(allowed_labels) == 0):
    return False
  
  G.nodes[v]['label'] = np.random.choice(list(allowed_labels))
  return True

def label_G(G,S):
  """ Labels graph G w.r.t. constraints S.
  Assigns labels randomly amongst valid ones along 
  BFS traversal of connected components with random source
  :param G: instance graph
  :param S: constraints
  :return: True if the process succeeds
  """

  nodes = dict(G.nodes(data='label'))
  while None in nodes.values():
    #   randomly select a vertex without label and label it
    to_label = [ v for (v,l) in nodes.items() if l == None]
    v = np.random.choice(to_label)
    G.nodes[v]['label'] = np.random.choice(S.nodes)

    # BFS assigning correct labels randomly
    for (_,u) in nx.bfs_edges(G, v):
      if(not label_v(u, G, S)):
        return False
    
    #update nodes
    nodes = dict(G.nodes(data='label'))
  
  return G

def generate_GS(v_size = 10, v_density = 1.5, lv_ratio = 0.5, l_density = 1.5, budget = 100):
  """ Generates an instance graph G=(V,E,lambda) and a constraint set S=(L,N)
  :param v_size: |V|, the size of G
  :param v_density: |E|/|V|, the density of G
  :param lv_ratio: |L|/|V|, the relative size of alphabet L to G
  :param l_density: |N|/|L|, the density of S
  :return: G,S, such that G respects S
  """

  # Generate G
  G = nx.Graph()

  V = np.arange(v_size)
  G.add_nodes_from(V)

  E = np.random.choice(V, size=round(v_size* v_density))
  E = [(u, np.random.choice(np.delete(V, u))) for u in E]
  G.add_edges_from(E)

  # Generate S
  S = nx.Graph()

  L = np.arange(round(lv_ratio*v_size))

  N = np.random.choice(L, size=round(len(L) * l_density))
  N = [(u, np.random.choice(np.delete(L, u))) for u in N]

  S.add_nodes_from([alphabet[l] for l in L])
  S.add_edges_from([ (alphabet[u], alphabet[v]) for (u,v) in N])
  # self_edges
  S.add_edges_from([ (alphabet[l], alphabet[l]) for l in L])

  # Label G as to respect S
  for v in G.nodes: 
    G.nodes[v]['label'] = None
  

  H = label_G(G.copy(),S)
  while(not H):
    # print("failed to label, retrying", budget)
    budget = budget - 1
    if(budget==0):
      raise TimeoutError
    H = label_G(G.copy(),S)

  return (H,S)

def inject_violation(v,G,S):
  """ Relabels v to create a violation
  :param v: vertex to relabel
  :param G: instance graph
  :param S: constraint set
  :return: True if the operation succeeds
  """
  
  allowed_labels = valid_labels(v,G,S)
  
  # incorrect labels
  violating_labels = set(S.nodes) - allowed_labels

  if(len(violating_labels) == 0):
    return False
  
  G.nodes[v]['label'] = np.random.choice(list(violating_labels))
  return True

# other version with ratio +- tolerance
def inject_violations(G, S, ratio_low = 0.18, ratio_high = 0.22, budget=100):
  """ Injects violations in G until the share of violations
   is in the given interval
  :param ratio_low: lower bound for |violations| / |E|
  :param ratio_high: upper bound for |violations| / |E|
  :param G: instance graph
  :param S: constraint set
  :return: True if the operation succeeds
  """
  
  while len(violations(G,S)) < len(G.edges) * ratio_low:
    n = np.random.choice(G.nodes)
    if(inject_violation(n, G, S) == False):
      budget = budget - 1
      if(budget==0):
        return False
    
  if(len(violations(G,S)) > len(G.edges) * ratio_high):
    return False
  
  return True

def force_inject_violations(G, S,
                            ratio_low = 0.15, ratio_high = 0.20,
                            budget = 1000, tries=10):
  """ Tries to inject_violations until succesful or budget is spent
  See inject_violations for more details
  :return: Modified G
  """
  # use a copy
  H = G.copy()

  while(not(inject_violations(H, S, ratio_low, ratio_high, budget=budget))):
    # undo injections
    H = G.copy()
    tries = tries - 1
    if tries == 0:
      raise TimeoutError

  return H

def generate_GSG(v_size=20, ratio=0.2):
    """ Generates a ground truth G, a constraint graph S, and H, a noisy version of G
    Note: this is a quick and dirty way to generate a trio. See other methods for more control
    :param v_size: the number of vertices in G and G'
    :param ratio: the noise ratio
    :return: G,S,H three graphs
    """
    G,S = generate_GS(v_size)
    H = force_inject_violations(G,S, ratio_low=ratio, ratio_high = ratio+0.03)
    return G,S,H

##### REPAIRING
def repair(G,S,verbose=False):
  """ Repairs G w.r.t. S by relabeling and deleting edges
  inspired by Neighorhoood constraints repair paper by Song et al
  """

  while len(violations(G,S)) > 0:
    # conflict participation
    conflict_participation = dict(zip(list(G.nodes), [0]*len(G.nodes)))
    all_violations = violations(G,S)
    for (u,v) in violations(G,S):
      conflict_participation[u] += 1
      conflict_participation[v] += 1
    # argmax with dict key
    candidates = [k for k,v in conflict_participation.items() if v == max(conflict_participation.values())]
    v = np.random.choice(candidates)

    allowed_labels = valid_labels(v, G, S)
    # deletion repair
    if(len(allowed_labels) == 0):
      for (x,y) in violations(G,S):
        if(x == v or y == v):
          G.remove_edge(x,y)
          if(verbose): 
            print("removing ", (x,y))
    # greedy relabelling repair
    else:
      best = G.nodes[v]['label']
      best_perf = len(violations(G,S))
      for l in allowed_labels:
        H = G.copy()
        H.nodes[v]['label'] = l
        perf = len(violations(H,S))
        if perf < best_perf:
          best = l
          best_perf = perf

      if(verbose):
        print("relabelling ", G.nodes[v]['label'], "-->", best)
      G.nodes[v]['label'] = best
  
  return G


def UserRepairWithMetadata(G,S, user, selectConflict, answers, apply, steps=1000, verbose=False):
  """ Repairs the graph G w.r.t. the constraints S by asking questions to the user using the framework
  Note: For framework definitions, see below
  :param G: Instance graph to be repaired
  :param S: Constraint graph
  :param user: a function with signature user(question, allowed answers, G, S) = answer
  :param selectConflict: a function that returns the question selected by the framework
  :param answers: a function that returns the set of allowed answers by the framework
  :param apply: a function to apply the answer to the graph
  :param steps: the maxium number of questions asked before throwing an error
  :return: the repaired graph G, the list of answers, the list of question complexities (a,b)
  """

  answer_trace = []
  question_cost = []
  while len(violations(G,S))>0:

    conflict = selectConflict(G,S)
    allowed_answers = answers(conflict, G, S)
    answer = user(conflict, allowed_answers, G, S)
    apply(conflict, answer, G, S)

    # trace
    answer_trace.append(answer)
    if(verbose):
      print("answer :", answer)
    
    #question cost
    question_cost.append(question_difficulty(conflict,allowed_answers,G))
    
    # force termination
    steps -= 1
    if(steps == 0):
      return None, answer_trace, question_cost

  return G, answer_trace, question_cost


def UserRepair(G,S, user, selectConflict, answers, apply, steps=1000, verbose=False):
  """ Like UserRepairWithMetadata, but without the metadata
  """ 
  return UserRepairWithMetadata(G,S,user, selectConflict, answers, apply, steps, verbose)[0]

##### QUESTION DIFFICULTY
def question_difficulty(conflict, allowed_answers, G):
    """ returns (a,b,c) to compute complexity(q) = alpha*a + beta*b
    :param conflict: the conflict formulation
    :param allowed_answers: the set of allowed answers
    :param G: the instance graph
    :return: a tuple of the components of question complexity
    """
    a = conflict_representation(conflict,G)
    b = len(allowed_answers)
    return (a,b)

def conflict_representation(conflict,G):
    """ returns the number of vertices needed to represent the conflict
    """
    #if question includes a possible repair
    if type(conflict[0]) is tuple:
        return 4
    else:
        return 2

##### INTERACTION MODELS

### F Boolean
### The framework greedily asks for a possible repair, the user answers yes or no
def selectConflictPossibleRepair(G,S):
  """ Select a possible repair for a greedily selected conflict
  """

  conflict = selectConflictGreedy(G,S)
  repairs = answersRepair(conflict, G, S)

  return (conflict, repairs[np.random.choice(len(repairs))])

def answersBoolean(conflict, G, S):
  return ["yes", "no"]

def applyBoolean(conflict, answer, G, S):
  """ If answer is "yes", apply the proposed repair 
  """
  if(answer == "yes"):
    # unpack the "conflict = (edge, proposed repair)"
    (edge, repair) = conflict
    if(repair == "delete"):
      G.remove_edge(*edge)
    else:
      (u,l) = repair
      G.nodes[u]['label'] = l
      G.nodes[u]['modified'] = True
  else:
    #answer is no, don't do anything
    pass
  return

f_bool = (selectConflictPossibleRepair, answersBoolean, applyBoolean)

### Fgreedy
### asks to repair a greedily selected conflict, user answers a possible repair

def selectConflictGreedy(G,S):
  """ Greedily select a conflict (u,v)
  """

  conflict_participation = dict(zip(list(G.nodes), [0]*len(G.nodes)))
  all_violations = violations(G,S)
  for (u,v) in all_violations:
    conflict_participation[u] += 1
    conflict_participation[v] += 1
  v = max(conflict_participation, key=conflict_participation.get)

  possible_e = [(u,w) for (u,w) in all_violations if((u == v) or (w==v))]

  return possible_e[np.random.choice(len(possible_e))]

def answersRepair(conflict, G, S):
  """ all valid repairs for conflict (u,v), 
  i.e. relabeling repairs for u or v, or delete the edge
  """
  (u,v) = conflict
  repairs = [(u,l) for l in valid_labels(u, G.subgraph([u,v]), S)] + \
            [(v,l) for l in valid_labels(v, G.subgraph([u,v]), S)] + \
            [ "delete"]
  return repairs

def applyTransformation(conflict, answer, G, S):
  if(answer == "delete"):
    G.remove_edge(*conflict)
  else:
    (u,l) = answer
    G.nodes[u]['label'] = l
    G.nodes[u]['modified'] = True
  return

f_gree = (selectConflictGreedy, answersRepair, applyTransformation)

### Fpermissive
### asks for a greedily selected conflict, the user answers any graph transformation

def answersTransformation(conflict, G, S):
  """ Any transformation on (u,v), 
  i.e. any relabeling of u or v, or delete the edge
  """
  (u,v) = conflict
  transformations = [(u,l) for l in S.nodes] + \
                    [(v,l) for l in S.nodes] + \
                    [ "delete"]
  return transformations

f_perm = (selectConflictGreedy, answersTransformation, applyTransformation)

### Fterminate
### Like Fgreedy, but only answers that decrease the total number of violations are allowed

def answersDecrease(conflict, G, S):
    """ Any transformation on (u,v) that reduces the number of conflicts in G wrt S, 
    """
    repairs = answersRepair(conflict, G, S)
    subgraph = G.subgraph(conflict_neighborhood(conflict, G))
    decreasing_repairs = []
    for r in repairs:
        modified = subgraph.copy()
        applyTransformation(conflict, r, modified, S)
        if len(violations(subgraph, S)) > len(violations(modified, S)):
            decreasing_repairs.append(r)
    return decreasing_repairs

f_term = (selectConflictGreedy, answersDecrease, applyTransformation)

### utilitaries
def conflict_neighborhood(conflict, G):
  """ returns only the subgraph around the conflict
  """

  if type(conflict[0]) is tuple:
        conflict = conflict[0]
  context = set(conflict)
  for u in conflict:
    for n in nx.neighbors(G, u):
      context.add(n)
  return context

##### USER SIMULATION

### Random
def userRandom(conflict, answers, G, S):
  """ Randomly selects amongst the answers
  """
  return answers[np.random.choice(len(answers))]

### Greedy
def userGreedy_(conflict, answers, G, S, apply):
  """ Tries all possible answers, selects the best in terms of remaining violations
  Note: needs to know the apply function to try the answers.
  See below for a version with classic apply function
  """
  # work on subgraph of interest
  context = conflict_neighborhood(conflict, G)
  sub_G = G.subgraph(context)
            
  # test all answers
  best = None
  best_perf = len(violations(sub_G,S))
  for a in answers:
    H = sub_G.copy()
    apply(conflict, a, H, S)
    current_perf = len(violations(H,S))
    if(current_perf < best_perf):
        best = a
        best_perf = current_perf

  return best if (best != None) else "delete"

def userGreedyCustomApplication(apply):
  return lambda conflict, answers, G, S: userGreedy_(conflict, answers, G, S, apply)

userGreedy = userGreedyCustomApplication(applyTransformation)
  
### Oracle

def userOracle_(conflict, answers, G, S, apply, G_opt):
  """ Tries all answers, selects the one ending closest to optimal G_opt
  Note: needs to know the apply function to try the answers, and the opt
  See below for a version with classic apply function
  """
  # work on subgraph of interest
  context = conflict_neighborhood(conflict, G)
  sub_G = G.subgraph(context)
  sub_G_opt = G_opt.subgraph(context)

  # test all answers
  best = None
  best_perf = inf

  for a in answers:
    H = sub_G.copy()
    apply(conflict, a, H, S)
    # performance is distance to searched graph
    current_perf = graph_diff(H, sub_G_opt)
    if(current_perf < best_perf):
        best = a
        best_perf = current_perf

  return best

def userOracle(G_opt, apply):
  return lambda conflict, answers, G, S: userOracle_(conflict, answers, G, S, apply, G_opt)

##### Generating repairs

def generate_all_repairs(G_opt, S, G, R, steps=1000):
    """ Generates a dataframe with repairs for every combination of framework and user
    :param G_opt: ground truth
    :param S: constraints
    :param G: instance graph
    :param R: result of automatic repair
    :return: a df with columns (G, S, G_opt, R, G', Answers, framework, user)
    """
    
    # make an empty dataframe
    df = pd.DataFrame(columns=["G", "S", "G_opt", "R", "G'", "Answers", "Q_difficulty", "framework", "user"])

    for u in ["userRandom", "userGreedy", "userOracle"]:
        for f in ["bool", "gree", "perm", "term"]:
            df = df.append(dict(zip(df.columns, [G,S,G_opt,R, None, None, None, f, u])), ignore_index=True)

    # repair the graph with all framework / user combination
    G_r_f_bool, A_r_f_bool, QD_r_f_bool = UserRepairWithMetadata(G.copy(),S,userRandom, *f_bool, steps=steps)
    G_r_f_gree, A_r_f_gree, QD_r_f_gree = UserRepairWithMetadata(G.copy(),S,userRandom, *f_gree, steps=steps)
    G_r_f_perm, A_r_f_perm, QD_r_f_perm = UserRepairWithMetadata(G.copy(),S,userRandom, *f_perm, steps=steps)
    G_r_f_term, A_r_f_term, QD_r_f_term = UserRepairWithMetadata(G.copy(),S,userRandom, *f_term, steps=steps)
    G_g_f_bool, A_g_f_bool, QD_g_f_bool = UserRepairWithMetadata(G.copy(),S,userGreedyCustomApplication(applyBoolean), *f_bool, steps=steps)
    G_g_f_gree, A_g_f_gree, QD_g_f_gree = UserRepairWithMetadata(G.copy(),S,userGreedy,                                *f_gree, steps=steps)
    G_g_f_perm, A_g_f_perm, QD_g_f_perm = UserRepairWithMetadata(G.copy(),S,userGreedy,                                *f_perm, steps=steps)
    G_g_f_term, A_g_f_term, QD_g_f_term = UserRepairWithMetadata(G.copy(),S,userGreedy,                                *f_term, steps=steps)
    G_o_f_bool, A_o_f_bool, QD_o_f_bool = UserRepairWithMetadata(G.copy(),S,userOracle(G_opt, applyBoolean),        *f_bool, steps=steps)
    G_o_f_gree, A_o_f_gree, QD_o_f_gree = UserRepairWithMetadata(G.copy(),S,userOracle(G_opt, applyTransformation), *f_gree, steps=steps)
    G_o_f_perm, A_o_f_perm, QD_o_f_perm = UserRepairWithMetadata(G.copy(),S,userOracle(G_opt, applyTransformation), *f_perm, steps=steps)
    G_o_f_term, A_o_f_term, QD_o_f_term = UserRepairWithMetadata(G.copy(),S,userOracle(G_opt, applyTransformation), *f_term, steps=steps)


    # populate the df
    # NOTE make use of column selection to edit here
    df.iloc[df.query("user == 'userRandom' & framework == 'bool'").index[0]]["G'"] = G_r_f_bool
    df.iloc[df.query("user == 'userRandom' & framework == 'gree'").index[0]]["G'"] = G_r_f_gree
    df.iloc[df.query("user == 'userRandom' & framework == 'perm'").index[0]]["G'"] = G_r_f_perm
    df.iloc[df.query("user == 'userRandom' & framework == 'term'").index[0]]["G'"] = G_g_f_term
    df.iloc[df.query("user == 'userGreedy' & framework == 'bool'").index[0]]["G'"] = G_g_f_bool
    df.iloc[df.query("user == 'userGreedy' & framework == 'gree'").index[0]]["G'"] = G_g_f_gree
    df.iloc[df.query("user == 'userGreedy' & framework == 'perm'").index[0]]["G'"] = G_g_f_perm
    df.iloc[df.query("user == 'userGreedy' & framework == 'term'").index[0]]["G'"] = G_g_f_term
    df.iloc[df.query("user == 'userOracle' & framework == 'bool'").index[0]]["G'"] = G_o_f_bool
    df.iloc[df.query("user == 'userOracle' & framework == 'gree'").index[0]]["G'"] = G_o_f_gree
    df.iloc[df.query("user == 'userOracle' & framework == 'perm'").index[0]]["G'"] = G_o_f_perm
    df.iloc[df.query("user == 'userOracle' & framework == 'term'").index[0]]["G'"] = G_o_f_term
    
    df.iloc[df.query("user == 'userRandom' & framework == 'bool'").index[0]]["Answers"] = A_r_f_bool
    df.iloc[df.query("user == 'userRandom' & framework == 'gree'").index[0]]["Answers"] = A_r_f_gree
    df.iloc[df.query("user == 'userRandom' & framework == 'perm'").index[0]]["Answers"] = A_r_f_perm
    df.iloc[df.query("user == 'userRandom' & framework == 'term'").index[0]]["Answers"] = A_r_f_term
    df.iloc[df.query("user == 'userGreedy' & framework == 'bool'").index[0]]["Answers"] = A_g_f_bool
    df.iloc[df.query("user == 'userGreedy' & framework == 'gree'").index[0]]["Answers"] = A_g_f_gree
    df.iloc[df.query("user == 'userGreedy' & framework == 'perm'").index[0]]["Answers"] = A_g_f_perm
    df.iloc[df.query("user == 'userGreedy' & framework == 'term'").index[0]]["Answers"] = A_g_f_term
    df.iloc[df.query("user == 'userOracle' & framework == 'bool'").index[0]]["Answers"] = A_o_f_bool
    df.iloc[df.query("user == 'userOracle' & framework == 'gree'").index[0]]["Answers"] = A_o_f_gree
    df.iloc[df.query("user == 'userOracle' & framework == 'perm'").index[0]]["Answers"] = A_o_f_perm
    df.iloc[df.query("user == 'userOracle' & framework == 'term'").index[0]]["Answers"] = A_o_f_term
    
    df.iloc[df.query("user == 'userRandom' & framework == 'bool'").index[0]]["Q_difficulty"] = QD_r_f_bool
    df.iloc[df.query("user == 'userRandom' & framework == 'gree'").index[0]]["Q_difficulty"] = QD_r_f_gree
    df.iloc[df.query("user == 'userRandom' & framework == 'perm'").index[0]]["Q_difficulty"] = QD_r_f_perm
    df.iloc[df.query("user == 'userRandom' & framework == 'term'").index[0]]["Q_difficulty"] = QD_r_f_term
    df.iloc[df.query("user == 'userGreedy' & framework == 'bool'").index[0]]["Q_difficulty"] = QD_g_f_bool
    df.iloc[df.query("user == 'userGreedy' & framework == 'gree'").index[0]]["Q_difficulty"] = QD_g_f_gree
    df.iloc[df.query("user == 'userGreedy' & framework == 'perm'").index[0]]["Q_difficulty"] = QD_g_f_perm
    df.iloc[df.query("user == 'userGreedy' & framework == 'term'").index[0]]["Q_difficulty"] = QD_g_f_term
    df.iloc[df.query("user == 'userOracle' & framework == 'bool'").index[0]]["Q_difficulty"] = QD_o_f_bool
    df.iloc[df.query("user == 'userOracle' & framework == 'gree'").index[0]]["Q_difficulty"] = QD_o_f_gree
    df.iloc[df.query("user == 'userOracle' & framework == 'perm'").index[0]]["Q_difficulty"] = QD_o_f_perm
    df.iloc[df.query("user == 'userOracle' & framework == 'term'").index[0]]["Q_difficulty"] = QD_o_f_term
    
    return df


##### DRAWING 

def draw_G(G, S, **kwds):
  """ Draws a labelled undirected graph with colored violations
  """
  edge_color = ["red" if isViolation(u,v,G,S) else "black" for (u,v) in G.edges]
  nx.draw(G, with_labels=True, labels=dict(G.nodes(data='label')),
          edge_color=edge_color,
          **kwds)
  return

def draw_S(S, **kwds):
  nx.draw(S, with_labels=True, node_color="green", node_shape="s", **kwds)
  return

def drawing_pos(G,S):
  """returns fixed drawing positions for G and S vertices
  """
  pos_G = nx.drawing.layout.kamada_kawai_layout(G)
  pos_S = nx.drawing.layout.kamada_kawai_layout(S)
  return (pos_G, pos_S)

def draw_GS(G,S, pos=None):
  """ draws G and S side to side
  :param G: see draw_G
  :param S: see draw_S
  :param pos: see drawing_pos
  """
  _, (ax1, ax2) = plt.subplots(1,2, figsize=(10,5))
  if(pos==None):
    draw_G(G,S,ax=ax1)
    draw_S(S,ax=ax2)
  else:
    (pos_G, pos_S) = pos
    draw_G(G,S,ax=ax1, pos=pos_G)
    draw_S(S,ax=ax2, pos=pos_S)
  return

##### LABELLED GRAPH

def graph_diff(G1, G2, theta = 0.5):
  """ diff = theta * #relabelings + (1-theta) * #deletions
  Assuming same node set
  :param theta: theta as in cost
  """
  if(G1 == None) or (G2==None):
    return None
  
  dist = 0

  # differing label is a difference
  for n in G1.nodes:
    l = G1.nodes[n]['label']
    h = G2.nodes[n]['label']
    if(l != h):
      dist = dist + theta

  # differing edges is a difference
  for e in G1.edges:
    if e not in G2.edges:
      dist = dist + 1 - theta
  for e in G2.edges:
    if e not in G1.edges:
      dist = dist + 1 - theta

  return dist





import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import string
from math import inf

##### LABELS AND VIOLATIONS

# A list of labels from A0000,...,Z0000,...A9999,...Z9999
alphabet = list(string.ascii_lowercase)
for i in range(1,1000):
  alphabet += [a + str(i) for a in list(string.ascii_lowercase)]


def valid_labels(v, G, S):
  """ The set of labels that respect neighborhood dependencies for v
  :param v: a vertex
  :param G: instance graph
  :param S: constraint set
  :return: a (possibly empty) set of labels
  """

  # neighbor labels
  neighbor_labels = set()
  for n in  G.neighbors(v):
    l = G.nodes[n]['label']
    if(l != None):
      neighbor_labels.add(l)
  
  # possible correct labels
  allowed_labels = set(S.nodes)
  for l in neighbor_labels:
    allowed_labels = allowed_labels.intersection(set(S.neighbors(l)))

  return allowed_labels


def isViolation(u,v, G, S):
  """ Is edge (u,v) a conflict w.r.t. S
  :return: True if (lambda(u), lambda(v)) not in N
  """
  return not ((G.nodes[u]['label'],G.nodes[v]['label']) in S.edges)

def violations(G,S):
  """ Returns the list of edges of G violating S
  :return: List of edges that violate S
  """
  violations = []
  for (u,v) in G.edges:
    if isViolation(u,v,G,S):
      violations.append((u,v))
  return violations

##### GENERATION
def label_v(v, G, S):
  """ Labels vertex v of G w.r.t. constraints S
  :param v: vertex
  :param G: instance graph
  :param S: constraints
  :return: True if the process succeeds
  """
  
  #get set of labels that respects the constraints
  allowed_labels = valid_labels(v,G,S)

  #if no label works, the process failed
  if(len(allowed_labels) == 0):
    return False
  
  G.nodes[v]['label'] = np.random.choice(list(allowed_labels))
  return True

def label_G(G,S):
  """ Labels graph G w.r.t. constraints S.
  Assigns labels randomly amongst valid ones along 
  BFS traversal of connected components with random source
  :param G: instance graph
  :param S: constraints
  :return: True if the process succeeds
  """

  nodes = dict(G.nodes(data='label'))
  while None in nodes.values():
    #   randomly select a vertex without label and label it
    to_label = [ v for (v,l) in nodes.items() if l == None]
    v = np.random.choice(to_label)
    G.nodes[v]['label'] = np.random.choice(S.nodes)

    # BFS assigning correct labels randomly
    for (_,u) in nx.bfs_edges(G, v):
      if(not label_v(u, G, S)):
        return False
    
    #update nodes
    nodes = dict(G.nodes(data='label'))
  
  return G

def generate_GS(v_size = 10, v_density = 1.5, lv_ratio = 0.5, l_density = 1.5, budget = 100):
  """ Generates an instance graph G=(V,E,lambda) and a constraint set S=(L,N)
  :param v_size: |V|, the size of G
  :param v_density: |E|/|V|, the density of G
  :param lv_ratio: |L|/|V|, the relative size of alphabet L to G
  :param l_density: |N|/|L|, the density of S
  :return: G,S, such that G respects S
  """

  # Generate G
  G = nx.Graph()

  V = np.arange(v_size)
  G.add_nodes_from(V)

  E = np.random.choice(V, size=round(v_size* v_density))
  E = [(u, np.random.choice(np.delete(V, u))) for u in E]
  G.add_edges_from(E)

  # Generate S
  S = nx.Graph()

  L = np.arange(round(lv_ratio*v_size))

  N = np.random.choice(L, size=round(len(L) * l_density))
  N = [(u, np.random.choice(np.delete(L, u))) for u in N]

  S.add_nodes_from([alphabet[l] for l in L])
  S.add_edges_from([ (alphabet[u], alphabet[v]) for (u,v) in N])
  # self_edges
  S.add_edges_from([ (alphabet[l], alphabet[l]) for l in L])

  # Label G as to respect S
  for v in G.nodes: 
    G.nodes[v]['label'] = None
  

  H = label_G(G.copy(),S)
  while(not H):
    # print("failed to label, retrying", budget)
    budget = budget - 1
    if(budget==0):
      raise TimeoutError
    H = label_G(G.copy(),S)

  return (H,S)

def inject_violation(v,G,S):
  """ Relabels v to create a violation
  :param v: vertex to relabel
  :param G: instance graph
  :param S: constraint set
  :return: True if the operation succeeds
  """
  
  allowed_labels = valid_labels(v,G,S)
  
  # incorrect labels
  violating_labels = set(S.nodes) - allowed_labels

  if(len(violating_labels) == 0):
    return False
  
  G.nodes[v]['label'] = np.random.choice(list(violating_labels))
  return True

# other version with ratio +- tolerance
def inject_violations(G, S, ratio_low = 0.18, ratio_high = 0.22, budget=100):
  """ Injects violations in G until the share of violations
   is in the given interval
  :param ratio_low: lower bound for |violations| / |E|
  :param ratio_high: upper bound for |violations| / |E|
  :param G: instance graph
  :param S: constraint set
  :return: True if the operation succeeds
  """
  
  while len(violations(G,S)) < len(G.edges) * ratio_low:
    n = np.random.choice(G.nodes)
    if(inject_violation(n, G, S) == False):
      budget = budget - 1
      if(budget==0):
        return False
    
  if(len(violations(G,S)) > len(G.edges) * ratio_high):
    return False
  
  return True

def force_inject_violations(G, S,
                            ratio_low = 0.15, ratio_high = 0.20,
                            budget = 1000, tries=10):
  """ Tries to inject_violations until succesful or budget is spent
  See inject_violations for more details
  :return: Modified G
  """
  # use a copy
  H = G.copy()

  while(not(inject_violations(H, S, ratio_low, ratio_high, budget=budget))):
    # undo injections
    H = G.copy()
    tries = tries - 1
    if tries == 0:
      raise TimeoutError

  return H

def generate_GSG(v_size=20, ratio=0.2):
    """ Generates a ground truth G, a constraint graph S, and H, a noisy version of G
    Note: this is a quick and dirty way to generate a trio. See other methods for more control
    :param v_size: the number of vertices in G and G'
    :param ratio: the noise ratio
    :return: G,S,H three graphs
    """
    G,S = generate_GS(v_size)
    H = force_inject_violations(G,S, ratio_low=ratio, ratio_high = ratio+0.03)
    return G,S,H

##### REPAIRING
def repair(G,S,verbose=False):
  """ Repairs G w.r.t. S by relabeling and deleting edges
  inspired by Neighorhoood constraints repair paper by Song et al
  """

  while len(violations(G,S)) > 0:
    # conflict participation
    conflict_participation = dict(zip(list(G.nodes), [0]*len(G.nodes)))
    all_violations = violations(G,S)
    for (u,v) in violations(G,S):
      conflict_participation[u] += 1
      conflict_participation[v] += 1
    # argmax with dict key
    candidates = [k for k,v in conflict_participation.items() if v == max(conflict_participation.values())]
    v = np.random.choice(candidates)

    allowed_labels = valid_labels(v, G, S)
    # deletion repair
    if(len(allowed_labels) == 0):
      for (x,y) in violations(G,S):
        if(x == v or y == v):
          G.remove_edge(x,y)
          if(verbose): 
            print("removing ", (x,y))
    # greedy relabelling repair
    else:
      best = G.nodes[v]['label']
      best_perf = len(violations(G,S))
      for l in allowed_labels:
        H = G.copy()
        H.nodes[v]['label'] = l
        perf = len(violations(H,S))
        if perf < best_perf:
          best = l
          best_perf = perf

      if(verbose):
        print("relabelling ", G.nodes[v]['label'], "-->", best)
      G.nodes[v]['label'] = best
  
  return G


def UserRepairWithMetadata(G,S, user, selectConflict, answers, apply, steps=1000, verbose=False):
  """ Repairs the graph G w.r.t. the constraints S by asking questions to the user using the framework
  Note: For framework definitions, see below
  :param G: Instance graph to be repaired
  :param S: Constraint graph
  :param user: a function with signature user(question, allowed answers, G, S) = answer
  :param selectConflict: a function that returns the question selected by the framework
  :param answers: a function that returns the set of allowed answers by the framework
  :param apply: a function to apply the answer to the graph
  :param steps: the maxium number of questions asked before throwing an error
  :return: the repaired graph G, the list of answers, the list of question complexities (a,b)
  """

  answer_trace = []
  question_cost = []
  while len(violations(G,S))>0:
    
    conflict = selectConflict(G,S)
    
    allowed_answers = answers(conflict, G, S)
    
    answer = user(conflict, allowed_answers, G, S)
    
    apply(conflict, answer, G, S)

    # trace
    answer_trace.append(answer)
    if(verbose):
      print("answer :", answer)
    
    #question cost
    question_cost.append(question_difficulty(conflict,allowed_answers,G))
    
    # force termination
    steps -= 1
    if(steps == 0):
      return None, answer_trace, question_cost

  return G, answer_trace, question_cost


def UserRepair(G,S, user, selectConflict, answers, apply, steps=1000, verbose=False):
  """ Like UserRepairWithMetadata, but without the metadata
  """ 
  print("UserRepair")
  return UserRepairWithMetadata(G,S,user, selectConflict, answers, apply, steps, verbose)[0]

##### QUESTION DIFFICULTY
def question_difficulty(conflict, allowed_answers, G):
    """ returns (a,b,c) to compute complexity(q) = alpha*a + beta*b
    :param conflict: the conflict formulation
    :param allowed_answers: the set of allowed answers
    :param G: the instance graph
    :return: a tuple of the components of question complexity
    """
    a = conflict_representation(conflict,G)
    b = len(allowed_answers)
    return (a,b)

def conflict_representation(conflict,G):
    """ returns the number of vertices needed to represent the conflict
    """
    #if question includes a possible repair
    if type(conflict[0]) is tuple:
        return 4
    else:
        return 2

##### INTERACTION MODELS

### F Boolean
### The framework greedily asks for a possible repair, the user answers yes or no
def selectConflictPossibleRepair(G,S):
  """ Select a possible repair for a greedily selected conflict
  """

  conflict = selectConflictGreedy(G,S)
  repairs = answersRepair(conflict, G, S)

  return (conflict, repairs[np.random.choice(len(repairs))])

def answersBoolean(conflict, G, S):
  return ["yes", "no"]

def applyBoolean(conflict, answer, G, S):
  """ If answer is "yes", apply the proposed repair 
  """
  if(answer == "yes"):
    # unpack the "conflict = (edge, proposed repair)"
    (edge, repair) = conflict
    if(repair == "delete"):
      G.remove_edge(*edge)
    else:
      (u,l) = repair
      G.nodes[u]['label'] = l
      G.nodes[u]['modified'] = True
  else:
    #answer is no, don't do anything
    pass
  return

f_bool = (selectConflictPossibleRepair, answersBoolean, applyBoolean)

### Fgreedy
### asks to repair a greedily selected conflict, user answers a possible repair

def selectConflictGreedy(G,S):
  """ Greedily select a conflict (u,v)
  """

  conflict_participation = dict(zip(list(G.nodes), [0]*len(G.nodes)))
  all_violations = violations(G,S)
  for (u,v) in all_violations:
    conflict_participation[u] += 1
    conflict_participation[v] += 1
  v = max(conflict_participation, key=conflict_participation.get)

  possible_e = [(u,w) for (u,w) in all_violations if((u == v) or (w==v))]

  return possible_e[np.random.choice(len(possible_e))]

def answersRepair(conflict, G, S):
  """ all valid repairs for conflict (u,v), 
  i.e. relabeling repairs for u or v, or delete the edge
  """
  (u,v) = conflict
  repairs = [(u,l) for l in valid_labels(u, G.subgraph([u,v]), S)] + \
            [(v,l) for l in valid_labels(v, G.subgraph([u,v]), S)] + \
            [ "delete"]
  return repairs

def applyTransformation(conflict, answer, G, S):
  if(answer == "delete"):
    G.remove_edge(*conflict)
  else:
    (u,l) = answer
    G.nodes[u]['label'] = l
    G.nodes[u]['modified'] = True
  return

f_gree = (selectConflictGreedy, answersRepair, applyTransformation)

### Fpermissive
### asks for a greedily selected conflict, the user answers any graph transformation

def answersTransformation(conflict, G, S):
  """ Any transformation on (u,v), 
  i.e. any relabeling of u or v, or delete the edge
  """
  (u,v) = conflict
  transformations = [(u,l) for l in S.nodes] + \
                    [(v,l) for l in S.nodes] + \
                    [ "delete"]
  return transformations

f_perm = (selectConflictGreedy, answersTransformation, applyTransformation)

### Fterminate
### Like Fgreedy, but only answers that decrease the total number of violations are allowed

def answersDecrease(conflict, G, S):
    """ Any transformation on (u,v) that reduces the number of conflicts in G wrt S, 
    """
    repairs = answersRepair(conflict, G, S)
    subgraph = G.subgraph(conflict_neighborhood(conflict, G))
    decreasing_repairs = []
    for r in repairs:
        modified = subgraph.copy()
        applyTransformation(conflict, r, modified, S)
        if len(violations(subgraph, S)) > len(violations(modified, S)):
            decreasing_repairs.append(r)
    return decreasing_repairs

f_term = (selectConflictGreedy, answersDecrease, applyTransformation)

### utilitaries
def conflict_neighborhood(conflict, G):
  """ returns only the subgraph around the conflict
  """

  if type(conflict[0]) is tuple:
        conflict = conflict[0]
  context = set(conflict)
  for u in conflict:
    for n in nx.neighbors(G, u):
      context.add(n)
  return context

##### USER SIMULATION

### Random
def userRandom(conflict, answers, G, S):
  """ Randomly selects amongst the answers
  """
  return answers[np.random.choice(len(answers))]

### Greedy
def userGreedy_(conflict, answers, G, S, apply):
  """ Tries all possible answers, selects the best in terms of remaining violations
  Note: needs to know the apply function to try the answers.
  See below for a version with classic apply function
  """
  # work on subgraph of interest
  context = conflict_neighborhood(conflict, G)
  sub_G = G.subgraph(context)
            
  # test all answers
  best = None
  best_perf = len(violations(sub_G,S))
  for a in answers:
    H = sub_G.copy()
    apply(conflict, a, H, S)
    current_perf = len(violations(H,S))
    if(current_perf < best_perf):
        best = a
        best_perf = current_perf

  return best if (best != None) else "delete"

def userGreedyCustomApplication(apply):
  return lambda conflict, answers, G, S: userGreedy_(conflict, answers, G, S, apply)

userGreedy = userGreedyCustomApplication(applyTransformation)
  
### Oracle

def userOracle_(conflict, answers, G, S, apply, G_opt):
  """ Tries all answers, selects the one ending closest to optimal G_opt
  Note: needs to know the apply function to try the answers, and the opt
  See below for a version with classic apply function
  """
  # work on subgraph of interest
  context = conflict_neighborhood(conflict, G)
  sub_G = G.subgraph(context)
  sub_G_opt = G_opt.subgraph(context)

  # test all answers
  best = None
  best_perf = inf

  for a in answers:
    H = sub_G.copy()
    apply(conflict, a, H, S)
    # performance is distance to searched graph
    current_perf = graph_diff(H, sub_G_opt)
    if(current_perf < best_perf):
        best = a
        best_perf = current_perf

  return best

def userOracle(G_opt, apply):
  return lambda conflict, answers, G, S: userOracle_(conflict, answers, G, S, apply, G_opt)

##### Generating repairs

def generate_all_repairs(G_opt, S, G, R, steps=1000):
    """ Generates a dataframe with repairs for every combination of framework and user
    :param G_opt: ground truth
    :param S: constraints
    :param G: instance graph
    :param R: result of automatic repair
    :return: a df with columns (G, S, G_opt, R, G', Answers, framework, user)
    """
    
    
    # make an empty dataframe
    df = pd.DataFrame(columns=["G", "S", "G_opt", "R", "G'", "Answers", "Q_difficulty", "framework", "user"])

    for u in ["userRandom", "userGreedy", "userOracle"]:
        for f in ["gree", "perm", "term"]:
            df = df.append(dict(zip(df.columns, [G,S,G_opt,R, None, None, None, f, u])), ignore_index=True)

    # repair the graph with all framework / user combination
    #G_r_f_bool, A_r_f_bool, QD_r_f_bool = UserRepairWithMetadata(G.copy(),S,userRandom, *f_bool, steps=steps)
    G_r_f_gree, A_r_f_gree, QD_r_f_gree = UserRepairWithMetadata(G.copy(),S,userRandom, *f_gree, steps=steps)
    G_r_f_perm, A_r_f_perm, QD_r_f_perm = UserRepairWithMetadata(G.copy(),S,userRandom, *f_perm, steps=steps)
    G_r_f_term, A_r_f_term, QD_r_f_term = UserRepairWithMetadata(G.copy(),S,userRandom, *f_term, steps=steps)
    #G_g_f_bool, A_g_f_bool, QD_g_f_bool = UserRepairWithMetadata(G.copy(),S,userGreedyCustomApplication(applyBoolean), *f_bool, steps=steps)
    G_g_f_gree, A_g_f_gree, QD_g_f_gree = UserRepairWithMetadata(G.copy(),S,userGreedy,                                *f_gree, steps=steps)
    G_g_f_perm, A_g_f_perm, QD_g_f_perm = UserRepairWithMetadata(G.copy(),S,userGreedy,                                *f_perm, steps=steps)
    G_g_f_term, A_g_f_term, QD_g_f_term = UserRepairWithMetadata(G.copy(),S,userGreedy,                                *f_term, steps=steps)
    #G_o_f_bool, A_o_f_bool, QD_o_f_bool = UserRepairWithMetadata(G.copy(),S,userOracle(G_opt, applyBoolean),        *f_bool, steps=steps)
    G_o_f_gree, A_o_f_gree, QD_o_f_gree = UserRepairWithMetadata(G.copy(),S,userOracle(G_opt, applyTransformation), *f_gree, steps=steps)
    G_o_f_perm, A_o_f_perm, QD_o_f_perm = UserRepairWithMetadata(G.copy(),S,userOracle(G_opt, applyTransformation), *f_perm, steps=steps)
    G_o_f_term, A_o_f_term, QD_o_f_term = UserRepairWithMetadata(G.copy(),S,userOracle(G_opt, applyTransformation), *f_term, steps=steps)


    # populate the df
    # NOTE make use of column selection to edit here
    #df.iloc[df.query("user == 'userRandom' & framework == 'bool'").index[0]]["G'"] = G_r_f_bool
    df.iloc[df.query("user == 'userRandom' & framework == 'gree'").index[0]]["G'"] = G_r_f_gree
    df.iloc[df.query("user == 'userRandom' & framework == 'perm'").index[0]]["G'"] = G_r_f_perm
    df.iloc[df.query("user == 'userRandom' & framework == 'term'").index[0]]["G'"] = G_g_f_term
    #df.iloc[df.query("user == 'userGreedy' & framework == 'bool'").index[0]]["G'"] = G_g_f_bool
    df.iloc[df.query("user == 'userGreedy' & framework == 'gree'").index[0]]["G'"] = G_g_f_gree
    df.iloc[df.query("user == 'userGreedy' & framework == 'perm'").index[0]]["G'"] = G_g_f_perm
    df.iloc[df.query("user == 'userGreedy' & framework == 'term'").index[0]]["G'"] = G_g_f_term
    #df.iloc[df.query("user == 'userOracle' & framework == 'bool'").index[0]]["G'"] = G_o_f_bool
    df.iloc[df.query("user == 'userOracle' & framework == 'gree'").index[0]]["G'"] = G_o_f_gree
    df.iloc[df.query("user == 'userOracle' & framework == 'perm'").index[0]]["G'"] = G_o_f_perm
    df.iloc[df.query("user == 'userOracle' & framework == 'term'").index[0]]["G'"] = G_o_f_term
    
    #df.iloc[df.query("user == 'userRandom' & framework == 'bool'").index[0]]["Answers"] = A_r_f_bool
    df.iloc[df.query("user == 'userRandom' & framework == 'gree'").index[0]]["Answers"] = A_r_f_gree
    df.iloc[df.query("user == 'userRandom' & framework == 'perm'").index[0]]["Answers"] = A_r_f_perm
    df.iloc[df.query("user == 'userRandom' & framework == 'term'").index[0]]["Answers"] = A_r_f_term
    #df.iloc[df.query("user == 'userGreedy' & framework == 'bool'").index[0]]["Answers"] = A_g_f_bool
    df.iloc[df.query("user == 'userGreedy' & framework == 'gree'").index[0]]["Answers"] = A_g_f_gree
    df.iloc[df.query("user == 'userGreedy' & framework == 'perm'").index[0]]["Answers"] = A_g_f_perm
    df.iloc[df.query("user == 'userGreedy' & framework == 'term'").index[0]]["Answers"] = A_g_f_term
    #df.iloc[df.query("user == 'userOracle' & framework == 'bool'").index[0]]["Answers"] = A_o_f_bool
    df.iloc[df.query("user == 'userOracle' & framework == 'gree'").index[0]]["Answers"] = A_o_f_gree
    df.iloc[df.query("user == 'userOracle' & framework == 'perm'").index[0]]["Answers"] = A_o_f_perm
    df.iloc[df.query("user == 'userOracle' & framework == 'term'").index[0]]["Answers"] = A_o_f_term
    
    #df.iloc[df.query("user == 'userRandom' & framework == 'bool'").index[0]]["Q_difficulty"] = QD_r_f_bool
    df.iloc[df.query("user == 'userRandom' & framework == 'gree'").index[0]]["Q_difficulty"] = QD_r_f_gree
    df.iloc[df.query("user == 'userRandom' & framework == 'perm'").index[0]]["Q_difficulty"] = QD_r_f_perm
    df.iloc[df.query("user == 'userRandom' & framework == 'term'").index[0]]["Q_difficulty"] = QD_r_f_term
    #df.iloc[df.query("user == 'userGreedy' & framework == 'bool'").index[0]]["Q_difficulty"] = QD_g_f_bool
    df.iloc[df.query("user == 'userGreedy' & framework == 'gree'").index[0]]["Q_difficulty"] = QD_g_f_gree
    df.iloc[df.query("user == 'userGreedy' & framework == 'perm'").index[0]]["Q_difficulty"] = QD_g_f_perm
    df.iloc[df.query("user == 'userGreedy' & framework == 'term'").index[0]]["Q_difficulty"] = QD_g_f_term
    #df.iloc[df.query("user == 'userOracle' & framework == 'bool'").index[0]]["Q_difficulty"] = QD_o_f_bool
    df.iloc[df.query("user == 'userOracle' & framework == 'gree'").index[0]]["Q_difficulty"] = QD_o_f_gree
    df.iloc[df.query("user == 'userOracle' & framework == 'perm'").index[0]]["Q_difficulty"] = QD_o_f_perm
    df.iloc[df.query("user == 'userOracle' & framework == 'term'").index[0]]["Q_difficulty"] = QD_o_f_term
    
    return df


##### DRAWING 

def draw_G(G, S, **kwds):
  """ Draws a labelled undirected graph with colored violations
  """
  edge_color = ["red" if isViolation(u,v,G,S) else "black" for (u,v) in G.edges]
  nx.draw(G, with_labels=True, labels=dict(G.nodes(data='label')),
          edge_color=edge_color,
          **kwds)
  return

def draw_S(S, **kwds):
  nx.draw(S, with_labels=True, node_color="green", node_shape="s", **kwds)
  return

def drawing_pos(G,S):
  """returns fixed drawing positions for G and S vertices
  """
  pos_G = nx.drawing.layout.kamada_kawai_layout(G)
  pos_S = nx.drawing.layout.kamada_kawai_layout(S)
  return (pos_G, pos_S)

def draw_GS(G,S, pos=None):
  """ draws G and S side to side
  :param G: see draw_G
  :param S: see draw_S
  :param pos: see drawing_pos
  """
  _, (ax1, ax2) = plt.subplots(1,2, figsize=(10,5))
  if(pos==None):
    draw_G(G,S,ax=ax1)
    draw_S(S,ax=ax2)
  else:
    (pos_G, pos_S) = pos
    draw_G(G,S,ax=ax1, pos=pos_G)
    draw_S(S,ax=ax2, pos=pos_S)
  return

##### LABELLED GRAPH

def graph_diff(G1, G2, theta = 0.5):
  """ diff = theta * #relabelings + (1-theta) * #deletions
  Assuming same node set
  :param theta: theta as in cost
  """
  if(G1 == None) or (G2==None):
    return None
  
  dist = 0

  # differing label is a difference
  for n in G1.nodes:
    l = G1.nodes[n]['label']
    h = G2.nodes[n]['label']
    if(l != h):
      dist = dist + theta

  # differing edges is a difference
  for e in G1.edges:
    if e not in G2.edges:
      dist = dist + 1 - theta
  for e in G2.edges:
    if e not in G1.edges:
      dist = dist + 1 - theta

  return dist





