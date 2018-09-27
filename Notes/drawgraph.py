#in class we added comparisons on the Edge class, we wrote Partition, and added the spanningTree set/loop
#we also talked very briefly about graphs, weighted graphs, and directed graphs

from xml.dom import minidom
import turtle


class Vertex:
    def __init__(self,vertexId,x,y,label):
        self.vertexId = vertexId
        self.x = x
        self.y = y
        self.label = label
        
        
class Edge:
    def __init__(self,v1,v2,weight=0):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight
        
    def getVertices(self):
        return (self.v1, self.v2)
    
    def __lt__(self, other):
        if type(self) != type(other):
            raise Exception("Cannot compare type {} with type {}.".format(type(self), type(other)))
        if self.weight < other.weight:
            return True
        return False
    
    def __gt__(self, other):
        if type(self) != type(other):
            raise Exception("Cannot compare type {} with type {}.".format(type(self), type(other)))        
        if self.weight > other.weight:
            return True
        return False
    
    def __eq__(self, other):
        if type(self) != type(other):
            raise Exception("Cannot compare type {} with type {}.".format(type(self), type(other)))        
        if self.weight == other.weight:
            return True   
        return False
    
        
class Partition:
    def __init__(self, size):
        # The root of a tree in the partition is identified
        # by the index being the same as the value at that spot
        # in the list called "data"
        self.data = list(range(size))
        
    def sameSetAndJoin(self, i , j):
        while i != self.data[i]:
            i = self.data[i]
        
        while j != self.data[j]:
            j = self.data[j]
            
        sameSet = i == j
        
        if not sameSet:
            self.data[i] = j
            
        return sameSet
        

def main():
    xmldoc = minidom.parse("graph.xml")
    
    graph = xmldoc.getElementsByTagName("Graph")[0]
    vertices = graph.getElementsByTagName("Vertices")[0].getElementsByTagName("Vertex")
    edges = graph.getElementsByTagName("Edges")[0].getElementsByTagName("Edge")
    
    width = float(graph.attributes["width"].value)
    height = float(graph.attributes["height"].value)
    
    t = turtle.Turtle()
    screen = t.getscreen()
    screen.setworldcoordinates(0,height,width,0)
    t.speed(100)
    t.ht()
    vertexDict = {}
    
    for vertex in vertices:
        vertexId = int(vertex.attributes["vertexId"].value)
        x = float(vertex.attributes["x"].value)
        y = float(vertex.attributes["y"].value)
        label = vertex.attributes["label"].value
        v = Vertex(vertexId, x, y, label)
        vertexDict[vertexId] = v
        print("added", label)
        
    edgeList = []
    
    for edge in edges:
        anEdge = Edge(int(edge.attributes["head"].value), int(edge.attributes["tail"].value))
        if "weight" in edge.attributes:       
            anEdge.weight = float(edge.attributes["weight"].value) 
        edgeList.append(anEdge)
        
    edgeList.sort()
    
    #spanningTree = set()
    spanningTree = []
    
    loc = 0   
    
    part = Partition(len(vertexDict))
    
    while len(spanningTree) < len(vertexDict) -1:
        edge = edgeList[loc]
        v1, v2 = edge.getVertices()
        if not part.sameSetAndJoin(v1, v2):
            print("go")
            #spanningTree.add(edge)
            spanningTree.append(edge)

            
    for edge in edgeList:
        x1 = float(vertexDict[edge.v1].x)
        y1 = float(vertexDict[edge.v1].y)
        x2 = float(vertexDict[edge.v2].x)
        y2 = float(vertexDict[edge.v2].y)
        t.penup()
        t.goto(x1,y1)
        t.pendown()
        t.goto(x2,y2)
        if edge.weight != 0:       
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
            t.penup()
            t.goto(x,y)
            if edge in spanningTree:
                print("in the tree")
                t.write(str(edge.weight),color="red",align="center",font=("Arial",12,"normal"))
            else:
                print("not")
                t.write(str(edge.weight),color="green",align="center",font=("Arial",12,"normal"))
                
                      

    
    for vertexId in vertexDict:
        vertex = vertexDict[vertexId]
        x = vertex.x
        y = vertex.y
        t.penup()
        t.goto(x,y-20)
        
        t.pendown()
        t.fillcolor(0.8,1,0.4)
        t.begin_fill()
        t.circle(20)
        t.end_fill()
        t.penup()
        t.goto(x+2,y+11)
        t.write(vertex.label,align="center",font=("Arial",12,"bold"))

        
    screen.exitonclick()
    
if _name_ == "_main_":
    main()
