# Newick-To-DOT

## Overview

The task is to build a tool that converts from the [Newick Format](https://en.wikipedia.org/wiki/Newick_format) to the [DOT format](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) in order to be represented by [Graphviz](https://en.wikipedia.org/wiki/Graphviz). I did it by simply parsing the input (should it be a string or a file), storing each node into a Node class and iteratively printing every node.
Every node has an internal *id* in order to avoid the case where the newick text has no node names.
The output, is a DOT string representing a [cladogram](https://en.wikipedia.org/wiki/Cladogram) of the corresponding input Newick text. I chose this representation because it was easier to implement in the DOT format.

Unfortunately, lengths cannot be represented properly using the DOT format. You are more than welcome to try to implement it.

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
    newick-to-dot.py (<str> | --inputFile <inFile>)
    newick-to-dot.py (-h | --help)
    newick-to-dot.py --version

Options:
    -h --help                           Show this screen.
    --version                           Show version.
    -i inFile, --inputFile inFile       File to load newick from.
```

### Examples
There are quite a few examples given in the repository, so you can play with those. All the examples are made using `random.seed(1)` for consistent results.

- Raw text as input
    ```bash
    $ newick-to-dot.py '(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);'
    ```
    Expected output ([Link to viewer](https://dreampuf.github.io/GraphvizOnline/#graph%20%7B%0A%20%20%20%20rankdir%3DLR%3B%0A%20%20%20%20splines%3Dline%3B%0A%20%20%20%20node%20%5Bshape%3Dnone%5D%0A%20%20%20%20%22d8a2fd%22%20%5Bshape%3D%22point%22%5D%3B%0A%20%20%20%20%22333740%22%20%5Bshape%3D%22point%22%5D%3B%0A%20%20%20%20%22d8a2fd%22%20--%20%22333740%22%20%5Bshape%3D%22point%22%5D%3B%0A%20%20%20%20%222dc477%22%20%5Blabel%3D%22A%22%5D%3B%0A%20%20%20%20%22333740%22%20--%20%222dc477%22%20%3B%0A%20%20%20%20%22ac10d6%22%20%5Blabel%3D%22B%22%5D%3B%0A%20%20%20%20%22333740%22%20--%20%22ac10d6%22%20%3B%0A%20%20%20%20%22360377%22%20%5Bshape%3D%22point%22%5D%3B%0A%20%20%20%20%22333740%22%20--%20%22360377%22%20%3B%0A%20%20%20%20%22c07b3f%22%20%5Blabel%3D%22C%22%5D%3B%0A%20%20%20%20%22360377%22%20--%20%22c07b3f%22%20%3B%0A%20%20%20%20%22e008f6%22%20%5Blabel%3D%22D%22%5D%3B%0A%20%20%20%20%22360377%22%20--%20%22e008f6%22%20%3B%0A%7D)):
    ```
    graph {
        rankdir=LR;
        splines=line;
        node [shape=none]
        "d8a2fd" [shape="point"];
        "333740" [shape="point"];
        "d8a2fd" -- "333740" [shape="point"];
        "2dc477" [label="A"];
        "333740" -- "2dc477" ;
        "ac10d6" [label="B"];
        "333740" -- "ac10d6" ;
        "360377" [shape="point"];
        "333740" -- "360377" ;
        "c07b3f" [label="C"];
        "360377" -- "c07b3f" ;
        "e008f6" [label="D"];
        "360377" -- "e008f6" ;
    }
    ```
- File text as input
    ```bash
    $ newick-to-dot.py --inputFile newick-file-1
    ```
    Expected output: ([Link to viewer](https://dreampuf.github.io/GraphvizOnline/#graph%20%7B%0A%09rankdir%3DLR%3B%0A%09splines%3Dline%3B%0A%09node%20%5Bshape%3Dnone%5D%0A%09%22d8a2fd%22%20%5Bshape%3D%22point%22%5D%3B%0A%09%22333740%22%20%5Bshape%3D%22point%22%5D%3B%0A%09%22d8a2fd%22%20--%20%22333740%22%20%5Bshape%3D%22point%22%5D%3B%0A%09%222dc477%22%20%5Blabel%3D%222dc477%22%5D%3B%0A%09%22333740%22%20--%20%222dc477%22%20%3B%0A%09%22ac10d6%22%20%5Blabel%3D%22ac10d6%22%5D%3B%0A%09%22333740%22%20--%20%22ac10d6%22%20%3B%0A%09%22360377%22%20%5Bshape%3D%22point%22%5D%3B%0A%09%22333740%22%20--%20%22360377%22%20%3B%0A%09%22c07b3f%22%20%5Blabel%3D%22c07b3f%22%5D%3B%0A%09%22360377%22%20--%20%22c07b3f%22%20%3B%0A%09%22e008f6%22%20%5Blabel%3D%22e008f6%22%5D%3B%0A%09%22360377%22%20--%20%22e008f6%22%20%3B%0A%7D))
    ```
    graph {
        rankdir=LR;
        splines=line;
        node [shape=none]
        "d8a2fd" [shape="point"];
        "333740" [shape="point"];
        "d8a2fd" -- "333740" [shape="point"];
        "2dc477" [label="2dc477"];
        "333740" -- "2dc477" ;
        "ac10d6" [label="ac10d6"];
        "333740" -- "ac10d6" ;
        "360377" [shape="point"];
        "333740" -- "360377" ;
        "c07b3f" [label="c07b3f"];
        "360377" -- "c07b3f" ;
        "e008f6" [label="e008f6"];
        "360377" -- "e008f6" ;
    }
    ```
