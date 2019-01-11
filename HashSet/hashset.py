#################################################################################
# HashSet.py - A hashtable implementation of a set datatype.
#################################################################################
# To complete this implementation you must complete the code for all methods that
# currently have a "pass" in them. Consult the documentation for these methods
# to see what they should return. Many of these methods can be implemented
# by calling other supporting methods, so make sure you don't write more
# code than necessary. Many methods take exactly one line of code to implement.
# The test main function at the bottom should completely run passing all tests
# once you have implemented the methods here. The test main function is not
# intended to completely test the entire class though. You have to write
# additional tests to throroughly test the HashSet class.


class HashSet:
    class __Placeholder:
        def __init__(self):
            self.name = "Placeholder"

        def __eq__(self, other):
            try:
                if other.name == "Placeholder":
                    return True
            except:
                return False
            return False

    def __add(item, items):
        idx = hash(item) % len(items)
        loc = -1

        while items[idx] != None:
            if items[idx] == item:
                # item already in set
                return False

            if loc < 0 and type(items[idx]) == HashSet.__Placeholder:
                loc = idx

            idx = (idx + 1) % len(items)

        if loc < 0:
            loc = idx

        items[loc] = item

        return True

    def __remove(item, items):
        idx = hash(item) % len(items)

        while items[idx] != None:
            if items[idx] == item:
                nextIdx = (idx + 1) % len(items)
                if items[nextIdx] == None:
                    items[idx] = None
                else:
                    items[idx] = HashSet.__Placeholder()
                return True

            idx = (idx + 1) % len(items)

        return False

    def __rehash(oldList, newList):
        for x in oldList:
            if x != None and type(x) != HashSet.__Placeholder:
                HashSet.__add(x, newList)

        return newList

    def __init__(self, contents=[]):
        self.items = [None] * 10
        self.numItems = 0

        for item in contents:
            self.add(item)

    def __str__(self):
        return str(self.items)

    def __iter__(self):
        for i in range(len(self.items)):
            if self.items[i] != None and type(self.items[i]) != HashSet.__Placeholder:
                yield self.items[i]

    # Following are the mutator set methods
    def add(self, item):
        if HashSet.__add(item, self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= 0.75:
                self.items = HashSet.__rehash(
                    self.items, [None]*2*len(self.items))

    def remove(self, item):
        if HashSet.__remove(item, self.items):
            self.numItems -= 1
            load = max(self.numItems, 10) / len(self.items)
            if load <= 0.25:
                self.items = HashSet.__rehash(
                    self.items, [None]*int(len(self.items)/2))
        else:
            raise KeyError("Item not in HashSet")

    def discard(self, item):
        if item in self:
            self.remove(item)

    def pop(self):
        for item in self:
            saved = item
            self.remove(item)
            return saved
        raise KeyError("Empty HashSet")

    def clear(self):
        for item in self.items:
            if item != None:
                self.remove(item)

    def update(self, other):
        for item in other:
            if item not in self:
                self.add(item)

    def intersection_update(self, other):
        discard = set()
        for item in self:
            if item not in other:
                discard.add(item)
        for item in discard:
            self.discard(item)

    def difference_update(self, other):
        for item in other:
            self.discard(item)

    def symmetric_difference_update(self, other):
        pass

    # Following are the accessor methods for the HashSet
    def __len__(self):
        return self.numItems

    def __contains__(self, item):
        idx = hash(item) % len(self.items)
        while self.items[idx] != None:
            if self.items[idx] == item:
                return True

            idx = (idx + 1) % len(self.items)

        return False

    # One extra method for use with the HashMap class. This method is not needed in the
    # HashSet implementation, but it is used by the HashMap implementation.
    def __getitem__(self, item):
        pass

    def not__contains__(self, item):
        pass

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
        clone = HashSet(self)
        for item in other:
            clone.add(item)
        return clone

    def intersection(self, other):
        clone = HashSet(self)
        clone.intersection_update(other)
        return clone

    def difference(self, other):
        clone = HashSet(self)
        clone.difference_update(other)
        return clone

    def symmetric_difference(self, other):
        pass

    def copy(self):
        return HashSet(self)

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
        if len(other) != len(self):
            return False
        return self.issuperset(other) and self.issubset(other)


def main():
    s = HashSet(list(range(100)))

    t = HashSet(list(range(10, 20)))

    u = HashSet(list(range(10, 20)))

    if len(t) == len(u) and len(t) == 10:
        print("Test 1 Passed")
    else:
        print("Test 1 Failed")

    s.intersection_update(t)

    if len(s) == 10:
        print("Test 2 Passed")
    else:
        print("Test 2 Failed")

    s = HashSet(list(range(100)))

    t.update(s)

    if len(s) == len(t):
        print("Test 3 Passed")
    else:
        print("Test 3 Failed")

    t.clear()
    t.update(u)

    if len(t) == len(u):
        print("Test 4 Passed")
    else:
        print("Test 4 Failed")

    s.difference_update(t)

    test5Passed = True
    test6Passed = True

    for x in range(1, 10):
        if x in s:
            pass
        else:
            test5Passed = False
            print("Test 5 Failed on", x)

        if x not in s:
            test6Passed = False
            print("Test 6 Failed on", x)

    if test5Passed:
        print("Test 5 Passed")

    if test6Passed:
        print("Test 6 Passed")

    test7Passed = True
    test8Passed = True

    for x in range(20, 100):
        if x in s:
            pass
        else:
            test7Passed = False
            print("Test 7 Failed on", x)

        if x not in s:
            test8Passed = False
            print("Test 8 Failed on", x)

    if test7Passed:
        print("Test 7 Passed")

    if test8Passed:
        print("Test 8 Passed")

    x = HashSet(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"])

    y = HashSet(["c", "d", "e", "l", "m", "n"])

    z = x.difference(y)

    if len(z) == 8:
        print("Test 9 Passed")
    else:
        print("Test 9 Failed")

    test10Passed = True

    for item in z:
        if item not in ["a", "b", "f", "g", "h", "i", "j", "k"]:
            test10Passed = False
            print("Test 10 Failed on", x)

    if test10Passed:
        print("Test 10 Passed")

    if z.issubset(x):
        print("Test 11 Passed")
    else:
        print("Test 11 Failed")

    if x.issuperset(z):
        print("Test 12 Passed")
    else:
        print("Test 12 Failed")

    if z == y:
        print("Test 13 Failed")
    else:
        print("Test 13 Passed")

    if z == z:
        print("Test 14 Passed")
    else:
        print("Test 14 Failed")

    r = z.copy()

    if r == z:
        print("Test 15 Passed")
    else:
        print("Test 15 Failed")

    for item in range(50):
        z.add(item)

    for item in range(50):
        z.discard(item)

    if r == z:
        print("Test 16 Passed")
    else:
        print("Test 16 Failed")

    for item in range(50):
        z.add(item)

    for item in range(50):
        z.remove(item)

    if r == z:
        print("Test 17 Passed")
    else:
        print("Test 17 Failed")


if __name__ == "__main__":
    main()
