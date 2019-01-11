# The following line is the import for testing with my code.
#import joinquerybtreerecursive as btree

import btree


def Node__repr__(self):
    degree = len(self.items) // 2
    items = self.items[:self.numberOfKeys] + ([None] * (degree*2 - self.numberOfKeys))
    children = self.child[:self.numberOfKeys+1] + ([None] * (degree*2 - self.numberOfKeys))
    return "BTreeNode("+str(degree)+","+str(self.numberOfKeys) + \
    ","+repr(items)+","+repr(children)+","+str(self.index)+")\n"


btree.BTreeNode.__repr__ = Node__repr__



def main():

    points = 23

    try:
        print("**** BTree of degree 2 created.")
        tree = btree.BTree(2)
        print(repr(tree))
        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,0,[None, None, None, None],[None, None, None, None, None],1)
},1,2)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("*** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Inserting 5")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,0,[None, None, None, None],[None, None, None, None, None],1)},1,2)
        tree.insert(5)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,1,[5, None, None, None],[None, None, None, None, None],1)
},1,2)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Inserting 3")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,1,[5, None, None, None],[None, None, None, None, None],1)},1,2)
        tree.insert(3)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[3, 5, None, None],[None, None, None, None, None],1)
},1,2)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Inserting 10")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,2,[3, 5, None, None],[None, None, None, None, None],1)},1,2)
        tree.insert(10)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,3,[3, 5, 10, None],[None, None, None, None, None],1)
},1,2)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Inserting 1")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,3,[3, 5, 10, None],[None, None, None, None, None],1)},1,2)
        tree.insert(1)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,4,[1, 3, 5, 10],[None, None, None, None, None],1)
},1,2)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Inserting 15 causing a split")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,4,[1, 3, 5, 10],[None, None, None, None, None],1)},1,2)
        tree.insert(15)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[1, 3, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[10, 15, None, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[5, None, None, None],[1, 2, None, None, None],3)
},3,4)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Inserting 25")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,2,[1, 3, None, None],[None, None, None, None, None],1), 2: btree.BTreeNode(2,2,[10, 15, None, None],[None, None, None, None, None],2), 3: btree.BTreeNode(2,1,[5, None, None, None],[1, 2, None, None, None],3)},3,4)
        tree.insert(25)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[1, 3, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[10, 15, 25, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[5, None, None, None],[1, 2, None, None, None],3)
},3,4)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Inserting 21")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,2,[1, 3, None, None],[None, None, None, None, None],1), 2: btree.BTreeNode(2,3,[10, 15, 25, None],[None, None, None, None, None],2), 3: btree.BTreeNode(2,1,[5, None, None, None],[1, 2, None, None, None],3)},3,4)
        tree.insert(21)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[1, 3, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,4,[10, 15, 21, 25],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[5, None, None, None],[1, 2, None, None, None],3)
},3,4)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Inserting 23 causing a split")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,2,[1, 3, None, None],[None, None, None, None, None],1), 2: btree.BTreeNode(2,4,[10, 15, 21, 25],[None, None, None, None, None],2), 3: btree.BTreeNode(2,1,[5, None, None, None],[1, 2, None, None, None],3)},3,4)
        tree.insert(23)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[1, 3, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[10, 15, None, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[5, 21, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[23, 25, None, None],[None, None, None, None, None],4)
},3,5)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Inserting 17")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,2,[1, 3, None, None],[None, None, None, None, None],1), 2: btree.BTreeNode(2,2,[10, 15, None, None],[None, None, None, None, None],2), 3: btree.BTreeNode(2,2,[5, 21, None, None],[1, 2, 4, None, None],3), 4: btree.BTreeNode(2,2,[23, 25, None, None],[None, None, None, None, None],4)},3,5)
        tree.insert(17)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[1, 3, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[10, 15, 17, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[5, 21, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[23, 25, None, None],[None, None, None, None, None],4)
},3,5)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Inserting 19")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,2,[1, 3, None, None],[None, None, None, None, None],1), 2: btree.BTreeNode(2,3,[10, 15, 17, None],[None, None, None, None, None],2), 3: btree.BTreeNode(2,2,[5, 21, None, None],[1, 2, 4, None, None],3), 4: btree.BTreeNode(2,2,[23, 25, None, None],[None, None, None, None, None],4)},3,5)
        tree.insert(19)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[1, 3, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,4,[10, 15, 17, 19],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[5, 21, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[23, 25, None, None],[None, None, None, None, None],4)
},3,5)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Deleting 1 causing redistribute from the right.")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,2,[1, 3, None, None],[None, None, None, None, None],1), 2: btree.BTreeNode(2,4,[10, 15, 17, 19],[None, None, None, None, None],2), 3: btree.BTreeNode(2,2,[5, 21, None, None],[1, 2, 4, None, None],3), 4: btree.BTreeNode(2,2,[23, 25, None, None],[None, None, None, None, None],4)},3,5)
        tree.delete(1)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[3, 5, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[15, 17, 19, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[10, 21, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[23, 25, None, None],[None, None, None, None, None],4)
},3,5)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Inserting 20")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,2,[3, 5, None, None],[None, None, None, None, None],1), 2: btree.BTreeNode(2,3,[15, 17, 19, None],[None, None, None, None, None],2), 3: btree.BTreeNode(2,2,[10, 21, None, None],[1, 2, 4, None, None],3), 4: btree.BTreeNode(2,2,[23, 25, None, None],[None, None, None, None, None],4)},3,5)
        tree.insert(20)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[3, 5, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,4,[15, 17, 19, 20],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[10, 21, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[23, 25, None, None],[None, None, None, None, None],4)
},3,5)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Deleting 23 causing redistribute from the left.")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,2,[3, 5, None, None],[None, None, None, None, None],1), 2: btree.BTreeNode(2,4,[15, 17, 19, 20],[None, None, None, None, None],2), 3: btree.BTreeNode(2,2,[10, 21, None, None],[1, 2, 4, None, None],3), 4: btree.BTreeNode(2,2,[23, 25, None, None],[None, None, None, None, None],4)},3,5)
        tree.delete(23)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[3, 5, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[15, 17, 19, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[10, 20, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[21, 25, None, None],[None, None, None, None, None],4)
},3,5)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Inserting 24")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,2,[3, 5, None, None],[None, None, None, None, None],1), 2: btree.BTreeNode(2,3,[15, 17, 19, None],[None, None, None, None, None],2), 3: btree.BTreeNode(2,2,[10, 20, None, None],[1, 2, 4, None, None],3), 4: btree.BTreeNode(2,2,[21, 25, None, None],[None, None, None, None, None],4)},3,5)
        tree.insert(24)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[3, 5, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[15, 17, 19, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[10, 20, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,3,[21, 24, 25, None],[None, None, None, None, None],4)
},3,5)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

        print("\n**** Deleting 20 from interior node.")

        tree.delete(20)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[3, 5, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[15, 17, 19, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[10, 21, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[24, 25, None, None],[None, None, None, None, None],4)
},3,5)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()

    try:

        print("\n**** Deleting 21")

        tree = btree.BTree(2,{1: btree.BTreeNode(2,2,[3, 5, None, None],[None, None, None, None, None],1), 2: btree.BTreeNode(2,3,[15, 17, 19, None],[None, None, None, None, None],2), 3: btree.BTreeNode(2,2,[10, 21, None, None],[1, 2, 4, None, None],3), 4: btree.BTreeNode(2,2,[24, 25, None, None],[None, None, None, None, None],4)},3,5)
        tree.delete(21)

        print(repr(tree))

        if repr(tree) == """BTree(2,
 {1: BTreeNode(2,2,[3, 5, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[15, 17, None, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[10, 19, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[24, 25, None, None],[None, None, None, None, None],4)
},3,5)""":
            print("**** Passed that test\n")
            points += 1
        else:
            print("**** There was a problem\n")

    except Exception as ex:
        print("**** There was an exception while running your code.")
        print(ex)
        print()




    print("*** You got", points, "out of 40 points for the program.")

if __name__ == "__main__":
    main()
