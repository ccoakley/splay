"""
An implementation of splay trees.

This was ported from the C++ example on wikipedia:
https://en.wikipedia.org/wiki/Splay_tree#Implementation_and_variants

There are a few differences:
1. I don't use p_size.
2. I splay on find, which matches our book and slides.
3. I generate a DOT file for the tree.
"""

class splay_tree(object):
    def __init__(self):
        self.root = None

    def set_root(self, new_root):
        if self.root == new_root:
            return
        #print "new root: {}".format(new_root.value)
        self.root = new_root

    def dot(self):
        prefix = 'digraph G{\n  graph [ordering="out"];\n'
        out = ""
        if self.root:
            out = self.root.internal_dot()
        return prefix + out + "}\n"

    def splay(self, x):
        while x.parent:
            if not x.parent.parent:
                if x.parent.left == x:
                    self.right_rotate(x.parent)
                else:
                    self.left_rotate(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                self.right_rotate(x.parent.parent)
                self.right_rotate(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                self.left_rotate(x.parent.parent)
                self.left_rotate(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                self.right_rotate(x.parent)
                self.left_rotate(x.parent)
            else:
                self.left_rotate(x.parent)
                self.right_rotate(x.parent)

    def left_rotate(self, x):
        r = x.right
        if r:
            x.right = r.left
            if r.left:
                r.left.parent = x
            r.parent = x.parent
        if not x.parent:
            self.set_root(r)
        elif x == x.parent.left:
            x.parent.left = r
        else:
            x.parent.right = r
        if r:
            r.left = x
        x.parent = r

    def right_rotate(self, x):
        l = x.left
        if l:
          x.left = l.right
          if l.right:
              l.right.parent = x
          l.parent = x.parent
        if not x.parent:
            self.set_root(l)
        elif x == x.parent.left:
            x.parent.left = l
        else:
            x.parent.right = l
        if l:
            l.right = x
        x.parent = l

    def insert(self, value):
        z = self.root
        p = None

        while z:
            p = z
            if z.value < value:
                z = z.right
            else:
                z = z.left

        z = splay_node( value, parent=p )

        if not p:
            self.set_root(z)
        elif p.value < z.value:
            p.right = z
        else:
            p.left = z

        self.splay(z)

    def find(self, value):
        z = self.root
        while z:
            prev = z
            if z.value < value:
                z = z.right
            elif value < z.value:
                z = z.left;
            else:
                self.splay(z)
                return z
        self.splay(prev)
        return None

    @classmethod
    def replace(cls, u, v):
        if not u.parent:
            self.set_root(u)
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def erase(self, value):
        z = self.find( value )
        if not z:
            return

        z.splay()

        if not z.left:
            self.replace( z, z.right )
        elif not z.right:
            self.replace( z, z.left )
        else:
            y = s.right.subtree_minimum()
            if y.parent != z:
                self.replace( y, y.right )
                y.right = z.right
                y.right.parent = y
            self.replace( z, y )
            y.left = z.left
            y.left.parent = y

    def alternate_erase(self, value):
        z = self.find( value )
        if not z:
            return

        z.splay()

        s = z.left
        t = z.right

        sMax = Node
        if s:
            s.parent = None
            sMax = s.subtree_maximum()
            sMax.splay()
            self.set_root(sMax)
        if t:
            if s:
                sMax.right = t
            else:
                self.set_root(t)
            t.parent = sMax


class splay_node(object):
    def __init__(self, value, parent=None, left=None, right=None):
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right

    def recursive_print(self, indent=""):
        print indent + str(self.value)
        if self.left:
            self.left.recursive_print(" " + indent)
        if self.right:
            self.right.recursive_print(" " + indent)

    def size(self):
        left_size = 0
        right_size = 0
        if self.left:
            left_size = self.left.size()
        if self.right:
            right_size = self.right.size()
        return 1 + left_size + right_size

    def internal_dot(self):
        out = ""
        if self.left:
            out += "{} -> {};\n".format(self.value, self.left.value)
            out += self.left.internal_dot()
        else:
            out += 'l{} [label="",width=.1,style=invis]\n'.format(self.value)
            out += '{0} -> l{0} [style=invis]\n'.format(self.value)
        out += 'm{} [label="",width=.1,style=invis]\n'.format(self.value)
        out += '{0} -> m{0} [style=invis]\n'.format(self.value)
        if self.right:
            out += "{} -> {};\n".format(self.value, self.right.value)
            out += self.right.internal_dot()
        else:
            out += 'r{} [label="",width=.1,style=invis]\n'.format(self.value)
            out += '{0} -> r{0} [style=invis]\n'.format(self.value)
        return out


    def subtree_minimum(self):
        u = self
        while u.left:
            u = u.left
        return u

    def subtree_maximum(self):
        u = self
        while u.right:
            u = u.right
        return u


dot_count=0

def dump_dot(tree):
    global dot_count
    dot_count += 1
    filename = "dots/tree_{:03d}.dot".format(dot_count)
    with open(filename, "w") as out:
        out.write(tree.dot())

if __name__ == "__main__":
    # to produce png files if you have graphviz installed, perform operations and call dump_dot on the tree each time
    # then run the following line in bash
    # for dotfile in `ls *.dot`; do prefix=$(echo $dotfile | cut -d'.' -f1); dot -Tpng $dotfile -o${prefix}.png; done
    import random
    tree = splay_tree()
    values = [i*5 for i in range(0,50)]
    random.shuffle(values)
    for i in values:
        tree.insert(i)
        dump_dot(tree)
    for i in range(0,10):
        tree.find(random.choice(values))
        dump_dot(tree)
    # tree.insert(15)
    # dump_dot(tree)
    # tree.insert(10)
    # dump_dot(tree)
    # tree.insert(30)
    # dump_dot(tree)
    # tree.insert(40)
    # dump_dot(tree)
    # tree.insert(20)
    # dump_dot(tree)
    # tree.insert(5)
    # dump_dot(tree)
    # tree.find(7)
    # dump_dot(tree)
    # tree.find(15)
    # dump_dot(tree)
