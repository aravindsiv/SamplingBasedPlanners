class State:
  def __init__(self,x,y,cost,idx):
    self.cost = cost
    self.x = x
    self.y = y
    self.idx = idx

class priority_queue:
  def __init__(self):
    self.heap = []

  def isEmpty(self):
    return len(self.heap)==0

  def elementInHeap(self,x,y):
    for i in range(len(self.heap)):
      if self.heap[i].x == x and self.heap[i].y == y:
        return i
    return -1

  def minKey(self):
    return self.heap[0].cost

  def top(self):
    return self.heap[0]

  def parent(self,child):
    parentIndex = (child-1)/2
    if parentIndex < 0:
      return -1
    return parentIndex

  def remove(self,index):
    if index == len(self.heap)-1:
      self.heap.pop()
      return
    self.heap[index], self.heap[-1] = self.heap[-1], self.heap[index]
    self.heap.pop()
    if index == 0 or self.heap[index].cost > self.heap[self.parent(index)].cost:
      self.minheapify_pop(index)
    else:
      self.minheapify_ins(index)

  def insert(self,x,y,cost,idx):
    temp = State(x,y,cost,idx)
    self.heap.append(temp)
    self.minheapify_ins(len(self.heap)-1)

  def pop(self):
    temp = self.top()
    self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
    self.heap.pop()
    self.minheapify_pop(0)
    return temp

  def leftChild(self,parent):
    lcIndex = 2*parent + 1
    if lcIndex < len(self.heap):
      return lcIndex
    return -1

  def rightChild(self,parent):
    rcIndex = 2*(parent+1)
    if rcIndex < len(self.heap):
      return rcIndex
    return -1

  def minheapify_pop(self,index):
    lcIndex = self.leftChild(index)
    # print "Left child index is ",lcIndex
    rcIndex = self.rightChild(index)
    # print "Right child index is ",rcIndex
    minElement = index

    if lcIndex < len(self.heap) and lcIndex >= 0 and self.heap[lcIndex].cost < self.heap[index].cost:
      minElement = lcIndex
    if rcIndex < len(self.heap) and rcIndex >= 0 and self.heap[rcIndex].cost < self.heap[minElement].cost:
      minElement = rcIndex

    if minElement != index:
      self.heap[index], self.heap[minElement] = self.heap[minElement], self.heap[index]
      self.minheapify_pop(minElement)

  def minheapify_ins(self,index):
    parentIndex = self.parent(index)
    if parentIndex >= 0 and self.heap[parentIndex].cost > self.heap[index].cost:
      self.heap[parentIndex], self.heap[index] = self.heap[index], self.heap[parentIndex]
      self.minheapify_ins(parentIndex)

  def displayHeap(self):
    for item in self.heap:
      print "("+str(item.x)+","+str(item.y)+") Cost: "+str(item.cost)


if __name__ == "__main__":
  array = [42,23,16,15,4,8]
  pq = priority_queue()
  for item in array:
    pq.insert(0,0,item)
  pq.displayHeap()
  for i in range(6):
    pq.pop()
    pq.displayHeap()


