from typing import List

class kv:
    def __init__(self,k:str,v:float):
        self.k = k
        self.v = v

class max_heap:
    def __init__(self):
        self.heap:List[kv] = []

    def push(self,val:kv):
        self.heap.append(val)
        self._heapUp(len(self.heap)-1)

    def pop(self)->kv:
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap[0]
        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapDown(0)
        return max_val

    def _heapUp(self,index:int):
        parent = (index - 1)//2
        if index > 0 and self.heap[index].v > self.heap[parent].v:
            self._swap(index,parent)
            self._heapUp(parent)
            
    def _heapDown(self,index:int):
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.heap) and self.heap[left].v > self.heap[largest].v:
            largest = left
        if right < len(self.heap) and self.heap[right].v > self.heap[largest].v:
            largest = right
        if largest != index:
            self._swap(largest,index)
            self._heapDown(largest)

    def _swap(self,a:int,b:int):
        self.heap[a],self.heap[b] = self.heap[b],self.heap[a]
