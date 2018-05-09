import networkx as nx
from random import randint
from util import flatten


import warnings
warnings.filterwarnings("ignore")

class Network(nx.Graph):
    
    def __init__(self):      
        super().__init__()
        self.nodeAttributes = set()
        self.edgeAttributes = set()
                
    def setNodeAttributes(self, attributeDict):
        for att in attributeDict.keys():
            nx.set_node_attributes(self,att,attributeDict[att])
        self.nodeAttributes |= set(attributeDict.keys())
            
    def setEdgeAttributes(self, attributeDict):
        for att in attributeDict.keys():
            nx.set_edge_attributes(self,att,attributeDict[att])
        self.edgeAttributes |= set(attributeDict.keys())
            
    def getNodeAttributes(self,att):
        return nx.get_node_attributes(self,att)
        
    def nodeView(self,node,deg=1):
        nodes = [node]
        for i in range(deg):
            temp = []
            for j in nodes:
                temp += list(nx.all_neighbors(self,j))
            nodes += temp
        sub = self.subgraph(nodes)
        sub.nodeAttributes = self.nodeAttributes
        sub.edgeAttributes = self.edgeAttributes        
        return sub
            
    def path(self,source,target,hops=None):
        if hops:
            nodes = set(flatten(nx.all_simple_paths(self,source,target,hops)))
        else:
            nodes = set(flatten(nx.all_shortest_paths(self,source=source,target=target)))
        sub = self.subgraph(nodes)
        sub.nodeAttributes = self.nodeAttributes
        sub.edgeAttributes = self.edgeAttributes
        return sub
        
    def colorGenerator(self,att='type'):  
        attributes = self.getNodeAttributes(att)
        values = set(attributes.values())      
        colorMap = {}
        for val in values:
            colorMap[val] = '#'+str(randint(100000,999999))           
        color = self.nodes()
        for i,j in enumerate(color):
            color[i] = colorMap[attributes[j]]          
        return color
    
    def draw(self,nodeLabelAttribute=None,nodeTypeAttribute=None):
        if nodeLabelAttribute:
            if nodeTypeAttribute:
                nx.draw(self,with_labels=True,labels=self.getNodeAttributes(nodeLabelAttribute),node_color=self.colorGenerator(nodeTypeAttribute))
            else:
                nx.draw(self,with_labels=True,labels=self.getNodeAttributes(nodeLabelAttribute))
        else:
            if nodeTypeAttribute:
                nx.draw(self,with_labels=True,node_color=self.colorGenerator(nodeTypeAttribute))
            else:
                nx.draw(self,with_labels=True)
            
