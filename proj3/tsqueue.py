from threading import Lock

class Node:
    def __init__(self, value, next_node):
        self.value = value
        self.next_node = next_node

class Empty(Exception):
    pass

class TSQueue:
    def __init__(self):
        self.head = Node(None, None)
        self.tail = self.head

        self.head_lock = Lock()
        self.tail_lock = Lock()

    def put(self, value):
        with self.head_lock:
            self.head.value = value
            self.head.next_node = Node(None, None)
            self.head = self.head.next_node

    def get(self):
        with self.tail_lock:
            if self.tail is self.head:
                raise Empty('Queue is empty.')
            value = self.tail.value
            self.tail = self.tail.next_node
            return value