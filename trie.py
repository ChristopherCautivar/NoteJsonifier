from collections import deque


class Node:
    def __init__(self):
        # a trie is a data structure of nodes
        self.leaves = [None] * (ord("z") - ord("a"))
        self.complete = False
        pass

    def get_leaf(self, char):
        return self.leaves[ord(char) - ord("a")]

    def set_leaf(self, char):
        self.leaves[ord(char) - ord("a")] = Node()
        pass

    def find_word(self):
        if self.complete:
            return ""
        else return


class Trie:
    # contains the root of the trie and also ensures all requests are lowercase
    def __init__(self, words):
        # takes a collection of words and creates a trie of them
        self.root = Node()
        for word in words:
            word.lower()
            curr = self.root
            for letter in word:
                curr.set_leaf(letter)
                curr = curr.get_leaf(letter)
            curr.complete = True

    def traverse(self, count):
        result = []
        # start at root
        curr = self.root
        # while len(result) < count
        # can implement lazy loading in future
        # go down trie until
        # use stack to save non none leaves to traverse down for more words


    def predict(self, char, count=3):
        # gives a list of non-None children to the next count letters
        # TODO: this is probably where all the suggestion and returning stuff should happen
        pass