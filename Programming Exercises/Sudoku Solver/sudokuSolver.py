# Ahmad M. Osman - sudokuSolver.py - Dr. Kent Lee, CS360


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
        newset = HashSet(self)
        for item in other:
            newset.add(item)
        return newset

    def intersection(self, other):
        newset = HashSet(self)
        newset.intersection_update(other)
        return newset

    def difference(self, other):
        newset = HashSet(self)
        newset.difference_update(other)
        return newset

    def copy(self):
        return HashSet(self)

    # Operator Definitions
    def __eq__(self, other):
        if len(other) != len(self):
            return False
        return self.issuperset(other) and self.issubset(other)


class PuzzleError(Exception):
    pass


def build_puzzle(f):
    puzzle = []
    for line in f:
        line = line.strip("\n")
        line = line.split()
        empty = False
        if len(line) == 0:
            empty = True
        row = []
        if not empty:
            counter = 0
            for item in line:
                counter += 1
                if item == "x":
                    row.append(HashSet([1, 2, 3, 4, 5, 6, 7, 8, 9]))
                else:
                    try:
                        row.append(HashSet([int(item)]))
                    except:
                        f.close()
                        raise PuzzleError("Puzzle is in invalid format")
            puzzle.append(row)
            if counter != 9:
                f.close()
                raise PuzzleError("Puzzle is in invalid format")
    f.close()
    return puzzle


def build_groups(puzzle):
    groups = []

    for row in puzzle:
        groups.append(row)

    for i in range(9):
        col = []
        for j in range(9):
            col.append(puzzle[j][i])
        groups.append(col)

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            box = []
            for k in range(3):
                for m in range(3):
                    box.append(puzzle[i + k][j + m])
            groups.append(box)

    return groups


def reduce_group(group):
    changed = False

    for cell in group:
        if len(cell) != 9:
            similar = []
            for compare_to in group:
                if cell == compare_to:
                    similar.append(compare_to)
            if len(cell) == len(similar):
                for reduce_this in group:
                    if reduce_this != cell:
                        old = reduce_this.copy()
                        reduce_this.difference_update(cell)
                        if old != reduce_this:
                            changed = True

    for cell in group:
        if len(cell) != 1:
            unique_values = cell.copy()
            for compare_to in group:
                if compare_to is not cell:
                    unique_values.difference_update(compare_to)
            if len(unique_values) == 1:
                changed = True
                cell.intersection_update(unique_values)

    return changed


def reduce_groups(groups):
    changed = True
    while changed:
        changed = False
        for group in groups:
            if reduce_group(group):
                changed = True


def main():
    filename = ""
    while True:
        filename = input("Enter sudoku puzzle file name: ")
        try:
            f = open(filename, "r")
            break
        except:
            print(filename, "couldn't be found")

    puzzle = build_puzzle(f)
    groups = build_groups(puzzle)
    reduce_groups(groups)

    for row in puzzle:
        for cell in row:
            if len(cell) != 1:
                raise PuzzleError("Couldn't be solved")

    f = open(filename.split('.')[0] + "Solution.txt", "w")
    for row in puzzle:
        row_str = ""
        for cell in row:
            num = str(cell.pop())
            f.write(num + " ")
            row_str += num + " "
        print(row_str)
        f.write("\n")
    print(filename.split('.')[0] + "Solution.txt has been created")


if __name__ == "__main__":
    main()
