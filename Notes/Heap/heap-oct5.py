class Priority Queue:
	def __init__(self, degree=2, contents = []):
		self.degree = degree
		self.data = list(contents)
		parentIndex = (len(self.data) - 2) // self.degree

		for i in range(parentIndex, -1, -1):
			self.__siftDownFromTo(i, len(self.data)-1)

def __siftDownFromTo(self, parentIdx, endIdx):
	done = False
	while not done and parentIdx < (endIdx-1)//self.degree:
		bestChildIdx = self.__bestChildOf(parentIdx, endIdx)
		if self.data[parentIdx] > self.data[bestChildIdx]:
			selft.data[parentIdx], self.data[bestChildIdx] = self.data[bestChildIdx], selft.data[parentIdx]
			parentIdx = bestChildIdx
		else:
			done = True

def __bestChildOf(self, parentIdx, endIdx):
	bestChildIdx = parentIdx * self.degree + 1
	endIdx = min(bestChildIdx + self.degree -1, endIdx)
	for i in range(bestChildIdx + 1, endIdx):
		if self.data[i] < self.data[bestChildIdx]:
			bestChildIdx = i

	return bestChildIdx

Trinary Heap:
	8	10	18	25	2	9	7	4	11	17

