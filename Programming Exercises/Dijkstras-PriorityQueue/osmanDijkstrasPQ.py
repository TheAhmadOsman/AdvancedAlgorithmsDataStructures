# Ahmad M. Osman - Dr. Kent Lee, CS 360

from xml.dom import minidom


class Heap:
    '''
    The class Heap provides a generic heap abstract data type.
    The instances of this class can hold objects of any sort that
    understand the relational operators.  It also allows us to create
    heaps with any maximum number of children.
    '''

    DefaultCapacity = 5  # A class variable
    DefaultNumberOfChildren = 2  # Another class variable

    def __init__(self, capacity=DefaultCapacity,
                 largestOnTop=False, numberOfChildren=DefaultNumberOfChildren):
        self.size = 0
        self.capacity = capacity
        self.largestOnTop = largestOnTop
        self.data = [None]*capacity
        self.maxChildren = numberOfChildren

    def __str__(self):
        if self.largestOnTop:
            sortOfHeap = 'largest on top'
        else:
            sortOfHeap = 'smallest on top'
        st = "It is a " + sortOfHeap + " heap:\n"
        st += "The size of the heap is: " + str(self.size) + "\n"
        st += "The capacity of the heap is: " + str(self.capacity) + "\n"
        st += "The elements of the heap are: " + "\n"
        for vertex in self.data:
            st += vertex + "\n"
        return st

    def addToHeap(self, newObject):
        '''If the heap is full, double its current capacity.
           Add the newObject to the heap, maintaining it as a
           heap of the same type.  Answer newObject.
        '''
        if self.size == self.capacity:
            self.data = self.data+([None]*self.capacity)
            self.capacity = self.capacity * 2
        self.data[self.size] = newObject
        newObject.heapIndex = self.size
        self.size += 1
        self.__siftUpFrom(self.size-1)

    def bestChildOf(self, index, lastIndex):
        ''' Answer the index of the "best child" of self.data[index], if it
          exists. If not, answer None.  lastIndex is the index of the last
          object in the heap.  For a largest on top heap, the best child is the
          largest child.  For a smallest on top heap, it is the smallest child
          of the node with the given index.
        '''
        bestChild = None
        childIndex1 = (index * 2) + 1
        childIndex2 = (index * 2) + 2
        if childIndex1 > lastIndex and childIndex2 > lastIndex:
            return None
        elif childIndex1 > lastIndex and not (childIndex2 > lastIndex):
            bestChild = childIndex2
        elif childIndex2 > lastIndex and not (childIndex1 > lastIndex):
            bestChild = childIndex1
        else:
            if self.data[childIndex1].cost <= self.data[childIndex2].cost:
                bestChild = childIndex1
            else:
                bestChild = childIndex2
        return bestChild

    def buildFrom(self, aSequence):
        '''aSequence is an instance of a sequence collection which
            understands the comparison operators. The elements of
            aSequence are copied into the heap and ordered to build
            a heap. '''
        pass

    def removeTop(self):
        '''  If the heap is not empty, remove the top element
          of the heap and adjust the heap accordingly.  Answer the object
          removed.  If the heap is empty, return None.
        '''
        if self.size != 0:
            topVertex = self.data[0]
            replacement = self.data[self.size-1]
            self.data[self.size-1] = None
            topVertex.heapIndex = None
            self.size -= 1
            self.data[0] = replacement
            replacement.heapIndex = 0
            self.siftDownFrom(0)
            return topVertex
        else:  # empty heap
            return None

    def siftDownFrom(self, fromIndex):
        '''fromIndex is the index of an element in the heap.
          Pre: data[fromIndex..size-1] satisfies the heap condition,
          except perhaps for the element self.data[fromIndex].
          Post:  That element is sifted down as far as neccessary to
          maintain the heap structure for data[fromIndex..size-1].
        '''
        return self.__siftDownFromTo(fromIndex, self.size-1)

    def __siftDownFromTo(self, fromIndex, lastIndex):
        '''fromIndex is the index of an element in the heap.
          Pre: data[fromIndex..lastIndex] satisfies the heap condition,
          except perhaps for the element data[fromIndex].
          Post:  That element is sifted down as far as neccessary to
          maintain the heap structure for data[fromIndex..lastIndex].'''
        if not self.largestOnTop:  # smallest on top
            relevantChildIndex = self.bestChildOf(fromIndex, lastIndex)
            while not (relevantChildIndex == None):  # there are children
                if self.data[fromIndex].cost > self.data[relevantChildIndex].cost:
                    temp = self.data[relevantChildIndex]
                    self.data[relevantChildIndex] = self.data[fromIndex]
                    self.data[relevantChildIndex].heapIndex = relevantChildIndex
                    self.data[fromIndex] = temp
                    self.data[fromIndex].heapIndex = fromIndex

                    fromIndex = relevantChildIndex
                    relevantChildIndex = self.bestChildOf(fromIndex, lastIndex)
                else:
                    return

    def siftUpFrom(self, childIndex):
        return self.__siftUpFrom(childIndex)

    def __siftUpFrom(self, childIndex):
        ''' child is the index of a node in the heap.  This method sifts
          that node up as far as necessary to ensure that the path to the root
          satisfies the heap condition. '''
        if not self.largestOnTop:  # smallest on top
            parentIndex = (childIndex-1)//2
            if parentIndex >= 0:
                while parentIndex >= 0 and self.data[childIndex].cost < self.data[parentIndex].cost:
                    temp = self.data[childIndex]
                    self.data[childIndex] = self.data[parentIndex]
                    self.data[childIndex].heapIndex = childIndex
                    self.data[parentIndex] = temp
                    self.data[parentIndex].heapIndex = parentIndex
                    childIndex = parentIndex
                    parentIndex = (childIndex-1)//2

    def levelByLevelString(self):
        ''' Return a string which lists the contents of the heap
           level by level.
        '''
        index = 0  # start at the root node
        maxLevel = \
            math.ceil(math.log(self.size*(self.numberOfChildren - 1) + 1) /
                      math.log(self.numberOfChildren))


class PriorityQueue:
    def __init__(self):
        self.queue = Heap()

    def __str__(self):
        return self.queue.__str__()

    def enqueue(self, vertex):
        self.queue.addToHeap(vertex)

    def dequeue(self):
        return self.queue.removeTop()

    def __len__(self):
        return self.queue.size

    def adjustPriority(self, vertex, priority):
        index = vertex.heapIndex
        vertex.cost = priority
        self.queue.siftUpFrom(index)


class Vertex:
    def __init__(self, vertexId, x, y, label, cost=99999999):
        self.vertexId = vertexId
        self.x = x
        self.y = y
        self.label = label
        self.cost = cost
        self.previous = None
        self.incidentEdges = []

    def setCost(self, cost):
        self.cost = cost

    def addEdge(self, e):
        self.incidentEdges.append(e)

    def getIncidentEdges(self):
        return self.incidentEdges

    def setPrevious(self, previous):
        self.previous = previous

    def __lt__(self, other):
        if type(self) != type(other):
            raise ValueError("Type mismatch!")
        return self.cost < other.cost

    def __gt__(self, other):
        if type(self) != type(other):
            raise ValueError("Type mismatch!")
        return self.cost > other.cost

    def __repr__(self):
        return "Vertex('"+str(self.label)+"',"+str(self.cost)+","+str(self.previous)+")"

    def __eq__(self, other):
        if type(self) != type(other):
            raise Exception('Type mismatch!')
        return self.vertexId == other.vertexId

    def __str__(self):
        return "Vertex: " + "\n  label: " + str(self.label) + ("\n  cost: %1.2f " % self.cost) + "\n  previous: " + str(self.previous)


class Edge:
    def __init__(self, v1, v2, weight=0):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight


def dijkstra(srcVid, vertexDic):

    def adjacent(v, edge):
        if edge.v1 == v.vertexId:
            return vertexDic[edge.v2]
        return vertexDic[edge.v1]

    unvisited = PriorityQueue()
    visited = set()

    for x in vertexDic:
        vertexDic[x].setCost(999999999)

    src = vertexDic[srcVid]
    src.setCost(0)
    src.setPrevious(0)
    unvisited.enqueue(src)

    while len(unvisited) != 0:
        currentVertex = unvisited.dequeue()
        visited.add(currentVertex.vertexId)
        for edge in currentVertex.getIncidentEdges():
            adjacentVertex = adjacent(currentVertex, edge)
            adjacentId = adjacentVertex.vertexId
            if not adjacentId in visited:
                new_cost = currentVertex.cost + edge.weight
                if new_cost < adjacentVertex.cost:
                    adjacentVertex.setCost(new_cost)
                    adjacentVertex.setPrevious(currentVertex.label)
                    unvisited.enqueue(adjacentVertex)


def main():
    xmldoc = minidom.parse("graph.xml")

    graph = xmldoc.getElementsByTagName("Graph")[0]
    vertices = graph.getElementsByTagName(
        "Vertices")[0].getElementsByTagName("Vertex")
    edges = graph.getElementsByTagName("Edges")[0].getElementsByTagName("Edge")

    width = float(graph.attributes["width"].value)
    height = float(graph.attributes["height"].value)

    vertexDict = {}
    sourceVertex = None

    for vertex in vertices:
        vertexId = int(vertex.attributes["vertexId"].value)
        x = float(vertex.attributes["x"].value)
        y = float(vertex.attributes["y"].value)
        label = vertex.attributes["label"].value
        v = Vertex(vertexId, x, y, label)
        if int(label) == 0:
            sourceVertex = v
        vertexDict[vertexId] = v

    edgeList = []

    for edge in edges:
        anEdge = Edge(int(edge.attributes["head"].value), int(
            edge.attributes["tail"].value))
        if "weight" in edge.attributes:
            anEdge.weight = float(edge.attributes["weight"].value)
        edgeList.append(anEdge)
        vertexDict[anEdge.v1].addEdge(anEdge)
        vertexDict[anEdge.v2].addEdge(anEdge)

    dijkstra(sourceVertex.vertexId, vertexDict)

    vertexList = sorted(vertexDict.values(), key=lambda v: int(v.label))

    for v in vertexList:
        print(str(v))


if __name__ == '__main__':
    main()
