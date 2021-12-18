from collections import deque


class Node:
    def __init__(self):
        # a trie is a data structure of nodes
        self.leaves = [None] * (ord("z") - ord("a") + 1)
        self.complete = False
        pass

    def get_leaf(self, char):
        return self.leaves[ord(char) - ord("a")]

    def set_leaf(self, char):
        self.leaves[ord(char) - ord("a")] = Node()


class Trie:
    # contains the root of the trie and also ensures all requests are lowercase
    def __init__(self, words):
        # takes a collection of words and creates a trie of them
        self.root = Node()
        for word in words:
            self.add_word(word)

    def find_words(self, node=None, word=None, result=None):
        # fix local-scope reuse of parameters.
        if not node:
            node = self.root
        if not result:
            result = []
        if not word:
            word = ""
        # if complete word, add word to result
        if node.complete:
            result.append(word)
        for i in range(len(node.leaves)):
            if node.leaves[i]:
                result = self.find_words(node.leaves[i], word + chr(i+ord("a")), result)
        return result

    def find_suggestions(self, prefix):
        node = self.root
        for c in prefix:
            if not node:
                return []
            node = node.get_leaf(c)
        if node:
            return self.find_words(node, prefix)

    def add_word(self, word):
        word.lower()
        curr = self.root
        for letter in word:
            if not curr.get_leaf(letter):
                curr.set_leaf(letter)
            curr = curr.get_leaf(letter)
        curr.complete = True
