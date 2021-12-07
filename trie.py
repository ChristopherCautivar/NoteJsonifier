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


class Trie:
    # contains the root of the trie and also ensures all requests are lowercase
    def __init__(self, words):
        # takes a collection of words and creates a trie of them
        self.root = Node()
        for word in words:
            word.lower()
            curr = self.root
            for letter in word:
                if not curr.get_leaf(letter):
                    curr.set_leaf(letter)
                curr = curr.get_leaf(letter)
            curr.complete = True

    def find_word(self, node, word="", result=[]):
        if node.complete:
            result.append(word)
        for i in range(len(node.leaves)):
            if node.leaves[i]:
                result = self.find_word(node.leaves[i], word + chr(i+ord("a")), result)
        return result

    def predict(self, char, count=3):
        # gives a list of non-None children to the next count letters
        # TODO: this is probably where all the suggestion and returning stuff should happen
        pass