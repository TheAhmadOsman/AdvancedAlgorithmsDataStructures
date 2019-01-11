""" 
    First, I have the xml file that I made these comments on attached in the uploaded zipped file. I tried to run the program with big numbers that would cause integer overflow. However, I noticed that Python does not care about the variable specified size and would just go on to increase the amount of space that the variable would need when doing multiplication. Also, it seemed like this pattern did not change the almost O(1) complexity when doing multiplication. This means that the multiplication operator itself counts for the dynamic assignments that the language makes during the operation and keeps the performance at O(1)
    From the graph, we can see that the line tends to stay as a a straight line on the same axis, proving that it is an O(1) operation.
    There are a couple of abnormalities that were found on the graph, mostly caused by the processor dealing with other tasks at the same time. But nothing really of a pattern.
    There isn't a clear cutoff point for handling multiplication in constant time because Python would dynamically move on into a bigger variable size.
    All in all, the multiplication process is in O(1).
"""

import datetime
import random
import time

def main():
    # Write an XML file with data
    file = open("Multiplication.xml", "w")
    file.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')
    file.write('<Plot title="Average Multiplication Time">\n')

    # Multiplying xmin by xmax, increasing both by 1000 for a 10000 times.
    xmin = 1000
    xmax = 2000

    # Recording the values of multiplication in xList and the amount of time for each product in yList
    xList = []
    yList = []

    i = 0
    while i < 10000:
        starttime = datetime.datetime.now()
        prod = xmin * xmax
        endtime = datetime.datetime.now()
        
        xList.append(prod)
        
        # The difference in time between start and end.
        deltaT = endtime - starttime

        # Divide by 1000 for the average access time
        # But also multiply by 1000000 for microseconds.
        accessTime = deltaT.total_seconds() * 1000000

        yList.append(accessTime)

        print(prod)

        xmin += 1000
        xmax += 1000
        i += 1

    file.write('  <Axes>\n')
    file.write('    <XAxis min="'+str(min(xList))+'" max="' +
               str(max(xList))+'">Product Value</XAxis>\n')
    file.write('    <YAxis min="'+str(min(yList)) +
               '" max="'+str(max(yList))+'">Microseconds</YAxis>\n')
    file.write('  </Axes>\n')

    file.write(
        '  <Sequence title="Average Time to Multipy by the Factor of Size" color="red">\n')

    for i in range(len(xList)):
        file.write('    <DataPoint x="' +
                   str(xList[i])+'" y="'+str(yList[i])+'"/>\n')

    file.write('  </Sequence>\n')

    file.write('</Plot>\n')
    file.close()
    print("program done")


if __name__ == "__main__":
    main()
