.. _changelog:

History
=======

OpenAlea.Container 0.7.0
------------------------
* Fix several bugs in remove_tree, add_tree, ...
* Add unit tests
* Add a conversion to and from graphviz (by using pydot) and networkx
* Enhance the export to NetworkX by considering graph with non connected components.
* Implement the breadth first search algorithm on a graph
* Add level order traversal and tests.
* Create a first skeleton for the user documentation
* Add generator methods for tree.
* Add implementation and interface of tree.
* use array instead of set in topomesh
* update container sphinx documentation
* Add rooted graph interface and tree interface.
* Add Property graph class which is a graph with vertex and edge properties.
* Add Property graph class which is a graph with vertex and edge properties.
* Fix bug in clear method. Add a clear method to IdGenerator.
* added txt serialization to topomesh
* added different kind of idgenerators
* new implementation of id generator using sets
* added mesh algo and alea nodes for mesh
* neighbors operator in mesh
* Add MAC OS X dynamic library to the package data to install build libraries correctly.
* Update SConscript and Sconstruct for compatibility with scons 1.0 and the latest version of sconsx



06/05/2009
    - Create a first skeleton for the user documentation
    - Implement a method to convert a Graph into a NetworkX graph
    - Add generator methods for tree.
    - Fix a bug in Tree. Now empty Tree (Tree without root node) are not allowed.

30/04/2009
    - Add new packages as a proposal for algorithms (traversal, backend, readwrite).
    - Add tree interface and implementation.
    - Provide basic traversal algorithms.





