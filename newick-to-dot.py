#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""Newick to DOT

Usage:
    newick-to-dot.py (<str> | --inputFile <inFile>) [--directed] [--empty]
    newick-to-dot.py (-h | --help)
    newick-to-dot.py --version

Options:
    -h --help                           Show this screen.
    --version                           Show version.
    -i inFile, --inputFile inFile       File to load newick from.
    -d --directed                       Wether the graph is a directed graph or not [default: False].
    -e --empty                          Wether to show or not empty labels [default: False].
"""

import sys
from docopt import docopt
import string
import random

# consistent labeling
random.seed(1)

class Node(object):
    def __init__(self, length=None, name=None):
        self.name = name
        self._length = length
        # generating an unique id for this node
        self.id = self._gen_random_node_id()
        self.descendants = []
        self.ancestor = None
        self.dot = self._to_dot
        self.leaf_count = self._leaf_count
        self.is_leaf = self._is_leaf()
        self.arch_props = {"label": self.length} if self.length else {}
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
    def length(self, len):
        if len is None:
            self._length = len
        else:
            self._length = '%s' % len

    def add_descendant(self, node):
        node.ancestor = self
        self.descendants.append(node)

    def _leaf_count(self):
        sum = 0
        if self._is_leaf:
            self.leaf_count = sum
        for n in self.descendants:
            sum += n.leaf_count()
        return sum

    def _is_leaf(self):
        return not bool(self.descendants)
    
    def _to_dot_label(self, d={}):
        if d is None:
            d = self.arch_props
        if not len(d):
            return ''

        out = '['
        for i, (key, value) in enumerate(d.items()):
            if isinstance(value, (int, float, complex)):
                out += '%s=%s' % (key, str(value))
            else:
                out += '%s="%s"' % (key, str(value))
            if i < len(d) - 1: # last
                out += ','
        out += ']'
        return out

    def _gen_random_node_id(self):
        return ''.join(random.choices(string.digits + 'abcdef', k=6))

    def _graph_node(self, nodeFromId, nodeToId=None, directed=False, props={}):
        if nodeToId:
            return '\n\t"%s" --%s "%s" %s;' % (nodeFromId, ('>') if directed else '',  nodeToId, self._to_dot_label(props))
        else: # printing out single node
            return '\n\t"%s" %s;' % (nodeFromId, self._to_dot_label(props))
    
    def _graph_same_rank(self, *kw):
        out = '\n\t{rank = same; '
        for id in kw:
            out += '"%s";' % id
        out += '}'
        return out

    def _phantom_node(self, fromNode=None, toNode=None, phantom=None, directed=False, before=True):
        phantom_node_id = self._gen_random_node_id()
        # first, lets print our phantom node
        if before:
            out = self._graph_node(phantom_node_id, nodeToId=toNode.id, props=toNode.arch_props)
        else:
            out = self._graph_node(phantom_node_id, props={"shape": "point"})

        # if we already have a previous phantom node, we attach to it!
        if not phantom is None:
            out += self._graph_node(nodeFromId=phantom, nodeToId=phantom_node_id, directed=directed)
        else:
            # then we arch from our initial node to the phantom node
            out += self._graph_node(fromNode.id, nodeToId=phantom_node_id, directed=directed)
        
        # then we state that they are at the same rank
        out += self._graph_same_rank(fromNode.id, phantom_node_id)
        
        if before:
            out += self._graph_node(phantom_node_id, props={"shape": "point"})
        else:
            out += self._graph_node(phantom_node_id, nodeToId=toNode.id, props=toNode.arch_props)

        return out, phantom_node_id

    def _to_dot(self, directed=False, emptyLabels=False):
        out = ''
        if not self.ancestor: # first
            out += ('digraph') if directed else 'graph'
            out += ' {'

        # set empty label if asked to
        if emptyLabels:
            if not self.name:
                out += self._graph_node(self.id, props={"label": "", "shape": "point"})
            else:
                out += self._graph_node(self.id, props={"label": self.name})
        else:
            if not self.name:
                out += self._graph_node(self.id, props={"label": self.id})
            else:
                out += self._graph_node(self.id, props={"label": self.name})

        phantom_node_id = None
        for i, n in enumerate(self.descendants):
            before = i < ((len(self.descendants) - 1) / 2)
            if phantom_node_id is None:
                out_tmp, phantom_node_id = self._phantom_node(fromNode=self, toNode=n, directed=directed, before=before)
            else:
                out_tmp, phantom_node_id = self._phantom_node(fromNode=self, toNode=n,  phantom=phantom_node_id, directed=directed, before=before)
            out += out_tmp
            out += n.dot(directed=directed, emptyLabels=emptyLabels)

        if not self.ancestor: # first
            out += '\n}\n'
        return out

    def __repr__(self):
        return '[id=%s;name=%s;length=%s;descendants=%s]' % (self.id, (self.name or ""), (self._length or ""), str(len(self.descendants) or "" ))

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

if __name__ == "__main__":
    main(sys.argv[1:])