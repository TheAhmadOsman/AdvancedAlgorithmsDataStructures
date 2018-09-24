class Stack:
    def __init__(self, size=1):
        self.items = [None] * size
        self.numitems = 0
        self.capacity = size

    def isEmpty(self):
        return self.numitems == 0
    
    def peek(self):
        return self.items[self.numitems-1]
    
    def size(self):
        return self.numitems
    
    def push(self, newitem):
        if len(self.items) == self.numitems:
            newlist = [None] * self.numitems * 2
            self.capacity = len(newlist)
            for k in range(len(self.items)):
                newlist[k] = self.items[k]
            
            self.items = newlist
        
        self.items[self.numitems] = newitem
        self.numitems += 1

    def pop(self):
        if self.numitems == 0:
            raise RuntimeError("Empty Stack!")

        if self.numitems == self.capacity//2:
            newlist = [None] * ((self.capacity//2)+1)
            self.capacity = len(newlist)
            for k in range(self.capacity):
                newlist[k] = self.items[k]
            
            self.items = newlist

        self.numitems = self.numitems -1
        return self.items[self.numitems + 1]

s = Stack()

s.push(1)
print(s.peek())
print(s.size())
s.push(2)
s.push(3)
s.push(4)
s.push(5)
s.push(5)
s.push(5)
s.push(5)
s.push(5)
s.push(5)
s.push(5)

print(len(s.items))
s.pop()
s.pop()
s.pop()
s.pop()
print((s.capacity))
s.pop()
s.pop()
s.pop()
s.pop()
s.pop()
print((s.capacity))
s.pop()
s.pop()
print((s.capacity))

#isEmpty, size, peek, pop, push.