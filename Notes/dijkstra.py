class VertexCost:
    def __init__(self, vertexId, cost):
        self.vertexId = vertexId
        self.cost = cost

    def __lt__(self, other):
        if type(self) != type(other):
            raise Exception("Unorderable Types")
        return self.cost < other.cost

treeSet.add(VertexCost(svId,0))

#Get small list for the orderedtreeset

#Dijsktra's worst case is O(n) and best is O(log n)

# worst case O(|vertices||edges|)