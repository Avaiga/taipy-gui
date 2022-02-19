import typing as t


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    def __init__(self):
        self.head = Node("head_node")
        self.size = 0

    def __len__(self):
        return self.size

    def isEmpty(self) -> bool:
        return self.size == 0

    def peek(self) -> t.Any:
        return None if self.isEmpty() else self.head.next.value

    def push(self, value) -> None:
        node = Node(value)
        node.next = self.head.next
        self.head.next = node
        self.size += 1

    def pop(self) -> t.Union[t.Any, None]:
        if self.isEmpty():
            return None
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value
