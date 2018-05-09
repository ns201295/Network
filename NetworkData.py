import pandas as pd

class NetworkData:
    
    def __init__(self,nodesCSV,edgesCSV):        
        self.nodesDF = pd.read_csv(nodesCSV)
        self.edgesDF = pd.read_csv(edgesCSV)
        
        self.nodes = None
        self.edges = None
        
        self.nodeID_label   = 'id'
        self.edgeFrom_label = 'from'
        self.edgeTo_label   = 'to'
        
        
    def create(self):       
        self.nodesDF = self.nodesDF.set_index(self.nodeID_label)        
        self.edgesDF = self.edgesDF.set_index([self.edgeFrom_label,self.edgeTo_label])
        self.nodes = list(self.nodesDF.index)
        self.edges = list(self.edgesDF.index)
        

    def getNodeAttributes(self):     
        return self.nodesDF.to_dict()
        
    def getEdgeAttributes(self):
        return self.edgesDF.to_dict()
        
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    