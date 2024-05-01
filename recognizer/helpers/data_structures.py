class StackNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, data):
        node = StackNode(data)
        if self.top:
            node.next = self.top
            self.top = node
        else:
            self.top = node
        self.size += 1

    def pop(self):
        if self.top:
            data = self.top.data
            self.size -= 1
            if self.top.next:
                self.top = self.top.next
            else:
                self.top = None
            return data
        return None

    def peek(self):
        return self.top.data if self.top else None

    def is_empty(self):
        return self.size == 0


class QueueNode:
    def __init__(self, data=None, _next=None, _prev=None):
        self.data = data
        self.next = _next
        self.prev = _prev


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def enqueue(self, data):
        new_node = QueueNode(data, None, None)
        if self.head is None:
            self.head = new_node
            self.tail = self.head
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.count += 1

    def dequeue(self):
        current = self.head
        if self.count == 1:
            self.count -= 1
            self.head = None
            self.tail = None
        elif self.count > 1:
            self.head = self.head.next
            self.head.prev = None
            self.count -= 1
        return current.data

    def peek(self):
        return self.head.data if self.head else None

    def is_empty(self):
        return self.count == 0


class TreeNode:
    def __init__(self, data=None):
        self.data = data
        self.children = []
        self.node_type = "TreeNode"

    def __str__(self):
        return str(self.data)


class RegionNode:
    def __init__(self, data=None):
        self.data = data
        self.children = []
        self.node_type = "RegionNode"

    def __str__(self):
        return str(self.data)


class SymbolNode:
    def __init__(self, data=None):
        self.data = data
        self.children = []
        self.node_type = "SymbolNode"

    def __str__(self):
        return str(self.data)


class Tree:
    def __init__(self):
        self.root_node = RegionNode("Expression")

    def preorder(self, root_node=None):
        current = self.root_node if not root_node else root_node
        if current is None:
            return
        for node in current.children:
            self.preorder(node)

    def insert(self, data, insert_node=None, _type="TreeNode"):
        node = None
        if _type == "Region":
            node = RegionNode(data)
        elif _type == "Symbol":
            node = SymbolNode(data)
        elif _type == "TreeNode":
            node = TreeNode(data)
        elif _type == "Node":
            node = data
        current = insert_node if insert_node else self.root_node
        parent = current
        parent.children.append(node)
        return node
