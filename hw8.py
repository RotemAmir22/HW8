import copy
from functools import total_ordering


class ByteNode:
    def __init__(self, byte):
        """
        constructor- build new ByteNode
        :param byte: given object
        """
        if not isinstance(byte, str):  # not a string
            raise TypeError("Type not str")
        if len(byte) != 8 or not all((list(map(lambda char: char == '1' or char == '0', byte)))):
            raise ValueError("Check length/value")  # chars are not 1/0, length not 8
        self.byte = byte
        self.next = None

    def get_byte(self):
        """
        :return: returns ByteNode value
        """
        return self.byte

    def get_next(self):
        """
        :return: returns next ByteNode
        """
        return self.next

    def set_next(self, next):
        """
        updates next ByteNode to given ByteNode
        :param next: given ByteNode
        """
        self.next = next

    def __repr__(self):
        """
        :return: string of ByteNode (byte) in format
        """
        return f"[{self.byte}]=>"


@total_ordering  # used for operations of comparing = eq, ne and more..
class LinkedListBinaryNum:
    def __init__(self, num=0):
        """
        gets a number and builds a list of BinaryNodes to represent the number
        :param num: number to build a binary representation
        """
        if not isinstance(num, int):
            raise TypeError('Input not a integer ')
        if num < 0:
            raise ValueError('Input must be a positive integer')

        self.head = None
        self.size = 0

        num_string = ''
        while num >= 1:  # convert to binary
            num_string = str(num % 2) + num_string
            num = num // 2

        if num_string == '':
            num_string = '0000000'
        while len(num_string) % 8 != 0:
            num_string = '0' + num_string

        while num_string:
            self.add_MSB(num_string[-8:])
            num_string = num_string[:-8]

    def add_MSB(self, byte):
        """
        gets a node and adds it the starts of the list
        :param byte:
        """
        new_byte = ByteNode(byte)
        if self.size == 0:
            self.head = new_byte
        else:
            temp_byte = self.head
            self.head = new_byte
            self.head.next = temp_byte
        self.size += 1

    def __len__(self):
        """
        :return: number of nodes on LinkedList
        """
        return self.size

    def __str__(self):  # end user
        """
        format: |BinaryNode|....
        :return: returns the list in format
        """
        if self.size == 1:
            write = f"|{str(self.head)[1:9]}|"
        else:
            write = "|"
            node = self.head
            while node is not None:
                write += repr(node)[1:9] + '|'
                node = node.next

        return write

    def __repr__(self):  # developer
        """
        binary list with information such as: size and order
        :return: binary list with information
        """
        if self.size == 1:
            write = f"LinkedListBinaryNum with 1 Byte, Bytes map: {self.head}"
        else:
            write = f"LinkedListBinaryNum with {self.size} Bytes, Bytes map: "
            node = self.head
            while node is not None:
                write += repr(node)
                node = node.next

        return write + f'{None}'

    def __getitem__(self, item):
        """
        :param item: index of wanted ByteNode
        :return: returns ByteNode
        """
        if not isinstance(item, int):
            raise TypeError('Not int')
        if not -self.size - 1 <= item < self.size:
            raise IndexError(f'Input not in range : 0-{self.size}')

        temp_node = self.head
        while item >= 0 or item >= -self.size:
            if item == 0 or item == -self.size:
                return str(temp_node)[1:9]
            else:
                item -= 1
                temp_node = temp_node.next

    # Order relations:

    def __eq__(self, other):
        """
        compares given object with other and return True if identical
        :param other: other object to compare to
        :return: True if identical, False if not
        """
        if not isinstance(other, int) or other < 0:
            if not isinstance(other, LinkedListBinaryNum):
                raise TypeError('Input not a integer')

        link_list1 = self.__str__()
        link_list2 = other.__str__()

        if len(link_list1) == len(link_list2):
            for index in range(len(link_list2)):
                if link_list1[index] != link_list2[index]:
                    return False
        else:
            return False
        return True

    def __gt__(self, other):
        """
        compare two objects and return true if self is greater than the other
        :param other: given object to compare two
        :return: if self is grater than other ten return True, if not return False
        """
        if not isinstance(other, int) or other < 0:
            if not isinstance(other, LinkedListBinaryNum):
                raise TypeError('Input not a integer')

        link_list1 = self.__str__()
        link_list2 = other.__str__()

        if len(link_list1) > len(link_list2):
            return True

        if len(link_list1) < len(link_list2):
            return False

        for index in range(1, len(link_list1) - 1):
            if link_list1[index] > link_list2[index]:
                return True
            elif link_list1[index] < link_list2[index]:
                return False

        return False

    def __add__(self, other):
        """
        sums two linked lists
        :param other: either number or linked list
        :return: addition of the two
        """
        if not isinstance(other, int) or other < 0:
            if not isinstance(other, LinkedListBinaryNum):
                raise TypeError('Input not a integer')
        if isinstance(other, int) and other < 0:
            raise ValueError('Not a positive number')

        "linked list as string"
        link_list1 = self.__str__()
        if isinstance(other, int):
            link_list2 = LinkedListBinaryNum(other).__str__()
        else:
            link_list2 = other.__str__()

        ans = ''
        remainder = '0'
        while link_list1 or link_list2:
            if link_list1 == '' or link_list2 == '':  # end if strings
                if link_list1:
                    if remainder == '1':
                        ans = link_list1 + ans
                elif link_list1:
                    ans = link_list2 + ans
                return ans

            if link_list1[-1] == '|' or link_list2 == '|':
                ans = link_list1[-1] + ans

            elif link_list1[-1] == '0':
                if link_list2[-1] == '0':
                    ans = remainder + ans
                    remainder = '0'
                else:
                    if remainder == '0':
                        ans = '1' + ans
                        remainder = '0'
                    else:
                        ans = '0' + ans
                        remainder = '1'
            else:
                if link_list2[-1] == '0':
                    ans = '0' + ans if remainder == '1' else '1' + ans
                else:
                    ans = '0' + ans if remainder == '0' else '1' + ans
                    remainder = '1'

            link_list1 = link_list1[:-1]
            link_list2 = link_list2[:-1]

        new_link = LinkedListBinaryNum()
        new_link.head = None
        while len(ans) > 8:
            new_link.add_MSB(ans[-9:-1])
            ans = ans[:-9]

        return new_link

    def __sub__(self, other):
        """
        subtracts from self the other given linked list
        :param other: given linked list
        :return: subtraction of the two
        """
        if not isinstance(other, int):
            if not isinstance(other, LinkedListBinaryNum):
                raise TypeError('Input not a integer')
        if other < 0 or other > self:  # self has to be larger
            raise ValueError('Not a positive number or order of operation not right')

        "linked list as string"
        link_list1 = self.__str__()
        if isinstance(other, int):
            link_list2 = LinkedListBinaryNum(other).__str__()
        else:
            link_list2 = other.__str__()

        """make them the same length"""
        while len(link_list1) != len(link_list2):
            while len(link_list2) % 9 != 0:
                link_list2 = '0' + link_list2
            link_list2 = '|' + link_list2

        ans = ''
        remainder = 0
        for index in range(len(link_list1) - 1, -1, -1):
            if link_list1[index] == '|':
                ans = '|' + ans
                continue
            if link_list1[index] == link_list2[index]:
                num = -remainder
            else:
                if link_list1[index] == '1':
                    num = 1 - remainder
                else:
                    num = -1 - remainder

            if num % 2 == 1:
                ans = '1' + ans
            else:
                ans = '0' + ans

            if num < 0:
                remainder = 1
            else:
                remainder = 0

        if remainder != 0:
            ans = '01' + ans

        """clean answer"""
        if len(ans) > 10:
            while ans[:10] == '|00000000|':
                ans = ans[9:]

        new_link = LinkedListBinaryNum()
        new_link.head = None
        while len(ans) > 8:
            new_link.add_MSB(ans[-9:-1])
            ans = ans[:-9]

        return new_link

    def __radd__(self, other):
        """
        able to do addition from the left
        :param other: given list to add to self
        :return: addition of the two
        """
        return self + other


class DoublyLinkedNode:
    def __init__(self, data):
        """
        creates DoubleLinkedNode with given data
        :param data: given data, can be any object
        """
        self.data = data
        self.prev = None
        self.next = None

    def get_data(self):
        """
        :return: data of selfNode
        """
        return self.data

    def set_next(self, next):
        """
        :param next: sets next Node to be given Node
        """
        self.next = next

    def get_next(self):
        """
        :return: next object of selfNode
        """
        return self.next

    def get_prev(self):
        """
        :return: prev object of selfNode
        """
        return self.prev

    def set_prev(self, prev):
        """
        :param prev: sets self.prev to be given Node
        """
        self.prev = prev

    def __repr__(self):
        """
        :return: returns data in format : =>[data]<=
        """
        return f"=>[{self.data}]<="


class DoublyLinkedList:
    def __init__(self):
        """
        builds an empty list
        """
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        """
        :return: number of nodes in DoubleLinkedList
        """
        return self.size

    def add_at_start(self, data):
        """
        :param data: updates head to be given data
        """
        node = self.head
        if self.size == 0:
            self.tail = DoublyLinkedNode(data)
        self.head = DoublyLinkedNode(data)
        self.head.set_next(node)
        if self.size > 1:
            self.head.get_next().set_prev(self.head)
        if self.size == 1:
            self.tail.set_prev(self.head)
        self.size += 1

    def remove_from_end(self):
        """
        removes Node form end of DoubleLinkedList
        """
        node = ''
        if self.size > 1:
            node = self.tail
            if node.get_prev:
                self.tail = node.get_prev()
                self.tail.set_next(None)
                self.size -= 1
        elif self.size == 1:
            node = self.head
            self.head = None
            self.size -= 1
        return node.get_data()

    def get_tail(self):
        """
        :return: DoubleLinkedList tail
        """
        return self.tail

    def get_head(self):
        """
        :return: DoubleLinkedLost head
        """
        return self.tail

    def __repr__(self):
        """
        :return: DoubleLinkedList in format: Head==>list data<==Tail
        """
        write = "Head="
        if self.size != 0:
            node = self.head
            while node is not None:
                write += f"=>[{node.get_data()}]<="
                node = node.next
        else:
            write += '=><='
        return write + "=Tail"

    def is_empty(self):
        """
        :return: if DoubleLinkedList is empty return True, if not returns False
        """
        if self.size == 0:
            return True
        return False


class DoublyLinkedListQueue:
    def __init__(self):
        """
        given method
        """
        self.data = DoublyLinkedList()

    def enqueue(self, val):
        """
        :param val: adds val to beginning of Queue
        """
        self.data.add_at_start(val)

    def dequeue(self):
        """
        removes value from end of Queue
        :return: value removed from Queue
        """
        if self.is_empty():
            raise StopIteration
        return self.data.remove_from_end()

    def __len__(self):
        """
        :return: returns number of objects in Queue
        """
        return self.data.size

    def is_empty(self):
        """
        :return: True if Queue is empty, and False if not
        """
        return self.data.is_empty()

    def __repr__(self):
        """
        :return: string representation on Queue in format: Newest=>[data]<=Oldest
        """
        write = "Newest=>["
        if self.data.size > 0:
            node = self.data.head
            while node is not None:
                write += f"{node.get_data()},"
                node = node.next
            write = write[:-1]
        return write + "]<=Oldest"

    def __iter__(self):
        """
        makes the Queue an iterable
        :return:
        """
        self.current = self.data.get_tail()
        return self

    def __next__(self):
        """
        moves along the Queue in FILO order
        :return: return current value or StopIteration if reached the end
        """
        if self.current:
            temp = self.current.get_data()
            self.current = self.current.get_prev()
        else:
            raise StopIteration
        return temp


from hw8_lib import Stack
from hw8_lib import BinarySearchTree


class NumsManagment:
    def __init__(self, file_name):
        self.file_name = file_name

    def is_line_pos_int(self, st):
        """
        checks if string in given line is a positive number
        :param st: given line
        :return:
        """
        try:
            return int(st) > 0
        except ValueError:
            return False

    def read_file_gen(self):
        """
        generator that returns a binary representation of all positive numbers in file
        """
        with open(self.file_name, 'r') as f:
            st = str(f.readline())
            while st != '':
                st = st[:-1]
                if self.is_line_pos_int(st):
                    yield LinkedListBinaryNum(int(st))
                st = str(f.readline())
        raise FileNotFoundError

    def stack_from_file(self):
        """
        builds a stack of all the positive numbers in file
        :return: stack of positive numbers
        """
        stack = Stack()
        try:
            item = self.read_file_gen()
            temp = next(item)
            while temp:
                stack.push(temp)
                temp = next(item)

        except FileNotFoundError:
            return stack

    def sort_stack_descending(self, s):
        """
        gets a stack and sorts it in order from maximum to minimum
        :param s: given stack
        :return: sorted stack
        """
        temp_stack = Stack()
        while not s.is_empty():
            temp = s.pop()

            while not temp_stack.is_empty() and temp_stack.top() > temp:
                s.push(temp_stack.pop())

            temp_stack.push(temp)
        return temp_stack

    def queue_from_file(self):
        """
        builds a queue of all the positive numbers in file
        :return: queue of positive numbers
        """
        queue = DoublyLinkedListQueue()
        try:
            item = self.read_file_gen()
            temp = next(item)
            while temp:
                queue.enqueue(temp)
                temp = next(item)

        except FileNotFoundError:
            return queue

    def set_of_bytes(self, q_of_nums):
        """
        creates a set of all the bytes that are used to create the numbers in given queue of binary numbers
        :param q_of_nums: given queue
        :return: set of bytes
        """
        set_of_nums = set()
        while not q_of_nums.is_empty():
            set_of_nums.update(q_of_nums.dequeue())
        return set_of_nums

    def nums_bst(self):
        """
        orders positive numbers from document into a BinarySearchTree using keys and values:
        key - number in decimal
        value - number in binary
        :return: BinarySearchTree of numbers
        """
        bst = BinarySearchTree()
        try:
            gen = self.read_file_gen()
            item = next(gen)
            key = 0
            brackets = 0

            while item:
                temp = item.__str__()
                temp = temp[::-1]
                for index in range(len(temp) - 1):
                    if temp[index] == '|':
                        brackets += 1
                        continue
                    elif temp[index] == '1':
                        key += (2 ** (index - brackets))
                bst.insert(key, item)
                item = next(gen)
                key = 0
                brackets = 0
        except FileNotFoundError:
            return bst

    def bst_closest_gen(self, bst):
        """
        gets a BinarySearchTree and look for two nodes that are closest to each other and returns all the
        Nodes between
        :param bst: given binarySearchTree
        :return: generator that returns one node when called
        """
        bst_edited = copy.deepcopy(bst)  # not edit first tree
        bst_from_root = bst_edited  # start point of BST for generator
        difference = -1
        gen = iter(bst)
        node1 = next(bst)
        node2 = next(bst)
        big_num = ''
        small_num = ''

        try:
            while gen:
                if difference < 0:
                    difference = node1[0] - node2[0]
                elif (node1[0] - node2[0]) < difference:
                    difference = node1[0] - node2[0]
                    big_num = node1
                    small_num = node2

                node2 = node1
                node1 = next(bst)
        except StopIteration:
            if difference > 1:
                for index in range(1, difference):  # add to copy of tree the differance
                    bst_edited.insert(small_num[0] + index, small_num[1] + index)

            temp = iter(bst_from_root)
            while small_num != temp:  # get to start of edited BST witch is small number
                temp = next(bst_from_root)

            def generator(node, num, binary_tree):
                while node[0] <= num[0]:
                    yield node
                    node = next(binary_tree)

            return generator(temp, big_num, bst_from_root)
