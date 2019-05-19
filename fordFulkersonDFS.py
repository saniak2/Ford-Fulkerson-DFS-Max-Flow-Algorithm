import pprint

class Edge(object):
    """class definition for an edge"""
    def __init__(self, source, dest, capacity):
        """initialization method for an edge"""
        self.source = source
        self.dest = dest
        self.capacity = capacity

    def __repr__(self):
        """str function for output"""
        return "{src}->{dst}".format(\
                src=self.source, capacity=self.capacity, dst=self.dest)

class FlowGraph(object):
    """class definition for the flow graph"""
    def __init__(self):
        """initialization method for flow graph (residual graph) with flows"""
        self.resid_graph = dict()
        self.all_flows = dict()

    def addVertex(self, vertex):
        """adds a vertex to the flow graph"""
        self.resid_graph[vertex] = []

    def addEdge(self, src, dst, capacity = 0):
        """adds an edge to the flow graph"""
        if src == dst:
            print("invalid edge {} to {}".format(src, dst))
            return
        #creating both the main edge and residual edge
        #main edge e has a forward direction
        #residual edge resid_e has a backward direction with 0 start capacity
        e = Edge(src, dst, capacity)
        resid_e = Edge(dst, src, 0)

        e.resid_e = resid_e
        resid_e.resid_e = e

        #adding the edge (and residual edge) to graph
        self.resid_graph[src].append(e)
        self.resid_graph[dst].append(resid_e)

        #initializing flow values (normal and residual/back flow) to 0
        self.all_flows[e] = 0
        self.all_flows[resid_e] = 0

    def findAugmentingPath(self, source, sink, path):
        """DFS method of finding an augmenting path in the flow graph"""
        #source = sink indicates sink is reached and so the path is returned
        if source == sink:
            return path

        #considers paths with forward and residual/backward edges!
        for e in self.resid_graph[source]:
            #residual capacity is:
            # current edge (residual or not)'s capacity - current edge's flow
            resid_capacity = e.capacity - self.all_flows[e]

            #if the residual (true) capacity > 0 and
            #the current edge of consideration isn't already in the path,
            #add the edge to the path
            if resid_capacity > 0 and (e, resid_capacity) not in path:
                aug_path = self.findAugmentingPath(e.dest, sink,\
                        path + [(e, resid_capacity)])

                #at this point, the augmenting path is realized recursivley
                #if it's not None it is returned
                if aug_path != None:
                    return aug_path

    def fordFulkersonDFS(self, source, sink):
        """Ford Fulkerson method for finding max flow using DFS to find
                augmenting path"""
        augmenting_path = self.findAugmentingPath(source, sink, [])
        print("Initial flow graph:")
        self.print_edges()
        print("\nFord Fulkerson DFS simulation:")
        while augmenting_path != None:
            print("\nAugmenting path: {}".format(augmenting_path))
            print("Edges after augmenting the flows:")
            bottle_neck = min(res_cap for e, res_cap in augmenting_path)
            for e, res_cap in augmenting_path:
                self.all_flows[e] += bottle_neck
                self.all_flows[e.resid_e] -= bottle_neck
            augmenting_path = self.findAugmentingPath(source, sink, [])
            self.print_edges()

        print("\nFinal flow graph:")
        self.print_edges()

        #max flow is = outgoing flow from source
        max_flow = sum(self.all_flows[e] for e in self.resid_graph[source])
        return max_flow

    def print_edges(self):
        for e in self.all_flows:
            print("({}): flow = {}/{}".format(e,self.all_flows[e],\
                    e.capacity))

def obtain_graph():
    g = FlowGraph()
    num_vertices = int(input("enter the number of vertices: "))
    for i in range(num_vertices):
        g.addVertex(input("Enter vertex {}: ".format(i+1)))
    source = input("Enter source vertex: ")
    sink = input("Enter sink vertex: ")

    print("Enter the edges and weights as follows (space delimited):")
    print("   src_vertex dst_vertex flow_capacity")
    print("Enter q to find max flow")
    u_input = input()
    while(u_input != "q"):
        [src, dst, cap] = u_input.split(" ")
        g.addEdge(src, dst, int(cap))
        u_input = input()
    return g

if __name__ == "__main__":
  g = obtain_graph()
  print("max flow: {}".format(g.fordFulkersonDFS('s', 't')))
