import pandas as pd

class NetworkToVisConverter:
    
    def __init__(self, net):
        self.net = net
        self.nodeColorMap = None
        self.labelAttribute = 'label'
        self.nodeColorAttribute = None
        self.defaultNodeColor = 'yellow'

    def getJSON(self):
        
        nodes = self.net.nodes()
        
        if self.nodeColorAttribute:
            if self.nodeColorMap:
                nodes = pd.DataFrame({'id':nodes,'label':list(self.net.getNodeAttributes(self.labelAttribute).values()),'color':list(self.net.getNodeAttributes(self.nodeColorAttribute).values())})
                nodes['color'] = nodes['color'].replace(self.nodeColorMap)
            else:
                nodes = pd.DataFrame({'id':nodes,'label':list(self.net.getNodeAttributes(self.labelAttribute).values()),'color':self.net.colorGenerator(self.nodeColorAttribute)})
        else:
            nodes = pd.DataFrame({'id':nodes,'label':list(self.net.getNodeAttributes(self.labelAttribute).values())})
            #nodes['color'] = self.defaultNodeColor

        nodesJSON = nodes.to_json(orient='records')
        
        edges = pd.DataFrame(list(self.net.edges()),columns=['from','to'])
        edgesJSON = edges.to_json(orient='records')
        
        return nodesJSON, edgesJSON

