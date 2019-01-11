# Ahmad M. Osman - Dr. Kent Lee, CS 360

from xml.dom import minidom


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)


class OrderedTreeSet:
    class BinarySearchTree:
        # This is a Node class that is internal to the BinarySearchTree class.
        class Node:
            def __init__(self, val, left=None, right=None):
                self.val = val
                self.left = left
                self.right = right

            def getVal(self):
                return self.val

            def setVal(self, newval):
                self.val = newval

            def getLeft(self):
                return self.left

            def getRight(self):
                return self.right

            def setLeft(self, newleft):
                self.left = newleft

            def setRight(self, newright):
                self.right = newright

            def getLeftmost(self):
                if not self.left:
                    return self
                return self.left.getLeftmost()

            def getRightmost(self):
                if not self.right:
                    return self
                return self.right.getRightmost()

            def deleteLeftmost(self):
                if not self.left.left:
                    self.setLeft(None)
                    return
                return self.right.deleteLeftmost()

            def deleteRightmost(self):
                if not self.right.right:
                    self.setRight(None)
                    return
                return self.right.deleteRightmost()

            # This method deserves a little explanation. It does an inorder traversal
            # of the nodes of the tree yielding all the values. In this way, we get
            # the values in ascending order.
            def __iter__(self):
                if self.left != None:
                    for elem in self.left:
                        yield elem

                yield self.val

                if self.right != None:
                    for elem in self.right:
                        yield elem

            def __repr__(self):
                return "BinarySearchTree.Node(" + repr(self.val) + "," + repr(self.left) + "," + repr(self.right) + ")"

        # Below are the methods of the BinarySearchTree class.
        def __init__(self, root=None):
            self.root = root

        def insert(self, val):
            self.root = OrderedTreeSet.BinarySearchTree.__insert(
                self.root, val)

        def __insert(root, val):
            if root == None:
                return OrderedTreeSet.BinarySearchTree.Node(val)

            if val < root.getVal():
                root.setLeft(OrderedTreeSet.BinarySearchTree.__insert(
                    root.getLeft(), val))
            else:
                root.setRight(OrderedTreeSet.BinarySearchTree.__insert(
                    root.getRight(), val))

            return root

        def delete(self, val):
            self.root = OrderedTreeSet.BinarySearchTree.__delete(
                self.root, val)

        def __delete(root, val):
            if root == None:
                return None

            if val < root.getVal():
                root.setLeft(OrderedTreeSet.BinarySearchTree.__delete(
                    root.getLeft(), val))
            elif val > root.getVal():
                root.setRight(OrderedTreeSet.BinarySearchTree.__delete(
                    root.getRight(), val))
            else:
                if not root.getRight():
                    return root.getLeft()
                elif not root.getLeft():
                    return root.getRight()
                else:
                    leftReplacement = root.getLeft().getRightmost()
                    root.setVal(leftReplacement.getVal())
                    if not root.getLeft().getRight():
                        if root.getLeft().getLeft():
                            root.setLeft(root.getLeft().getLeft())
                        else:
                            root.setLeft(None)
                    else:
                        root.getLeft().deleteRightmost()
            return root

        def dfs(node, val):
            if node == None:
                return []

            if node.getVal() == val:
                return [val]

            path = OrderedTreeSet.BinarySearchTree.dfs(node.getLeft(), val)

            if len(path) == 0:
                pass

        def __iter__(self):
            if self.root == None:
                return
            s = Stack()
            parent = self.root
            s.push(parent)
            while parent.left:
                parent = parent.left
                s.push(parent)
            while not s.isEmpty():
                parent = s.pop()
                yield parent.val
                if parent.right:
                    parent = parent.right
                    s.push(parent)
                    while parent.left:
                        parent = parent.left
                        s.push(parent)

        def __str__(self):
            return "BinarySearchTree(" + repr(self.root) + ")"

    def __init__(self, contents=None):
        self.tree = OrderedTreeSet.BinarySearchTree()
        if contents != None:
            # randomize the list
            indices = list(range(len(contents)))
            random.shuffle(indices)

            for i in range(len(contents)):
                self.tree.insert(contents[indices[i]])

            self.numItems = len(contents)
        else:
            self.numItems = 0

    def __str__(self):
        return str(self.tree)

    def __iter__(self):
        return iter(self.tree)

    # Following are the mutator set methods
    def add(self, item):
        self.tree.insert(item)

    def remove(self, item):
        self.tree.delete(item)

    def discard(self, item):
        self.remove(item)

    def pop(self):
        pass

    def clear(self):
        for item in self:
            if item != None:
                self.discard(item)

    def update(self, other):
        for item in other:
            if item not in self:
                self.add(item)

    def intersection_update(self, other):
        self.tree = self.intersection(other)

    def difference_update(self, other):
        self = self.difference(other)

    def smallest(self):
        node = self.tree.root
        while node.getLeft():
            node = node.getLeft()
        return node.val

    def symmetric_difference_update(self, other):
        pass

    # Following are the accessor methods for the HashSet
    def __len__(self):
        length = 0
        for item in self:
            length += 1
        return length

    def __find(node, val):
        if node == None:
            return False

        if node.getVal() == val:
            return True

        if val > node.getVal():
            return OrderedTreeSet.BinarySearchTree.__find(root.getRight(), val)

        return OrderedTreeSet.BinarySearchTree.__find(root.getLeft(), val)

    def __contains__(self, item):
        for compareItem in self:
            if item == compareItem:
                return True
        return False

    # One extra method for use with the HashMap class. This method is not needed in the
    # HashSet implementation, but it is used by the HashMap implementation.
    def __getitem__(self, item):
        pass

    def not__contains__(self, item):
        for compareItem in self:
            if item == compareItem:
                return False
        return True

    def isdisjoint(self, other):
        pass

    def issubset(self, other):
        for item in self:
            if item not in other:
                return False
        return True

    def issuperset(self, other):
        for item in other:
            if item not in self:
                return False
        return True

    def union(self, other):
        pass

    def intersection(self, other):
        selfCopy = self.copy()
        for item in selfCopy:
            if item not in other:
                selfCopy.discard(item)
        for item in other:
            if item not in selfCopy:
                selfCopy.discard(item)
        return selfCopy

    def difference(self, other):
        selfCopy = self.copy()
        for item in selfCopy:
            if item in other:
                selfCopy.discard(item)
        return selfCopy

    def symmetric_difference(self, other):
        pass

    def copy(self):
        copy = OrderedTreeSet()
        for item in self:
            copy.add(item)
        return copy

    # Operator Definitions
    def __or__(self, other):
        pass

    def __and__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __xor__(self, other):
        pass

    def __ior__(self, other):
        pass

    def __iand__(self, other):
        pass

    def __ixor(self, other):
        pass

    def __le__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __eq__(self, other):
        for item in self:
            if item not in other:
                return False
        for item in other:
            if item not in self:
                return False
        return True


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

    unvisited = OrderedTreeSet()
    visited = OrderedTreeSet()

    for x in vertexDic:
        vertexDic[x].setCost(999999999)

    src = vertexDic[srcVid]
    src.setCost(0)
    src.setPrevious(0)
    unvisited.add(src)

    while len(unvisited) != 0:
        currentVertex = unvisited.smallest()
        visited.add(currentVertex.vertexId)
        unvisited.remove(currentVertex)
        # print(currentVertex)
        for edge in currentVertex.getIncidentEdges():
            adjacentVertex = adjacent(currentVertex, edge)
            adjacentId = adjacentVertex.vertexId
            if adjacentId not in visited:
                # print(adjacentVertex)
                new_cost = currentVertex.cost + edge.weight
                visited.add(adjacentId)
                if new_cost < adjacentVertex.cost:
                    adjacentVertex.setCost(new_cost)
                    adjacentVertex.setPrevious(currentVertex.label)
                    unvisited.add(adjacentVertex)
                    visited.remove(adjacentId)
        # print("-------------------------------")


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
