from typing import Union

from src.ER.Operation import Operation


class Node:
    def __init__(self, el, operation: Operation):
        self.el = el
        self.op = operation
        self.left: Union[None, Node] = None
        self.right: Union[None, Node] = None
        self.father: Union[None, Node] = None
        self.first_pos = set()
        self.last_pos = set()
        self.follow_pos = set()

    def __repr__(self):
        return self.el

    def is_nullable(self) -> bool:
        if self.op == Operation.CONCAT:
            return self.left.is_nullable() and self.right.is_nullable()
        elif self.op == Operation.OR:
            return self.left.is_nullable() or self.right.is_nullable()
        elif self.op == Operation.FECHO:
            return True
        elif self.op == Operation.CLOSE:
            return False
        elif self.op == Operation.ELEMENT:
            return self.el == "&"

    def get_first_pos(self):
        if self.op == Operation.CONCAT:
            if self.left.is_nullable():
                return self.left.get_first_pos().union(self.right.get_first_pos())
            else:
                return self.left.get_first_pos()
        elif self.op == Operation.OR:
            return self.left.get_first_pos().union(self.right.get_first_pos())
        elif self.op == Operation.FECHO:
            return self.right.get_first_pos()
        elif self.op in (Operation.CLOSE, Operation.ELEMENT):
            return self.first_pos

    def get_last_pos(self):
        if self.op == Operation.CONCAT:
            if self.right.is_nullable():
                return self.right.get_last_pos().union(self.left.get_last_pos())
            else:
                return self.right.get_last_pos()
        elif self.op == Operation.OR:
            return self.right.get_last_pos().union(self.left.get_last_pos())
        elif self.op == Operation.FECHO:
            return self.right.get_last_pos()
        elif self.op in (Operation.CLOSE, Operation.ELEMENT):
            return self.last_pos