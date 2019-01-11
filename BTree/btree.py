'''
  File: btree.py
  Author: Kent D. Lee and Steve Hubbard
  Date: 06/30/2014
  Description: This module provides the BTree class, based on support from
    the BTreeNode class.  The BTreeNode class is also implemented in this
    module. This module is meant to support the recursive implementation of
    insert, lookup, and delete within a BTree.

    The module requires the Queue class in the queue module.

    This program has two main functions, the btreemain function and the main
    function. The btreemain function tests the BTree datatype. The expected
    output is provided in a comment after the function. Once the btreemain
    function runs and produces the proper output, the main function can be
    run to test the BTree with the join functionality.

    The main function either builds a new BTree or reads an existing BTree
    from the index files, Feed.idx and FeedAttribType.idx files. If the idx
    file does not exist, then a new BTree is built and written to the
    corresponding idx file.
'''
import datetime
import os
from copy import deepcopy
import sys
import queue


class BTreeNode:
    '''
      This class will be used by the BTree class.  Much of the functionality of
      BTrees is provided by this class.
    '''

    def __init__(self, degree=1, numberOfKeys=0, items=None, child=None,
                 index=None):
        ''' Create an empty node with the indicated degree'''
        self.degree = degree
        self.numberOfKeys = numberOfKeys
        if items != None:
            self.items = items
        else:
            self.items = [None]*2*degree
        if child != None:
            self.child = child
        else:
            self.child = [None]*(2*degree+1)
        self.index = index

    def __repr__(self):
        ''' This provides a way of writing a BTreeNode that can be
            evaluated to reconstruct the node.
        '''
        return "BTreeNode("+str(len(self.items)//2)+","+str(self.numberOfKeys) + \
            ","+repr(self.items)+","+repr(self.child)+","+str(self.index)+")\n"

    def __str__(self):
        st = 'The contents of the node with index ' + \
             str(self.index) + ':\n'
        for i in range(0, self.numberOfKeys):
            st += '   Index   ' + str(i) + '  >  child: '
            st += str(self.child[i])
            st += '   item: '
            st += str(self.items[i]) + '\n'
        st += '                 child: '
        st += str(self.child[self.numberOfKeys]) + '\n'
        return st

    def insert(self, bTree, item):
        '''
        Insert an item in the node. Return three values as a tuple,
        (left,item,right). If the item fits in the current node, then
        return self as left and None for item and right. Otherwise, return
        two new nodes and the item that will separate the two nodes in the parent.
        '''
        if self.child == [None] * (2 * self.degree + 1):
            if self.isFull():
                return BTreeNode.splitNode(self, bTree, item, None)
            else:
                self.items[self.numberOfKeys] = item
                self.items = sorted(self.items, key=lambda x: (x is None, x))
                self.numberOfKeys += 1
                return self, None, None
        else:
            idx = 0
            finished = False
            while not finished and self.items[idx] < item:
                if self.items[idx] == None or idx == self.getNumberOfKeys()-1:
                    finished = True
                idx += 1

            leftidx, up, rightidx = BTreeNode.insert(
                bTree.nodes[self.getChild(idx)], bTree, item)

            if not self.isFull() and up != None:
                self.items[self.getNumberOfKeys()] = up
                self.items = sorted(self.items, key=lambda x: (x is None, x))

                upidx = self.items.index(up)

                self.child.insert(upidx+1, rightidx)
                self.child.pop()
                self.numberOfKeys += 1
            else:
                if self.isFull() and up != None:
                    return self.splitNode(bTree, up, rightidx)

            return self, None, None

    def splitNode(self, bTree, item, right):
        '''
        This method is given the item to insert into this node and the node
        that is to be to the right of the new item once this node is split.

        Return the indices of the two nodes and a key with the item added to
        one of the new nodes. The item is inserted into one of these two
        nodes and not inserted into its children.
        '''
        lst = self.items + [item]
        lst.sort()

        children = []
        itemidx = lst.index(item)
        children.append(self.child[0])

        n = 1
        for i in range(bTree.degree * 2 + 1):
            if i == itemidx:
                children.append(right)
            else:
                children.append(self.child[n])
                n += 1

        upidx = len(lst) // 2
        up = lst[upidx]

        self.items = lst
        newnum = len(lst[:upidx])
        self.setNumberOfKeys(newnum)

        right = bTree.getFreeNode()
        newnum = len(lst[upidx+1:])
        right.setNumberOfKeys(newnum)

        fromidx = upidx + 1
        toidx = upidx + right.getNumberOfKeys()+1
        n = 0
        for i in range(fromidx, toidx):
            right.items[n] = lst[i]
            n += 1

        leftChildren = children[:len(children)//2]
        for i in range(len(leftChildren)):
            self.child[i] = leftChildren[i]
        rightChildren = children[len(children)//2:]
        for i in range(len(rightChildren)):
            right.child[i] = rightChildren[i]

        self.items = lst[:upidx] + [None] * \
            (bTree.degree * 2 - len(lst[:upidx]))

        for i in range(len(self.child) - 1, self.getNumberOfKeys(), -1):
            self.child[i] = None

        return self.getIndex(), up, right.getIndex()

    def getLeftMost(self, bTree):
        ''' Return the left-most item in the
            subtree rooted at self.
        '''
        if self.child[0] == None:
            return self.items[0]

        return bTree.nodes[self.child[0]].getLeftMost(bTree)

    def delete(self, bTree, item):
        '''
           The delete method returns None if the item is not found
           and a deep copy of the item in the tree if it is found.
           As a side-effect, the tree is updated to delete the item.
        '''
        itemidx = None
        for i in range(self.getNumberOfKeys()):
            if self.items[i] == item:
                itemidx = i

        if itemidx != None:
            if self.child == [None] * (2 * self.degree + 1):
                self.items.pop(itemidx)
                self.items.append(None)
                self.numberOfKeys -= 1
                return item
            else:
                rightidx = itemidx + 1
                node = bTree.readFrom(self.getChild(rightidx))
                after = node.getLeftMost(bTree)
                self.items[itemidx] = BTreeNode.delete(
                    bTree.rootNode, bTree, after)
                self.redistributeOrCoalesce(bTree, rightidx)
                return item
        else:
            idx = 0
            finished = False
            while not finished and self.items[idx] < item:
                if self.items[idx] == None or idx == self.getNumberOfKeys()-1:
                    finished = True
                idx += 1

            node = bTree.readFrom(self.getChild(idx))
            r = BTreeNode.delete(node, bTree, item)
            self.redistributeOrCoalesce(bTree, idx)
            return item

    def redistributeOrCoalesce(self, bTree, childIndex):
        '''
          This method is given a node and a childIndex within
          that node that may need redistribution or coalescing.
          The child needs redistribution or coalescing if the
          number of keys in the child has fallen below the
          degree of the BTree. If so, then redistribution may
          be possible if the child is a leaf and a sibling has
          extra items. If redistribution does not work, then
          the child must be coalesced with either the left
          or right sibling.

          This method does not return anything, but has the
          side-effect of redistributing or coalescing
          the child node with a sibling if needed.
        '''
        node = bTree.readFrom(self.getChild(childIndex))
        if node.getNumberOfKeys() < bTree.degree:
            if childIndex == 0:
                left = None
                right = bTree.readFrom(self.getChild(childIndex+1))
                chosen = right
            elif childIndex == self.getNumberOfKeys():
                right = None
                left = bTree.readFrom(self.getChild(childIndex-1))
                chosen = left
            else:
                left = bTree.readFrom(self.getChild(childIndex-1))
                right = bTree.readFrom(self.getChild(childIndex+1))
                chosen = max([right, left], key=lambda x: x.getNumberOfKeys())

            if chosen.getNumberOfKeys() > bTree.degree:
                if chosen == right:
                    parentItem = self.items[childIndex]
                    self.items[childIndex] = bTree.delete(right.items[0])
                    bTree.insert(parentItem)
                else:
                    parentItem = self.items[childIndex-1]
                    self.items[childIndex -
                               1] = bTree.delete(left.items[left.getNumberOfKeys()-1])
                    bTree.insert(parentItem)
            else:
                if chosen == right:
                    parentItem = self.items[childIndex]
                    self.numberOfKeys -= 1
                else:
                    parentItem = self.items[childIndex-1]
                    self.numberOfKeys -= 1

                for i in range(childIndex, len(self.items)-1):
                    self.items[i] = self.items[i+1]
                for i in range(childIndex, len(self.child)-1):
                    self.child[i] = self.child[i+1]

                if self.getNumberOfKeys() == 0:
                    if self == bTree.rootNode:
                        bTree.rootNode = chosen
                        bTree.rootIndex = chosen.getIndex()
                    lst = chosen.items[:chosen.getNumberOfKeys(
                    )] + node.items[:node.getNumberOfKeys()] + [parentItem]
                    lst.sort()

                    children = []
                    for i in range(bTree.degree*2-(len(lst))):
                        lst.append(None)
                        children.append(None)

                    if chosen.getIndex() == self.child[0]:
                        for i in range(chosen.getNumberOfKeys()+1):
                            children.append(chosen.child[i])
                        for i in range(node.getNumberOfKeys()+1):
                            children.append(node.child[i])
                    else:
                        for i in range(node.getNumberOfKeys()+1):
                            children.append(node.child[i])
                        for i in range(chosen.getNumberOfKeys()+1):
                            children.append(chosen.child[i])

                    chosen.items = lst
                    chosen.child = children
                    chosen.setNumberOfKeys(0)
                    for item in chosen.items:
                        if item != None:
                            chosen.numberOfKeys += 1
                else:
                    bTree.insert(parentItem)
                    for i in range(node.getNumberOfKeys()):
                        bTree.insert(node.items[i])

    def getChild(self, i):
        # Answer the index of the ith child
        if (0 <= i <= self.numberOfKeys):
            return self.child[i]
        else:
            print('Error in getChild().')

    def setChild(self, i, childIndex):
        # Set the ith child of the node to childIndex
        self.child[i] = childIndex

    def getIndex(self):
        return self.index

    def setIndex(self, anInteger):
        self.index = anInteger

    def isFull(self):
        ''' Answer True if the receiver is full.  If not, return
          False.
        '''
        return (self.numberOfKeys == len(self.items))

    def getNumberOfKeys(self):
        return self.numberOfKeys

    def setNumberOfKeys(self, anInt):
        self.numberOfKeys = anInt

    def clear(self):
        self.numberOfKeys = 0
        self.items = [None]*len(self.items)
        self.child = [None]*len(self.child)

    def search(self, bTree, item):
        '''Answer a dictionary satisfying: at 'found'
          either True or False depending upon whether the receiver
          has a matching item;  at 'nodeIndex' the index of
          the matching item within the node; at 'fileIndex' the 
          node's index. nodeIndex and fileIndex are only set if the 
          item is found in the current node. 
        '''
        for i in range(self.getNumberOfKeys()):
            if self.items[i] == None:
                return {"found": False}
            elif self.items[i] == item:
                return {"found": True, "nodeIndex": i, "fileIndex": self.getIndex()}
            elif (self.items[i] > item) and (self.child != [None]*(2*self.degree+1)):
                node = bTree.nodes[self.getChild(i)]
                return node.search(bTree, item)
            if (i == self.getNumberOfKeys()-1) and (self.child != [None]*(2*self.degree+1)):
                node = bTree.nodes[self.getChild(i+1)]
                return node.search(bTree, item)

        return {"found": False}


class BTree:
    def __init__(self, degree, nodes={}, rootIndex=1, freeIndex=2):
        self.degree = degree

        if len(nodes) == 0:
            self.rootNode = BTreeNode(degree)
            self.nodes = {}
            self.rootNode.setIndex(rootIndex)
            self.writeAt(1, self.rootNode)
        else:
            self.nodes = deepcopy(nodes)
            self.rootNode = self.nodes[rootIndex]

        self.rootIndex = rootIndex
        self.freeIndex = freeIndex

    def __repr__(self):
        return "BTree("+str(self.degree)+",\n "+repr(self.nodes)+"," + \
            str(self.rootIndex)+","+str(self.freeIndex)+")"

    def __str__(self):
        st = '  The degree of the BTree is ' + str(self.degree) +\
             '.\n'
        st += '  The index of the root node is ' + \
              str(self.rootIndex) + '.\n'
        for x in range(1, self.freeIndex):
            node = self.readFrom(x)
            if node.getNumberOfKeys() > 0:
                st += str(node)
        return st

    def delete(self, anItem):
        ''' Answer None if a matching item is not found.  If found,
          answer the entire item.
        '''
        result = BTree.__searchTree(self, anItem)
        if result["found"] == False:
            return None
        return BTreeNode.delete(self.rootNode, self, anItem)

    def getFreeIndex(self):
        # Answer a new index and update freeIndex.  Private
        self.freeIndex += 1
        return self.freeIndex - 1

    def getFreeNode(self):
        # Answer a new BTreeNode with its index set correctly.
        # Also, update freeIndex.  Private
        newNode = BTreeNode(self.degree)
        index = self.getFreeIndex()
        newNode.setIndex(index)
        self.writeAt(index, newNode)
        return newNode

    def inorderOn(self, aFile):
        '''
          Print the items of the BTree in inorder on the file 
          aFile.  aFile is open for writing.
        '''
        aFile.write("An inorder traversal of the BTree:\n")
        self.inorderOnFrom(aFile, self.rootIndex)

    def inorderOnFrom(self, aFile, index):
        ''' Print the items of the subtree of the BTree, which is
          rooted at index, in inorder on aFile.
        '''
        pass

    def insert(self, anItem):
        ''' Answer None if the BTree already contains a matching
          item. If not, insert a deep copy of anItem and answer
          anItem.
        '''
        result = BTree.__searchTree(self, anItem)
        if result["found"] == True:
            return None

        left, middle, right = BTreeNode.insert(
            self.rootNode, self, deepcopy(anItem))
        if middle != None:
            node = self.getFreeNode()
            node.items[0] = middle
            node.setChild(0, left)
            node.setChild(1, right)
            node.setNumberOfKeys(1)
            self.rootNode = node
            self.rootIndex = node.getIndex()
        return anItem

    def levelByLevel(self, aFile):
        ''' Print the nodes of the BTree level-by-level on aFile. )
        '''
        pass

    def readFrom(self, index):
        ''' Answer the node at entry index of the btree structure.
          Later adapt to files
        '''
        if self.nodes.__contains__(index):
            return self.nodes[index]
        else:
            return None

    def recycle(self, aNode):
        # For now, do nothing
        aNode.clear()

    def retrieve(self, anItem):
        ''' If found, answer a deep copy of the matching item.
          If not found, answer None
        '''
        result = self.__searchTree(anItem)
        if result["found"] == True:
            fileIndex = result["fileIndex"]
            nodeIndex = result["nodeIndex"]
            return deepcopy(self.nodes[fileIndex].items[nodeIndex])
        return None

    def __searchTree(self, anItem):
        ''' Answer a dictionary.  If there is a matching item, at
          'found' is True, at 'fileIndex' is the index of the node
          in the BTree with the matching item, and at 'nodeIndex'
          is the index into the node of the matching item.  If not,
          at 'found' is False, but the entry for 'fileIndex' is the
          leaf node where the search terminated.
        '''
        return self.rootNode.search(self, anItem)

    def update(self, anItem):
        ''' If found, update the item with a matching key to be a
          deep copy of anItem and answer anItem.  If not, answer None.
        '''
        pass

    def writeAt(self, index, aNode):
        ''' Set the element in the btree with the given index
          to aNode.  This method must be invoked to make any
          permanent changes to the btree.  We may later change
          this method to work with files.
          This method is complete at this time.
        '''
        self.nodes[index] = aNode

    def __contains__(self, item):
        result = self.__searchTree(item)
        if result["found"] == True:
            return True
        return False


def btreemain():
    print("My/Our name(s) is/are ")

    lst = [10, 8, 22, 14, 12, 18, 2, 50, 15]

    b = BTree(2)

    for x in lst:
        print(repr(b))
        print("***Inserting", x)
        b.insert(x)

    print(repr(b))

    lst = [14, 50, 8, 12, 18, 2, 10, 22, 15]

    for x in lst:
        print("***Deleting", x)
        b.delete(x)
        print(repr(b))

    # return
    lst = [54, 76]

    for x in lst:
        print("***Deleting", x)
        b.delete(x)
        print(repr(b))

    print("***Inserting 14")
    b.insert(14)

    print(repr(b))

    print("***Deleting 2")
    b.delete(2)

    print(repr(b))

    print("***Deleting 84")
    b.delete(84)

    print(repr(b))


'''
Here is the expected output from running this program. Depending on the order of 
redistributing or coalescing, your output may vary. However, the end result in 
every case should be the insertion or deletion of the item from the BTree. 

My/Our name(s) is/are 
BTree(2,
 {1: BTreeNode(2,0,[None, None, None, None],[None, None, None, None, None],1)
},1,2)
***Inserting 10
BTree(2,
 {1: BTreeNode(2,1,[10, None, None, None],[None, None, None, None, None],1)
},1,2)
***Inserting 8
BTree(2,
 {1: BTreeNode(2,2,[8, 10, None, None],[None, None, None, None, None],1)
},1,2)
***Inserting 22
BTree(2,
 {1: BTreeNode(2,3,[8, 10, 22, None],[None, None, None, None, None],1)
},1,2)
***Inserting 14
BTree(2,
 {1: BTreeNode(2,4,[8, 10, 14, 22],[None, None, None, None, None],1)
},1,2)
***Inserting 12
BTree(2,
 {1: BTreeNode(2,2,[8, 10, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[14, 22, None, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, None, None, None],[1, 2, None, None, None],3)
},3,4)
***Inserting 18
BTree(2,
 {1: BTreeNode(2,2,[8, 10, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[14, 18, 22, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, None, None, None],[1, 2, None, None, None],3)
},3,4)
***Inserting 2
BTree(2,
 {1: BTreeNode(2,3,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[14, 18, 22, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, None, None, None],[1, 2, None, None, None],3)
},3,4)
***Inserting 50
BTree(2,
 {1: BTreeNode(2,3,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,4,[14, 18, 22, 50],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, None, None, None],[1, 2, None, None, None],3)
},3,4)
***Inserting 15
BTree(2,
 {1: BTreeNode(2,3,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[14, 15, None, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[12, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 14
**Redistribute From Left**
BTree(2,
 {1: BTreeNode(2,2,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[12, 15, None, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[10, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 50
**Coalesce with Left Sibling in node with index 3
BTree(2,
 {1: BTreeNode(2,2,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,4,[12, 15, 18, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[10, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 8
**Redistribute From Right**
BTree(2,
 {1: BTreeNode(2,2,[2, 10, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[15, 18, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 12
BTree(2,
 {1: BTreeNode(2,2,[2, 10, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[18, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 18
**Coalesce with Left Sibling in node with index 3
BTree(2,
 {1: BTreeNode(2,4,[2, 10, 15, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 2
BTree(2,
 {1: BTreeNode(2,3,[10, 15, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 10
BTree(2,
 {1: BTreeNode(2,2,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 22
BTree(2,
 {1: BTreeNode(2,1,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 15
BTree(2,
 {1: BTreeNode(2,0,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 54
54 not found during delete.
BTree(2,
 {1: BTreeNode(2,0,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 76
76 not found during delete.
BTree(2,
 {1: BTreeNode(2,0,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Inserting 14
BTree(2,
 {1: BTreeNode(2,1,[14, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 2
2 not found during delete.
BTree(2,
 {1: BTreeNode(2,1,[14, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 84
84 not found during delete.
BTree(2,
 {1: BTreeNode(2,1,[14, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
'''


def readRecord(file, recNum, recSize):
    file.seek(recNum*recSize)
    record = file.read(recSize)
    return record


def readField(record, colTypes, fieldNum):
    # fieldNum is zero based
    # record is a string containing the record
    # colTypes is the types for each of the columns in the record

    offset = 0
    for i in range(fieldNum):
        colType = colTypes[i]

        if colType == "int":
            offset += 10
        elif colType[:4] == "char":
            size = int(colType[4:])
            offset += size
        elif colType == "float":
            offset += 20
        elif colType == "datetime":
            offset += 24

    colType = colTypes[fieldNum]

    if colType == "int":
        value = record[offset:offset+10].strip()
        if value == "null":
            val = None
        else:
            val = int(value)
    elif colType == "float":
        value = record[offset:offset+20].strip()
        if value == "null":
            val = None
        else:
            val = float(value)
    elif colType[:4] == "char":
        size = int(colType[4:])
        value = record[offset:offset+size].strip()
        if value == "null":
            val = None
        else:
            val = value[1:-1]  # remove the ' and ' from each end of the string
            if type(val) == bytes:
                val = val.decode("utf-8")
    elif colType == "datetime":
        value = record[offset:offset+24].strip()
        if value == "null":
            val = None
        else:
            if type(val) == bytes:
                val = val.decode("utf-8")
            val = datetime.datetime.strptime(val, '%m/%d/%Y %I:%M:%S %p')
    else:
        print("Unrecognized Type")
        raise Exception("Unrecognized Type")

    return val


class Item:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return "Item("+repr(self.key)+","+repr(self.value)+")"

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __ge__(self, other):
        return self.key >= other.key

    def getValue(self):
        return self.value

    def getKey(self):
        return self.key


def main():
    # Select Feed.FeedNum, Feed.Name, FeedAttribType.Name, FeedAttribute.Value where
    # Feed.FeedID = FeedAttribute.FeedID and FeedAttribute.FeedAtribTypeID = FeedAttribType.ID
    attribTypeCols = ["int", "char20", "char60", "int", "int", "int", "int"]
    feedCols = ["int", "int", "int", "char50", "datetime",
                "float", "float", "int", "char50", "int"]
    feedAttributeCols = ["int", "int", "float"]

    feedAttributeTable = open("FeedAttribute.tbl", "r")

    if os.path.isfile("Feed.idx"):
        indexFile = open("Feed.idx", "r")
        feedTableRecLength = int(indexFile.readline())
        feedIndex = eval("".join(indexFile.readlines()))
    else:
        feedIndex = BTree(3)
        feedTable = open("Feed.tbl", "r")
        offset = 0
        for record in feedTable:
            feedID = readField(record, feedCols, 0)
            anItem = Item(feedID, offset)
            feedIndex.insert(anItem)
            offset += 1
            feedTableRecLength = len(record)

        print("Feed Table Index Created")
        indexFile = open("Feed.idx", "w")
        indexFile.write(str(feedTableRecLength)+"\n")
        indexFile.write(repr(feedIndex)+"\n")
        indexFile.close()

    if os.path.isfile("FeedAttribType.idx"):
        indexFile = open("FeedAttribType.idx", "r")
        attribTypeTableRecLength = int(indexFile.readline())
        attribTypeIndex = eval("".join(indexFile.readlines()))
    else:
        attribTypeIndex = BTree(3)
        attribTable = open("FeedAttribType.tbl", "r")
        offset = 0
        for record in attribTable:
            feedAttribTypeID = readField(record, attribTypeCols, 0)
            anItem = Item(feedAttribTypeID, offset)
            attribTypeIndex.insert(anItem)
            offset += 1
            attribTypeTableRecLength = len(record)

        print("Attrib Type Table Index Created")
        indexFile = open("FeedAttribType.idx", "w")
        indexFile.write(str(attribTypeTableRecLength)+"\n")
        indexFile.write(repr(attribTypeIndex)+"\n")
        indexFile.close()

    feedTable = open("Feed.tbl", "rb")
    feedAttribTypeTable = open("FeedAttribType.tbl", "rb")
    before = datetime.datetime.now()
    for record in feedAttributeTable:

        feedID = readField(record, feedAttributeCols, 0)
        feedAttribTypeID = readField(record, feedAttributeCols, 1)
        value = readField(record, feedAttributeCols, 2)

        lookupItem = Item(feedID, None)
        item = feedIndex.retrieve(lookupItem)
        offset = item.getValue()
        feedRecord = readRecord(feedTable, offset, feedTableRecLength)
        feedNum = readField(feedRecord, feedCols, 2)
        feedName = readField(feedRecord, feedCols, 3)

        lookupItem = Item(feedAttribTypeID, None)
        item = attribTypeIndex.retrieve(lookupItem)
        offset = item.getValue()
        feedAttribTypeRecord = readRecord(feedAttribTypeTable, offset,
                                          attribTypeTableRecLength)
        feedAttribTypeName = readField(feedAttribTypeRecord, attribTypeCols, 1)

        print(feedNum, feedName, feedAttribTypeName, value)
    after = datetime.datetime.now()
    deltaT = after - before
    milliseconds = deltaT.total_seconds() * 1000
    print("Done. The total time for the query with indexing was", milliseconds,
          "milliseconds.")


if __name__ == "__main__":
    btreemain()
    main()
