#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""Newick to DOT

Usage:
    newick-to-dot.py (<str> | --inputFile <inFile>) [--directed] [--empty] [-p <outPicture> | --picture <outPicture>]
    newick-to-dot.py (-h | --help)
    newick-to-dot.py --version

Options:
    -h --help                           Show this screen.
    --version                           Show version.
    -i inFile, --inputFile inFile       File to load newick from.
    -d --directed                       Wether the graph is a directed graph or not [default: False].
    -p outPicture --picture outPicture  If specified, outputs to the specified directory an image representing the newick tree.
    -e --empty                          Wether to show or not empty labels [default: False].
"""

import sys
from docopt import docopt
import graphviz
import string
import random

class Node(object):
    def __init__(self, length=None, name=None):
        self.name = name
        self._length = length
        # generating an unique id for this node
        self.id = ''.join(random.choices(string.digits + 'abcdef', k=6))
        self.descendants = []
        self.ancestor = None
        self.dot = self._to_dot
        self.leaf_count = self._leaf_count
        self.label_properties = {"label": self.length, "weight": self.length} if self.length else {}
        self.label = self._to_dot_label

    @classmethod
    def create(cls, name=None, length=None, descendants=None):
        node = cls(name=name, length=length)
        for descendant in descendants or []:
            node.add_descendant(descendant)
        return node

    @property
    def length(self):
        return float(self._length or 0.0)

    @length.setter
    def length(self, l):
        if l is None:
            self._length = l
        else:
            self._length = '%s' % l

    def add_descendant(self, node):
        node.ancestor = self
        self.descendants.append(node)

    def add_label_property(self, key, value):
        self.label_properties[key] = value

    def _leaf_count(self):
        sum = 0
        if self._is_leaf:
            self.leaf_count = sum
        for n in self.descendants:
            sum += n.leaf_count()
        return sum

    def _is_leaf(self):
        return not bool(self.descendants)

    def __repr__(self):
        return '[id=%s;name=%s;length=%s;descendants=%s]' % (self.id, (self.name or ""), (self._length or ""), str(len(self.descendants) or "" ))
    
    def _to_dot_label(self, d=None):
        if d is None:
            d = self.label_properties
        if not len(d):
            return ''

        out = '['
        for i, (key, value) in enumerate(d.items()):
            if isinstance(value, (int, float, complex)):
                
                if key != 'weight':
                    out += '%s=%s' % (key, str(value))
                else:
                    out += '%s=%s' % (key, 1)
            else:
                out += '%s="%s"' % (key, str(value))
            if i < len(d) - 1: # last
                out += ','
        out += ']'
        return out

    def _to_dot(self, directed=False, emptyLabels=False):
        out = ''
        if not self.ancestor: # first
            out += ('digraph') if directed else 'graph'
            out += ' {'

        if emptyLabels:
            if not self.name:
                out += '\n\t"%s" [label=""];' % (self.id)
            else:
                out += '\n\t"%s" [label="%s"];' % (self.id, self.name)
        else:
            if not self.name:
                out += '\n\t"%s" [label="%s"];' % (self.id, self.id)
            else:
                out += '\n\t"%s" [label="%s"];' % (self.id, self.name)

        for n in self.descendants:
            if directed:
                out += '\n\t"%s" --> "%s" %s;' % (self.id, n.id, self._to_dot_label())
            else:
                out += '\n\t"%s" -- "%s" %s;' % (self.id, n.id, self._to_dot_label())
            out += n.dot(directed=directed, emptyLabels=emptyLabels)

        if not self.ancestor: # first
            out += '\n}\n'
        return out

def loads(s):
    # Theoretically, you will never parse more than two root nodes.
    return [parse_node(ss.strip()) for ss in s.split(';') if ss.strip()]

def _parse_name_and_length(s):
    l = None
    if ':' in s:
        s, l = s.split(':', 1)
    return s or None, l or None

def _parse_siblings(s):
    bracket_level = 0
    current = []

    for c in (s + ","):
        """
        we loop through every character
        when we stumble upon a comma
        then we should have a node.
        """
        if c == "," and bracket_level == 0:
            # putting the current parsed node into the generator
            yield parse_node("".join(current))
            # resetting character for node name
            current = []
        else:
            # If not, we have a higher level
            if c == "(":
                bracket_level += 1  # up one level
            elif c == ")":
                bracket_level -= 1  # down one level
            current.append(c)

def parse_node(s):
    s = s.strip()
    parts = s.split(')')  # la parte a sinistra contiene i dati del mio nodo
    if len(parts) == 1:  # se non ho una parentesi chiusa vuol dire che ho finito e non ho altri nodi figlio
        descendants, label = [], s
    else:
        if not parts[0].startswith('('):  # errore di formattazione: "A),B"
            raise ValueError('Le parentesi non coincidono')
        # analizzo la parte a destra
        descendants = list(_parse_siblings(')'.join(parts[:-1])[1:]))
        label = parts[-1]
    name, length = _parse_name_and_length(label)
    return Node.create(name=name, length=length, descendants=descendants)

# Printing

def printPicture(string, pictureOutput):
    s = graphviz.Source(string)
    s.render(filename=pictureOutput, cleanup=True, format="png")

def main(argv):

    arguments = docopt(__doc__, version="Newick To Dot 1.0")

    if arguments['<str>'] or arguments['--inputFile']:
        inputtext = None
        if arguments['<str>']:
            inputtext = arguments['<str>']
        elif arguments['--inputFile']:
            f = open(arguments['--inputFile'], 'r')
            inputtext = f.read()

        tree = loads(inputtext)
        output = tree[0].dot(directed=arguments['--directed'] or False, emptyLabels=arguments['--empty'] or False)
        print(output)
        if arguments['--picture']:
            printPicture(output, arguments['--picture'])


if __name__ == "__main__":
    main(sys.argv[1:])
