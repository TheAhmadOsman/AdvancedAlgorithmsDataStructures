class EasyStack:
    def __init__(self):
        self.items = {}
        self.topIndex = 0
    
    def push(self, item):
        self.items[self.topIndex] = item
        self.topIndex += 1

    def pop(self):
        self.topIndex -= 1
        rv = self.items[self.topIndex]
        del self.items[self.topIndex]
        return rv

class Node:
    def __init__(self, val, next):
        self.val = val
        self.next = next
    
class LinkedStack:
    def __init__(self):
        self.head = None
    
    def push(self, item):
        self.head = Node(item,self.head)
    
    def pop(self):
        rv = self.head.val
        self.head = self.head.next
        return rv

class Stack:
    def __init__(self, size=10):
        self.items = [None] * size
        self.topIndex = 0 # Next available spot
        self.capacity = size

    def push(self,item):
        #self._makeroom()
        if len(self.items) == self.topIndex:
            self.items = self.items + ([None] * len(self.items))
            
        self.items[self.topIndex] = item
        self.topIndex += 1
    
    def pop(self):
        #self._makeroom
        half = len(self.items)//2
        if self.topIndex + 10 < half:
            self.items = self.items[0:half]

        self.topIndex -= 1

        return self.items[self.topIndex]

def main():
    s = Stack()
    for i in range(10):
        s.push(i)
    
    for i in range(10):
        print(s.pop())

main()