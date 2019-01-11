def reduceGroups(groups):
    changed = True
    while changed:
        changed = False
        for group in groups:
            if reduceGroup(group):
                changed = True

# You should never get to a curdinality of zero - Use len function for this

# Equality in sets
a = set({1,2,3})
b = set({1,2,3})
b == a

# Harder example!
c = set({2,3,4,5})
a != c
# The following isn't the same as it is a reference equator # is keyword can only be like a is None because there is only one object in any program and it is the same reference
a is b

# Use difference_update when removing elements usign rules #1 and #2

# Set = HashSet(Java)

# Hashtable = Map = Dictionary == HashMap