from hashset import HashSet

from datetime import datetime


def buildPuzzle(file):
    puzzle = []
    for line in file:
        line = line.strip("\n")
        line = line.split()
        isEmpty = False
        if len(line) == 0:
            isEmpty = True
        rowEntry = []
        if not isEmpty:
            counter = 0
            for item in line:
                counter += 1
                if item == "x":
                    rowEntry.append(HashSet([1, 2, 3, 4, 5, 6, 7, 8, 9]))
                else:
                    try:
                        rowEntry.append(HashSet([int(item)]))
                    except:
                        print(
                            "Your puzzle is in an invalid format. Please include only numbers seperated by a space.")
                        file.close()
                        return
            puzzle.append(rowEntry)
            if counter != 9:
                print(
                    "Your puzzle is in an invalid format. Please include only numbers seperated by a space.")
                file.close()
                return
    file.close()
    return puzzle


def buildGroups(puzzle):
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


def readFile():
    while True:
        print("Enter the name of your sudoku puzzle (without .txt)")
        try:
            fileName = input()
            file = open(fileName + ".txt", "r")
            return file, fileName
        except:
            print("{} cannot be found".format(fileName))


def writeFile(puzzle, fileName):
    file = open(fileName + "Solution" + ".txt", "w")
    for row in puzzle:
        rowStr = ""
        for entry in row:
            num = str(entry.pop())
            file.write(num + " ")
            rowStr += num + " "
        print(rowStr)
        file.write("\n")
    print("Solution has been written to {}Solution.txt".format(fileName))


def reduceGroups(groups):
    changed = True
    runs = 0
    while changed:
        runs += 1
        print("Puzzle reduced {} time(s)".format(runs))
        changed = False
        for group in groups:
            if reduceGroup(group):
                changed = True


def reduceGroup(group):
    changed = False

    # Rule 1
    for entry in group:
        if len(entry) != 9:
            similarEntries = []
            for compareEntry in group:
                if entry == compareEntry:
                    similarEntries.append(compareEntry)
            if len(entry) == len(similarEntries):
                for reduceEntry in group:
                    if reduceEntry != entry:
                        oldEntry = reduceEntry.copy()
                        reduceEntry.difference_update(entry)
                        if oldEntry != reduceEntry:
                            changed = True

    # Rule 2
    for entry in group:
        if len(entry) != 1:
            uniqueValues = entry.copy()
            for compareEntry in group:
                if compareEntry is not entry:
                    uniqueValues.difference_update(compareEntry)
            if len(uniqueValues) == 1:
                changed = True
                entry.intersection_update(uniqueValues)
    return changed


def integrityCheck(puzzle):
    for row in puzzle:
        for entry in row:
            if len(entry) != 1:
                return True


def main():

    file, fileName = readFile()

    start = datetime.now()

    puzzle = buildPuzzle(file)
    if not puzzle:
        return

    groups = buildGroups(puzzle)

    print("{} groups formed.".format(len(groups)))

    reduceGroups(groups)

    err = integrityCheck(puzzle)

    if err:
        print("No solution found for {}.".format(fileName))
        return

    end = datetime.now()

    print("Solution found in {} seconds".format((end - start).total_seconds()))

    writeFile(puzzle, fileName)


if __name__ == "__main__":
    main()
