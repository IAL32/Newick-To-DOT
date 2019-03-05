# Newick-To-DOT

## Overview

The task is to build a tool that converts from the [Newick Format](https://en.wikipedia.org/wiki/Newick_format) to the [DOT format](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) in order to be represented by [Graphviz](https://en.wikipedia.org/wiki/Graphviz). I did it by simply parsing the input (should it be a string or a file), storing each node into a Node class and iteratively printing every node.
Every node has an internal *id* in order to avoid the case where the newick text has no node names.

## About the Newick Format

As the Wikipedie page states:
> The Newick tree format is a way of representing graph-theoretical trees with edge length using parentheses and commas.

We also have some examples, also from Wikipedia:

- no nodes are named
    
    `(,,(,));`
- leaf nodes are named
    
    `(A,B,(C,D));`
- all nodes are named

    `(A,B,(C,D)E)F;`
- all but root node have a distance to parent
    
    `(:0.1,:0.2,(:0.3,:0.4):0.5);`
- all have a distance to parent

    `(:0.1,:0.2,(:0.3,:0.4):0.5):0.0;`
- distances and leaf names (popular)

    `(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);`
- distances and all names
    
    `(A:0.1,B:0.2,(C:0.3,D:0.4)E:0.5)F;`
- a tree rooted on a leaf node (rare)
    
    `((B:0.2,(C:0.3,D:0.4)E:0.5)A:0.1)F;`

## Usage
```
Newick to DOT

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
```

### Examples
There are quite a few examples given in the repository, so you can play with those.

- Raw text as input
    ```bash
    $ newick-to-dot.py '(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);'
    ```
    Expected output:
    ```
    graph {
            "c031eb" [label="c031eb"];
            "c031eb" -- "342d6f" ;
            "342d6f" [label="A"];
            "c031eb" -- "dfb943" ;
            "dfb943" [label="B"];
            "c031eb" -- "2b0028" ;
            "2b0028" [label="2b0028"];
            "2b0028" -- "e30a56" [label=0.5,weight=1];
            "e30a56" [label="C"];
            "2b0028" -- "92809c" [label=0.5,weight=1];
            "92809c" [label="D"];
    }
    ```
- File text as input
    ```bash
    $ newick-to-dot.py --inputFile newick-file-1
    ```
    Expected output:
    ```
    graph {
            "bd0f65" [label="bd0f65"];
            "bd0f65" -- "790e7e" ;
            "790e7e" [label="790e7e"];
            "bd0f65" -- "de427d" ;
            "de427d" [label="de427d"];
            "bd0f65" -- "e1342d" ;
            "e1342d" [label="e1342d"];
            "e1342d" -- "150e01" ;
            "150e01" [label="150e01"];
            "e1342d" -- "756e43" ;
            "756e43" [label="756e43"];
    }
    ```
- Directed graph option
    ```bash
    $ newick-to-dot.py -i '(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);'
    ```
    Expected output:
    ```
    digraph {
            "6789e8" [label="6789e8"];
            "6789e8" --> "b62ae7" ;
            "b62ae7" [label="A"];
            "6789e8" --> "1d1856" ;
            "1d1856" [label="B"];
            "6789e8" --> "36a405" ;
            "36a405" [label="36a405"];
            "36a405" --> "11e845" [label=0.5,weight=1];
            "11e845" [label="C"];
            "36a405" --> "608c82" [label=0.5,weight=1];
            "608c82" [label="D"];
    }
    ```