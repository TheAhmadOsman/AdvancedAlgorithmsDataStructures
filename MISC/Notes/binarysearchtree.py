class BinarySearchTree:
    # This is a Node class that is internal to the BinarySearchTree class. 
    class Node:
        def __init__(self,val,left=None,right=None):
            self.val = val
            self.left = left
            self.right = right
            
        def getVal(self):
            return self.val
        
        def setVal(self,newval):
            self.val = newval
            
        def getLeft(self):
            return self.left
        
        def getRight(self):
            return self.right
        
        def setLeft(self,newleft):
            self.left = newleft
            
        def setRight(self,newright):
            self.right = newright
            
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
        
    def insert(self,val):
        self.root = BinarySearchTree.__insert(self.root,val)
        
    def __insert(root,val):
        if root == None:
            return BinarySearchTree.Node(val)
        
        if val < root.getVal():
            root.setLeft(BinarySearchTree.__insert(root.getLeft(),val))
        else:
            root.setRight(BinarySearchTree.__insert(root.getRight(),val))
            
        return root
        
    def __iter__(self):
        if self.root != None:
            return iter(self.root)
        else:
            return iter([])

    def __str__(self):
        return "BinarySearchTree(" + repr(self.root) + ")"

    def __repr__(self):
        return "BinarySearchTree(" + repr(self.root) + ")"
 
def main():
    t = BinarySearchTree()
    t.insert(10)
    t.insert(17)
    t.insert(1)
    t.insert(7)
    t.insert(14)

    print(t)

    r = BinarySearchTree(BinarySearchTree.Node(10,BinarySearchTree.Node(1,None,BinarySearchTree.Node(7,None,None)),BinarySearchTree.Node(17,BinarySearchTree.Node(14,None,None),None)))
    
    print(r.lookup(14))

    # s = input("Enter a list of numbers: ")
    # lst = s.split()
    
    # tree = BinarySearchTree()
    
    # for x in lst:
    #     tree.insert(float(x))
        
    # for x in tree:
    #     print(x)

if __name__ == "__main__":
    main()