# Ahmad M. Osman - Dr. Kent Lee, CS 360

import random


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

class AVLNode:
   def __init__(self, item, balance = 0, left=None, right=None):
      self.item = item
      self.left = left
      self.right = right
      self.balance = balance
      
   def __str__(self):
      '''  This performs an inorder traversal of the tree rooted at self, 
         using recursion.  Return the corresponding string.
      '''
      st = str(self.item) + ' ' + str(self.balance) + '\n'
      if self.left != None:
         st = str(self.left) +  st  # A recursive call: str(self.left)
      if self.right != None:
         st = st + str(self.right)  # Another recursive call
      return st

   def __repr__(self):
      return "AVLNode("+repr(self.item)+", balance="+ \
            repr(self.balance)+", left="+repr(self.left)+ \
            ", right="+repr(self.right)+")"
 
   def depth(self):
       if self.left == None and self.right == None:
           return 1
       elif self.left == None:
           return self.right.depth() + 1
       elif self.right == None:
           return self.left.depth() +1
       else:
           return 1 + max(self.left.depth(), self.right.depth())

   def rotateLeft(self):
      '''  Perform a left rotation of the subtree rooted at the
       receiver.  Answer the root node of the new subtree.  
      '''
      child = self.right
      if (child == None):
         print( 'Error!  No right child in rotateLeft.' )
         return None  # redundant
      else:
         self.right = child.left
         child.left = self
         return child

   def rotateRight(self):
      '''  Perform a right rotation of the subtree rooted at the
       receiver.  Answer the root node of the new subtree.  
      '''
      child = self.left
      if (child == None):
         print( 'Error!  No left child in rotateRight.' )
         return None  # redundant
      else:
         self.left = child.right
         child.right = self
         return child

   def rotateRightThenLeft(self):
      '''Perform a double inside left rotation at the receiver.  We
       assume the receiver has a right child (the bad child), which has a left 
       child. We rotate right at the bad child then rotate left at the pivot 
       node, self. Answer the root node of the new subtree.  We call this 
       case 3, subcase 2.
      '''
      self.right = self.right.rotateRight()
      return self.rotateLeft()

      
   def rotateLeftThenRight(self):
      '''Perform a double inside right rotation at the receiver.  We
       assume the receiver has a left child (the bad child) which has a right 
       child. We rotate left at the bad child, then rotate right at 
       the pivot, self.  Answer the root node of the new subtree. We call this 
       case 3, subcase 2.
      '''
      self.left = self.left.rotateLeft()
      return self.rotateRight()

   
class AVLTree:
   def __init__(self):
      self.root = None
      self.count = 0
      
   def __str__(self):
      st = 'There are ' + str(self.count) + ' nodes in the AVL tree.\n'
      return  st + str(self.root)  # Using the string hook for AVL nodes
   
   def __repr__(self):
      return repr(self.root)
   
   def insert(self, newItem):
      '''  Add a new node with item newItem, if there is not a match in the 
        tree.  Perform any rotations necessary to maintain the AVL tree, 
        including any needed updates to the balances of the nodes.  Most of the 
        actual work is done by other methods.
      '''
      self.count += 1
      pivot, pathStack, parent, found = self.search(newItem)

      if parent == None:
         self.root = AVLNode(newItem)

      elif not found:
         if pivot == None:
            if newItem > parent.item:
               parent.right = AVLNode(newItem)
            else:
               parent.left = AVLNode(newItem)
            self.case1(pathStack, pivot, newItem)
         else:
            if newItem > pivot.item:
               insertingDirection = "right"
            else:
                insertingDirection = "left"
            if pivot.balance > 0:
               inbalanceDirection = "right" 
            else:
               inbalanceDirection = "left"

            if newItem > parent.item:
                  parent.right = AVLNode(newItem)
            else:
                  parent.left = AVLNode(newItem)

            if insertingDirection != inbalanceDirection:
                self.case2(pathStack, pivot, newItem)
            else:
                self.case3(pathStack, pivot, newItem)
    
   def adjustBalances(self, theStack, pivot, newItem):
      '''  We adjust the balances of all the nodes in theStack, up to and
         including the pivot node, if any.  Later rotations may cause
         some of the balances to change.
      '''
      pivotAdjusted = False
      while (not theStack.isEmpty()) and (not pivotAdjusted):
         current = theStack.pop()
         
         if newItem > current.item:
            current.balance += 1
         elif newItem < current.item:
            current.balance -= 1
         
         if current == pivot:
            pivotAdjusted = True       
      
   def case1(self, theStack, pivot, newItem):
      '''  There is no pivot node.  Adjust the balances of all the nodes
         in theStack.
      '''
      self.adjustBalances(theStack, pivot, newItem)
            
   def case2(self, theStack, pivot, newItem):
      ''' The pivot node exists.  We have inserted a new node into the
         subtree of the pivot of smaller height.  Hence, we need to adjust 
         the balances of all the nodes in the stack up to and including 
         that of the pivot node.  No rotations are needed.
      '''
      self.adjustBalances(theStack, pivot, newItem)
            
   def case3(self, theStack, pivot, newItem):
      '''  The pivot node exists.  We have inserted a new node into the
         larger height subtree of the pivot node.  Hence rebalancing and 
         rotations are needed.
      '''
      self.adjustBalances(theStack, pivot, newItem)
      if pivot.balance > 0:
        pivotInbalanceDirection = "right" 
      else:
        pivotInbalanceDirection =  "left"
      
      if pivot.balance > 0:
        badChild = pivot.right 
      else: 
        badChild = pivot.left
      
      if badChild.balance > 0:
        badGrandChild = badChild.right
      else:
        badGrandChild = badChild.left

      if badGrandChild.item == newItem:
        badGrandChild = None

      if newItem > badChild.item:
        badChildinsertingDirection = "right"
      else:
        badChildinsertingDirection = "left"
      
      if (not theStack.isEmpty()):
        pivotsParent = theStack.pop()
      else:
        pivotsParent = pivot


      if pivotInbalanceDirection == badChildinsertingDirection:
        if badChildinsertingDirection == "left":
          if pivotsParent == pivot:
            self.root = pivot.rotateRight()
          else:
            if newItem > pivotsParent.item:
              pivotsParent.right = pivot.rotateRight()
            else:
              pivotsParent.left = pivot.rotateRight()
        else:
          if pivotsParent == pivot:
            self.root = pivot.rotateLeft()
          else:
            if newItem > pivotsParent.item:
              pivotsParent.right = pivot.rotateLeft()
            else:
              pivotsParent.left = pivot.rotateLeft()
      
        pivot.balance = 0
        badChild.balance = 0

      else:
        if pivotInbalanceDirection == "left":
          if pivotsParent == pivot:
            self.root = pivot.rotateLeftThenRight()
          else:
            if newItem > pivotsParent.item:
              pivotsParent.right = pivot.rotateLeftThenRight()
            else:
              pivotsParent.left = pivot.rotateLeftThenRight()
        else:
          if pivotsParent == pivot:
            self.root = pivot.rotateRightThenLeft()
          else:
            if newItem > pivotsParent.item:
              pivotsParent.right = pivot.rotateRightThenLeft()
            else:
              pivotsParent.left = pivot.rotateRightThenLeft()

        if badGrandChild == None:
          pivot.balance = 0
          badChild.balance = 0
        else:
          badGrandChild.balance = 0
          if badChildinsertingDirection == "right":
            if newItem < badGrandChild.item:
              badChild.balance = 0
              pivot.balance = 1
            else:
              badChild.balance = -1
              pivot.balance = 0
          else:
            if newItem < badGrandChild.item:
              badChild.balance = 1
              pivot.balance = 0
            else:
              badChild.balance = 0
              pivot.balance = -1
         
   def search(self, newItem):
      '''  The AVL tree is not empty.  We search for newItem. This method will 
        return a tuple: (pivot, theStack, parent, found).  
        In this tuple, if there is a pivot node, we return a reference to it 
        (or None). We create a stack of nodes along the search path -- theStack. 
        We indicate whether or not we found an item which matches newItem.  We 
        also return a reference to the last node the search examined -- referred
        to here as the parent.  (Note that if we find an object, the parent is 
        reference to that matching node.)  If there is no match, parent is a 
        reference to the node used to add a child in insert().
      '''
      pivot, theStack, parent, found = None, Stack(), self.root, False

      if self.count > 0:
        node = self.root
        while node != None and not found:
          if newItem == node.item:
            found = True
          else:
            theStack.push(node)
            parent = node
            if node.balance != 0:
              pivot = node
            if newItem > node.item:
              node = node.right
            else:
              node = node.left

      return pivot, theStack, parent, found
   
   def check(self):
       try:
         lDepth = self.root.left.depth()
       except:
         lDepth = 0
       try:
         rDepth = self.root.right.depth()
       except:
         rDepth = 0
       
       if max(lDepth, rDepth) - min(lDepth, rDepth) > 1:
           raise ValueError("Tree is invalid at right depth:", rDepth, " - left depth:", lDepth)
  
   def __pushLefts(root, theStack):
      while root != None:
        theStack.append(root)
        root = root.left
   
   def __iter__(self):
      nodeStack = []
      root = self.root
      AVLTree.__pushLefts(root, nodeStack)
      while len(nodeStack) > 0:
        top = nodeStack.pop()
        yield top.item
        AVLTree.__pushLefts(top.right, nodeStack)

            
def main():
  #  print("Our names are ")
  #  print()
  #  a = AVLNode(20, -1)
  #  b = AVLNode( 30, -1)
  #  c = AVLNode(-100)
  #  d = AVLNode(290)
  #  '''
  #  print(a)
  #  print(b)
  #  '''
  #  t = AVLTree()
  #  t.root = b
  #  b.left = a
  #  a.left = c
  #  b.right = d
  #  t.count = 4
  #  print(t)
              
  #  a = AVLNode(50)
  #  b = AVLNode(30)
  #  c = AVLNode(40)
  #  a.left = b
  #  b.right = c
  #  print("Testing rotateLeftThenRight()")
  #  print(a.rotateLeftThenRight())
              
  #  (pivot, theStack, parent, found) = t.search(-70)
  #  print(pivot.item, parent.item, found)
  #  print()
  #  print("The items in the nodes of the stack are: ")
  #  while not theStack.isEmpty():
  #     current = theStack.pop()
  #     print(current.item)
  #  print()

  #  (pivot, theStack, parent, found) = t.search(25)
  #  print(pivot.item, parent.item, found)
   
  #  (pivot, theStack, parent, found) = t.search(-100)
  #  print(pivot.item, parent.item, found)

  t = AVLTree()
  
  print("Processing a randomly generated tree of 1000 nodes...")
  vals = set()
  while len(vals) < 1000:
    vals.add(random.randint(1, 1000000))

  for v in vals:
    t.insert(v)
    try:
      t.check()
    except ValueError as ve:
      print("Could not insert value", v, "in tree:")
      print(ve)
      print(repr(t))

  count = 0
  for node in t:
    count += 1
  
  print("Done!")
  print("Number of Elements in AVL tree:", t.count)
  print("Number of Elements counted using __iter__ method:",count)
  if count != t.count:
    raise ValueError("t.count and __iter__ do not agree on the same count!")

  print("\nLet's look at a simpler tree\n")
  
  t = AVLTree()
  vals = [12, 4, 19, 3, 13, 24, 50, 32, 11, 17, 69, 9, 56]

  for v in vals:
    t.insert(v)
    try:
      t.check()
    except ValueError as ve:
      print("Could not insert value", v, "in tree:")
      print(ve)
      print(repr(t))
  
  count = 0
  for node in t:
    count += 1

  print("Number of Elements in AVL tree:", t.count)
  print("Number of Elements counted using __iter__ method:",count)
  print()

  if count != t.count:
    raise ValueError("t.count and __iter__ do not agree on the same count!")

  print(repr(t))
   
if __name__ == '__main__': 
  main()

'''  The output from main():
[evaluate avltree.py]
Our names are
There are 4 nodes in the AVL tree.
-100 0
20 -1
30 -1
290 0

Testing rotateLeftThenRight()
30 0
40 0
50 0

20 -100 False

The items in the nodes of the stack are: 
-100
20
30

20 20 False
20 -100 True
'''
