def add_to_n(x):
    total = 0
    for counter in range(2, x+1):
        if counter % 2 == 0:
            total = total + counter

    return total

addTo = 10
total = add_to_n(addTo)
print(total)