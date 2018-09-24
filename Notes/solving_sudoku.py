groups = []
for row in puzzle:
    groups.append(row)

groups = list(puzzle)  # same as the above loop

# to access cols
puzzle[rowIndex][colIndex]

for i in range(0, 9, 3):
    for j in range(0, 9, 3):
        group = []
        for k in range(3):
            for m in range(3):
