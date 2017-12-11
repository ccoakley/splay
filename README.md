# Splay Trees

This program helps illustrate splay trees by generating a bunch of dot files as random nodes are added to a tree.


To generate png files from the dotfiles produced by this program, you'll need graphviz installed. By default, this dumps the dot files in the dots/ directory.

> for dotfile in `ls *.dot`; do prefix=$(echo $dotfile | cut -d'.' -f1); dot -Tpng $dotfile -o${prefix}.png; done

