class Partition:
    def __init__(self, size):
        self.data = list(range(size))
    
    def sameSetAndUnion(self,i,j):
        rooti = i
        rootj = j
        while rooti != self.data[rooti]:
            rooti = self.data[rooti]
        while rootj != self.data[rootj]:
            rootj = self.data[rootj]
        if rooti != rootj:
            self.data[rooti] = rootj
            return False
        return True

partition = Partition(len(vertDict))
edgeIndex = 0

while len(spanningTree) + 1 < len(vertDict) and edgeIndex < len(edgeList):
    edge = edgeList[edgeIndex]
    if not partition.sameSetAndUnion(edge.v1, edge.v2):
        spanningTree.append(edge)
    edgeIndex += 1
    