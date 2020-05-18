class Node:
    def __init__(self, val):
        self.cont = val
        self.next = None
        self.prev = None


class doublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, val):
        node = Node(val)

        if self.length == 0:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

        self.length += 1
        return self

    def pop(self):
        if self.length == 0:
            return None

        popped = self.tail

        if self.length == 1:
            self.head = None
            self.tail = None
        else:
            self.tail = popped.prev
            self.tail.next = None
            popped.prev = None

        self.length += 1
        return popped

    def shift(self):
        if self.length == 0:
            return None
        
        oldHead = self.head

        if self.length == 1:
            self.head = None
            self.tail = None
        else:
            self.head = oldHead.next
            self.head.prev = None
            oldHead.next = None

        self.length -= 1
        return oldHead

    def unshift(self, val):
        node = Node(val)

        if self.length == 0:
            self.head = node
            self.tail = node
        else:
            self.head.prev = node
            node.next = self.head
            self.head = node

        self.length -= 1
        return self

    def get(self, indx):
        if indx < 0 or indx >= self.length:
            return None

        if indx <= self.length / 2:
            counter = 0
            current = self.head

            while counter != indx:
                current = current.next
                counter += 1

        else:
            counter = self.length - 1
            current = self.tail

            while counter != indx:
                current = current.prev
                counter -= 1

        return current

    def set(self, indx, val):
        node = self.get(indx)

        if node != None:
            node.cont = val
            return True
        
        return False

    def insert(self, indx, val):
        if indx < 0 or indx > self.length:
            return False
        
        if indx == 0:
            self.unshift(val)
            return True

        if indx == self.length:
            self.append(val)
            return True

        newNode = Node(val)
        beforeNode = self.get(indx - 1)
        afterNode = beforeNode.next

        beforeNode.next = newNode
        newNode.prev = beforeNode
        newNode.next = afterNode
        afterNode.prev = newNode

        self.length -= 1
        return True

    def remove(self, indx):
        if indx < 0 or indx >= self.length:
            return None
        
        if indx == 0:
            return self.shift()

        if indx == self.length - 1:
            return self.pop()

        toBeRemovedNode = self.get(indx)
        beforeNode = toBeRemovedNode.prev
        afterNode = toBeRemovedNode.next

        beforeNode.next = afterNode
        afterNode.prev = beforeNode

        toBeRemovedNode.next = None
        toBeRemovedNode.prev = None

        self.length -= 1
        return toBeRemovedNode