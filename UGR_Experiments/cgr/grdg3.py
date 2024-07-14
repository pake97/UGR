import igraph as ig
from matplotlib.figure import Figure
import numpy as np
from copy import deepcopy
class GRDG:
    def __init__(self,SEED, assignement):
        self.original_graph = None
        self.graph = ig.Graph()
        self.lookup_vertex = {}
        self.lookup_hypervertex = {}
        self.lookup_nodes = {}
        self.nodes_by_betweenness=[]
        self.node_counter = 0
        self.nodes=[]
        np.random.seed(SEED)
        self.assignement = assignement


    """     def build(self, violations):
        
        for violation in violations:
            self.add_hypervertex(violation)
        
        self.compute_betweenness()
        self.original_graph = deepcopy(self.graph) """

    def build(self, violations,edges):
        
        for violation in violations:
            self.add_hypervertex2(violation)

        for edge in edges:
            self.add_edge(edge)
        self.compute_betweenness()
        self.original_graph = deepcopy(self.graph)    
    
    def restore(self):
        
        self.reset()
        self.graph = deepcopy(self.original_graph)
        


    def reset(self):
        self.node_counter = 0
        del self.graph
        del self.lookup_vertex
        del self.lookup_hypervertex
        del self.nodes_by_betweenness
        del self.lookup_nodes
        self.lookup_vertex = {}
        self.lookup_hypervertex = {}
        self.nodes_by_betweenness=[]
        self.lookup_nodes = {}

    def plot(self):
        fig = Figure()
        ax = fig.subplots()
        ig.plot(
            self.graph,
            #vertex_label=[v["name"] for v in self.graph.vs],
            target=ax,
            vertex_size=0.2,
            vertex_color=[self.color_node(v) for v in self.graph.vs],
            edge_width=0.4,
            layout="random",
            edge_curved=0.8,
            edge_color='gray'
        )
        fig.set_size_inches(10, 10)
        
        # Save it to a temporary buffer.
        fig.savefig('plot.png')

    def color_node(self,v):
        if(v["locked"]):
            if(v["selected"]==True):
                return "red"
            else:
                return "lightblue"
        else:
            return "gray"

    def add_hypervertex(self, hypervertex):        
        id1=hypervertex['v1'].element_id.split(":")[-1]
        id2=hypervertex['v2'].element_id.split(":")[-1]
        nodo1=None
        nodo2=None

        if(id1 not in self.nodes):
            nodo1=self.graph.add_vertex(id1)
            properties = {}
            for l, v in hypervertex['v1'].items():
                properties[l] = v 
            self.graph.vs[self.node_counter]["properties"] = properties
            self.node_counter+=1
            self.nodes.append(id1)
        else:
            nodo1=self.graph.vs.find(id1)
            
        if(id2 not in self.nodes):
            nodo2=self.graph.add_vertex(id2)
            properties = {}
            for l, v in hypervertex['v2'].items():
                properties[l] = v 
            self.graph.vs[self.node_counter]["properties"] = properties
            self.node_counter+=1
            self.nodes.append(id2)
        else:
            nodo2=self.graph.vs.find(id2)
            
        if(not self.graph.are_connected(nodo1,nodo2)):
           self.graph.add_edge(nodo1,nodo2)
           
    def add_hypervertex2(self, hypervertex):        
        id1=hypervertex['v1'].element_id.split(":")[-1]
        
        if(id1 not in self.nodes):
            nodo1=self.graph.add_vertex(id1)
            properties = {}
            for l, v in hypervertex['v1'].items():
                properties[l] = v 
            self.graph.vs[self.node_counter]["properties"] = properties
            self.node_counter+=1
            self.nodes.append(id1)
        
    
    def add_node(self, node):
        id1=node['v1'].element_id.split(":")[-1]
        if(id1 not in self.nodes):
            nodo1=self.graph.add_vertex(id1)
            properties = {}
            for l, v in node['v1'].items():
                properties[l] = v 
            self.graph.vs[nodo1.index]["properties"] = properties
            self.node_counter+=1
            self.nodes.append(id1)

    def add_edge(self, hypervertex):
        id1=hypervertex['v1'].element_id.split(":")[-1]
        id2=hypervertex['v2'].element_id.split(":")[-1]
        nodo1 = self.graph.vs.find(id1)
        nodo2 = self.graph.vs.find(id2)
        if(not self.graph.are_connected(nodo1,nodo2)):
           self.graph.add_edge(nodo1,nodo2)

        
    def add_hyperedge(self, hvert2):
        for hvert1 in list(self.lookup_vertex.keys()):
            if(hvert1!=hvert2):
                print(self.lookup_vertex[hvert1]['ids'])
                print(self.lookup_vertex[hvert2]['ids'])
                if(len(self.lookup_vertex[hvert1]['ids'].intersection(self.lookup_vertex[hvert2]['ids']))>0):
                    self.graph.add_edge(hvert1,hvert2)
    
    def print_stats(self):
        
        print(len(list(self.lookup_vertex.keys())))
        print(self.lookup_vertex)
        print(len(list(self.lookup_hypervertex.keys())))
        print(self.lookup_hypervertex)
        print(self.graph.get_adjacency())
        print(self.lookup_nodes)


    def add_hyperedges2(self):
        for nodo in list(self.lookup_nodes.keys()):
            if(len(self.lookup_nodes[nodo])>1):
                nodi = self.lookup_nodes[nodo]
                for i in range(len(nodi)):
                    for j in range(i+1,len(nodi)):    
                        if self.graph.are_connected(int(nodi[i]), int(nodi[j])):
                            continue
                        else:
                            self.graph.add_edge(int(nodi[i]), int(nodi[j]))

    def add_hyperedges(self):
        for hvert1 in list(self.lookup_vertex.keys()):
            for hvert2 in list(self.lookup_vertex.keys()):
                if(hvert1!=hvert2):
                    if(len(set(self.lookup_vertex[hvert1]['ids']).intersection(set(self.lookup_vertex[hvert2]['ids'])))>0):
                        if self.graph.are_connected(hvert1, hvert2):
                            continue
                        else:
                            if(hvert1!=hvert2):
                                self.graph.add_edge(hvert1,hvert2)
    
    def compute_betweenness(self):
        for count,v in enumerate(self.graph.vs()):
            v["locked"]=False
            v["selected"]=False
            if(self.assignement=="betweenness"):
                v["betweenness"]=self.graph.betweenness(v)
        if(self.assignement=="betweenness"):
            self.nodes_by_betweenness=sorted(self.graph.vs, key=lambda v: v['betweenness'])[::-1]
        else:
            self.nodes_by_betweenness=[v for v in self.graph.vs]

    def getViolationToRepairBetweenness(self):
        counter=0
        
        while(True):
            if(counter>=len(self.nodes_by_betweenness)):
                return None
            node = self.nodes_by_betweenness[counter]
            
            if(node["locked"]==True):
                counter+=1
            else:
                neighbors_free=True
                #check if neighbors are not locked
                for v in self.graph.neighbors(self.nodes_by_betweenness[counter]):
                    
                    neighbors_free=neighbors_free and self.graph.vs[v]["locked"]==False
                if(neighbors_free):
                    node["locked"]=True
                    node["selected"]=True
                    for v in self.graph.neighbors(self.nodes_by_betweenness[counter]):
                        
                        self.graph.vs[v]["locked"]=True
                        
                    return node
                else:
                    counter+=1
                

    def getViolationToRepairRandom(self):
        counter=0
        np.random.shuffle(self.nodes_by_betweenness)
        while(True):
            if(counter>=len(self.nodes_by_betweenness)):
                
                return None
            node = self.nodes_by_betweenness[counter]
            if(node["locked"]==True):
                counter+=1
            else:
                neighbors_free=True
                #check if neighbors are not locked
                for v in self.graph.neighbors(self.nodes_by_betweenness[counter]):
                    neighbors_free=neighbors_free and self.graph.vs[v]["locked"]==False
                if(neighbors_free):
                    node["locked"]=True
                    node["selected"]=True
                    for v in self.graph.neighbors(self.nodes_by_betweenness[counter]):
                        
                        self.graph.vs[v]["locked"]=True
                        
                    return node
                else:
                    counter+=1