import random as r
import os
import time
import splay_node
import matplotlib.pyplot as plt


class SplayTree(object):

    splay_node = splay_node.SplayNode

    def __init__(self, new_node=splay_node):
        """setters"""
        self._root = None
        self._new_node = new_node

    @property
    def root(self):
        return self._root

    """три случая поворотов"""
    def _move_zig(self, node):
        p = node.par
        p._par = node
        if node == p.leftChild:
            p._leftChild = node.rightChild
            if node.rightChild is not None:
                node.rightChild._par = p
            node._rightChild = p
        else:
            p._rightChild = node.leftChild
            if node.leftChild is not None:
                node.leftChild._par = p
            node._leftChild = p
        self._root = node

    def _move_zig_zig(self, node):
        g = node.par.par
        p = node.par
        if g != self.root:
            if g.par.leftChild == g:
                g.par._leftChild = node
            else:
                g.par._rightChild = node
        else:
            self._root = node
        if g.leftChild == p:
            """zig"""
            g._leftChild = p.rightChild
            if p.rightChild is not None:
                p.rightChild._par = g
            p._par = g.par
            g._par = p
            p._rightChild = g
            """zig"""
            p._leftChild = node.rightChild
            if node.rightChild is not None:
                node.rightChild._par = p
            node._rightChild = p
            node._par = p.par
            p._par = node
        else:
            """zig"""
            g._rightChild = p.leftChild
            if p.leftChild is not None:
                p.leftChild._par = g
            p._par = g.par
            g._par = p
            p._leftChild = g
            """zig"""
            p._rightChild = node.leftChild
            if node.leftChild is not None:
                node.leftChild._par = p
            node._leftChild = p
            node._par = p.par
            p._par = node

    def _move_zig_zag(self, node):
        g = node.par.par
        p = node.par
        if g != self.root:
            if g.par.leftChild == g:
                g.par._leftChild = node
            else:
                g.par._rightChild = node
        else:
            self._root = node
        if g.leftChild == p:
            """zag"""
            p._rightChild = node.leftChild
            if node.leftChild is not None:
                node.leftChild._par = p
            p._par = node
            node._leftChild = p
            node._par = g
            g._leftChild = node
            """zig"""
            g._leftChild = node.rightChild
            if node.rightChild is not None:
                node.rightChild._par = g
            node._rightChild = g
            node._par = g.par
            g._par = node
        else:
            """zag"""
            p._leftChild = node.rightChild
            if node.rightChild is not None:
                node.rightChild._par = p
            p._par = node
            node._rightChild = p
            node._par = g
            g._rightChild = node
            """zig"""
            g._rightChild = node.leftChild
            if node.leftChild is not None:
                node.leftChild._par = g
            node._leftChild = g
            node._par = g.par
            g._par = node

    def splay_operation(self, node):        # основная операция поворотов, используемая почти во всех других
        if (self.root is None) or (node == self.root):
            return None
        else:
            p = node.par
            if p == self.root:
                self._move_zig(node)
                return None
            elif (p.leftChild == node and p.par.leftChild == p) or (p.rightChild == node and p.par.rightChild == p):
                self._move_zig_zig(node)
                self.splay_operation(node)
            else:
                self._move_zig_zag(node)
                self.splay_operation(node)

    def find_data(self, data):                         # найти узел по data, если существует
        if self.root is not None:
            node = self.root
            while node is not None:
                if node.data == data:
                    self.splay_operation(node)
                    return node
                elif node.data < data:
                    node = node.rightChild
                elif node.data > data:
                    node = node.leftChild
        return None

    def max_data(self, node=None):                     # нахождение максимума в поддереве узла node
        if self.root is None:
            return
        else:
            if node is None:
                node = self.root
            while node.rightChild is not None:
                node = node.rightChild
            return node

    def min_data(self, node=None):                     # нахождение минимума в поддереве узла node
        if self.root is None:
            return
        else:
            if node is None:
                node = self.root
            while node.leftChild is not None:
                node = node.leftChild
            return node

    def add_data(self, data):                          # вызов добавления узла по data
        self.add_node(self._new_node(data=data))

    def add_node(self, node):                          # операция добавления узла в splay дерево
        if self.root is None:
            self._root = node
            return
        temp = self.root
        while (temp.leftChild is not None) and (temp.data > node.data):
            temp = temp.leftChild
        while (temp.rightChild is not None) and (temp.data < node.data):
            temp = temp.rightChild
        self.splay_operation(temp)
        # print(temp.data, "a")
        temp._par = node
        if temp.data < node.data:
            if temp.rightChild is not None:
                temp.rightChild._par = node
                node._rightChild = temp.rightChild
            node._leftChild = temp
            temp._rightChild = None
        else:
            if temp.leftChild is not None:
                temp.leftChild._par = node
                node._leftChild = temp.leftChild
            node._rightChild = temp
            temp._leftChild = None
        self._root = node

    def delete_data(self, data):                        # вызывает операцию удаления для узла с параметром data
        node = self.find_data(data)
        if node is not None:
            self.delete_node(node)

    def delete_node(self, node):
        if node.rightChild is not None:
            temp = node.rightChild
            while temp.leftChild is not None:
                temp = temp.leftChild
            self._root = node.rightChild
            temp._leftChild = node.leftChild
            if node.leftChild is not None:
                node.leftChild._par = temp
        else:
            if node.leftChild is not None:
                node.leftChild._par = None
                self._root = node.leftChild
            else:
                self._root = None
        return


def show_tree(t, node=None):
    if node is None:
        node = t.root
    print(node.data, end = " ")
    if node.leftChild != None:
        print("leftChild = \"%s\" " % node.leftChild.data, end = ",")
    if node.rightChild != None:
        print("rightChild = \"%s\"" % node.rightChild.data, end = ",")
    print("")
    if node.leftChild is None and node.rightChild is None:
        return
    else:
        if node.leftChild is not None:
            show_tree(t, node.leftChild)
        if node.rightChild is not None:
            show_tree(t, node.rightChild)
    return


def call_random_op(kol, m, s):
    ch = [0, 1, 2]       # 0 - find, 1 - add, 2 - del
    data = read_test_file()                # massive of int, which is in the tree
    data_2 = generate_data(m*2, s*2)
    set1 = set(data_2)
    set2 = set(data)
    data_2 = list(set1.difference(set2))   # massive of int, which is not in the tree
    # print(sorted(data), len(data))
    # print(sorted(data_2), len(data_2))
    start = time.time()
    fi, de, ad = 0, 0 ,0
    for k in range(kol):
        op = r.SystemRandom().choice(ch)
        d_1 = r.SystemRandom().choice(data)
        d_2 = r.SystemRandom().choice(data_2)
        if op == 0:
            t.find_data(d_1)
            fi += 1
        elif op == 1:
            t.add_data(d_2)
            data.append(d_2)
            data_2.remove(d_2)
            ad += 1
        elif op == 2:
            t.delete_data(d_1)
            data.remove(d_1)
            de += 1
    print(fi, ad, de)
    end = time.time()
    return end - start


def generate_data(max_data, size):
    return list(r.SystemRandom().sample(range(max_data), size))


def create_test_file(max_data, size):
    rand_data = generate_data(max_data, size)
    f = open('test.txt', 'w')
    for i, data in enumerate(rand_data):
        f.write(str(data) + "\n")


def read_test_file():
    spisok = list()
    with open("test.txt") as f:
        for line in f:
            spisok.append(int(line))
    return spisok


def build_tree(t):
    for node in read_test_file():
        t.add_data(node)


def write_result(t, f, node=None):
    if node is None:
        node = t.root
    f.write("  data=\"%s\" \t"% node.data )
    if node.leftChild is not None:
        f.write("leftChild = \"%s\" " % node.leftChild.data)
    if node.rightChild is not None:
        f.write("rightChild = \"%s\"" % node.rightChild.data)
    f.write("\n")
    if node.leftChild:
        if node.leftChild is not None:
            write_result(t, f, node.leftChild)
    if node.rightChild:
        if node.rightChild is not None:
            write_result(t, f, node.rightChild)
    return


def save_tree(t, filename, time=0):
        f = open('%s.txt' % filename, 'w')
        write_result(t, f)
        if time != 0:
            f.write("время = " + str(time))
        f.close()
        os.system('%s.txt -T' % filename)


def graphic():

    _, ax = plt.subplots()

    #ax.plot(x_data, y_data)

    ax.set_title("T(n)")
    ax.set_xlabel("n")
    ax.set_ylabel("T")
    plt.grid(True, linestyle='-', color='0.75')
    plt.show()


if '__main__' == __name__:

    t = SplayTree()
    m = 25
    s = kol = 20
    create_test_file(m, s)          # 1 argument - max possible data, 2 argument - data count
    build_tree(t)                      # building splay tree using data from text file
    """for i in range(0, kol, 10):
        sec = call_random_op(kol, m, s)  # makes n random operations from list [find, add, del]
        sec_list = list().append(sec)
        kol_list = list().append(kol)"""
    sec = call_random_op(kol, m, s)  # makes n random operations from list [find, add, del]
    # graphic()
    save_tree(t, 'result', )       # save in result.txt
    # show_tree(t)                     # uncomment to view in console


