# !/usr/bin/env python3

"""
Suffix tree to search in dictionary
"""

from typing import List


class SSet:
    """String set. Should be based on Suffix tree"""

    def __init__(self, fname: str) -> None:
        """Saves filename of a dictionary file"""
        self.fname = fname
        self.words = None
        self.tree = SuffixTree(self.fname)

    def load(self) -> None:
        """
        Loads words from a dictionary file.
        Each line contains a word.
        File is not sorted.
        """
        with open(self.fname, 'r') as f:
            self.words = [line.rstrip() for line in f]

    def search(self, substring: str) -> List[str]:
        self.load_on_tree()
        """Returns all words that contain substring."""
        words = self.tree.search(substring)
        # words.append("some wrong word!")
        return words

    def load_on_tree(self):
        for word in self.words:
            self.tree.insert(word)


class SuffixTree:
    def __init__(self, fname):
        self.root = SuffixTreeNode()
        self.load(fname)

    def insert(self, word):
        # Insert all suffixes of the word into the suffix tree
        for i in range(len(word)):
            current_node = self.root
            suffix = word[i:]
            for char in suffix:
                if char not in current_node.children:
                    current_node.children[char] = SuffixTreeNode()
                current_node = current_node.children[char]
            current_node.is_end_of_word = True  # Mark the end of the word

    def search(self, substring):
        # Search for all words containing the substring
        result = []

        def dfs(node, prefix):
            if node.is_end_of_word:
                result.append(prefix)
            for char, child in node.children.items():
                dfs(child, prefix + char)

        # Find the node where the substring ends
        current_node = self.root
        for char in substring:
            if char in current_node.children:
                current_node = current_node.children[char]
            else:
                return []  # If the substring is not in the tree, return empty list

        # Use DFS to find all words that contain the substring
        dfs(current_node, substring)
        return result

    def load(self, fname):
        with open(fname, 'r') as f:
            words = [line.rstrip() for line in f]
        for word in words:
            self.insert(word)


class SuffixTreeNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
