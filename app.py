from NetworkData import NetworkData
from Network import Network
from NetworkToVisConverter import NetworkToVisConverter

from flask import Flask, render_template, request

app = Flask(__name__)

nodesCSV = 'data/nodes.csv'
edgesCSV = 'data/edges.csv'


netData = NetworkData(nodesCSV,edgesCSV)
netData.create()

net = Network()
net.add_nodes_from(netData.nodes)
net.add_edges_from(netData.edges)

net.setNodeAttributes(netData.getNodeAttributes())

conv = NetworkToVisConverter(net)
conv.nodeColorAttribute = 'type'
conv.nodeColorMap = {'Tag':'red','Entity':'yellow','Category':'blue'}

n,e =conv.getJSON()


# index page route
@app.route('/',methods=['GET'])
def home():
    data = {}
    data['nodes'] = net.nodes()
    degree = 1
    
    # gets the operation type from radio button
    operation = request.args.get('operation')
    data['selectedOperation'] = operation
    
    if operation == 'nodeView':   
            
        if 'degree' in request.args.keys():
            degree = int(request.args.get('degree'))
        else: degree = 1 # defalut degree
        
        node   = request.args.get('node')
        
        # fetches the subgraph for the provided node with all neighbors of given degree 
        sub = net.nodeView(node,degree)
        
        # JSON for rendering of network
        subconv = NetworkToVisConverter(sub)
        data['nodesJSON'],data['edgesJSON'] = subconv.getJSON()

        # creates data for persistence
        data['selectedNode']   = net.nodes()
        data['selectedDegree'] = degree

        return render_template('home.htm', data=data)
                      
            
    if operation == 'findPath':
        
        # fetches number of hops
        if 'hops' in request.args.keys():
            hops = int(request.args.get('hops'))
            if hops == -1:
                hops = None
        else: hops = None  # None -- any number of hops
        
        source = request.args.get('source')
        target = request.args.get('target')
        
        # fetches the subgraph for the given source and target
        sub = net.path(source, target, hops)
        
        # JSON for rendering of network
        subconv = NetworkToVisConverter(sub)
        data['nodesJSON'], data['edgesJSON'] = subconv.getJSON()

         # creates data for persistence
        data['selectedSource']  = source
        data['selectedTarget']  = target        
        data['selectedHops']    = hops

        return render_template('home.htm', data=data)

    # Full Graph Mode -- Site initial landing page
            
    data['nodesJSON'],data['edgesJSON'] = n,e
    return render_template('home.htm', data=data)
  
@app.route('/test',methods=['GET'])
def test():
    return str(request.args.get('coordinates')) + '\n\n' + str(request.args.get('clickedNode'))
    
    
if __name__ == '__main__':
    app.run(port=80,debug=True)
    