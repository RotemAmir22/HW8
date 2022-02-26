class Stack:
    def __init__(self):
        self.__s = []

    def push(self, item):
        self.__s.append(item)

    def top(self):
        return self.__s[-1]

    def pop(self):
        return self.__s.pop()

    def is_empty(self):
        return len(self.__s) == 0

    def __repr__(self):
        res = '['
        for i in self.__s:
            res += str(i) + ','
        if len(self.__s) > 0:
            res = res[:-1]
        return res + ']<=Top'

    def __len__(self):
        return len(self.__s)


# from printree import * #for Binary_search_tree's __repr__
class TreeNode():
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

    def successor(self):
        succ = self
        if self.right:
            succ = succ.right
            while succ.left:
                succ = succ.left
        else:
            while succ and self.key >= succ.key:
                succ = succ.parent

        return succ


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, val):
        ''' insert node with key,val into tree, uses recursion '''

        def insert_rec(node, key, val):
            if key == node.key:
                node.val = val  # update the val for this key
            elif key < node.key:
                if node.left == None:
                    node.left = TreeNode(key, val)
                    node.left.parent = node
                else:
                    insert_rec(node.left, key, val)
            else:  # key > node.key:
                if node.right == None:
                    node.right = TreeNode(key, val)
                    node.right.parent = node
                else:
                    insert_rec(node.right, key, val)
            return

        if self.root is None:  # empty tree
            self.root = TreeNode(key, val)
        else:
            insert_rec(self.root, key, val)

    def minimum(self):
        ''' return node with minimal key '''
        if self.root == None:
            return None
        node = self.root
        left = node.left
        while left != None:
            node = left
            left = node.left
        return node

    def __iter__(self):
        self.runner = self.minimum()
        return self

    def __next__(self):
        if self.runner is None:
            self.runner = self.minimum()
            raise StopIteration
        res = [self.runner.key, self.runner.val]
        self.runner = self.runner.successor()
        return res

    def __repr__(self):
        def repr_help(node, res):
            if node is None:
                return
            repr_help(node.left, res)
            res[0] += '(' + str(node.key) + ',' + str(node.val) + ')\n'
            repr_help(node.right, res)
        res = ['']
        repr_help(self.root, res)
        return res[0]
