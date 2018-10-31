# Ahmad M. Osman - Dr. Kent Lee, CS360

# Dr. Lee, please notice that if multiple words were seperated by nothing but punctuation, like "Happiness.--That", my string manipulation to remove punctuation will transfer it into "happinessthat". I did not want to put more time into cleaning the words as leaving "happinessthat" like it that is helping to test the Bloom Filter.


import math
import string


class Trie:
    def __insert(node, item):
        if len(item) == 0:
            raise ValueError("Inserting empty item into Trie!")

        if node == None:
            node = Trie.TrieNode(item[0])
            item = item[1:]

        original_node = node

        for letter in item:
            if node.item == letter:
                print(letter)
                node = node.follows
                continue
            elif node.item == None:
                node.item = letter
                node.follows = Trie.TrieNode(letter)
                node = node.follows
            elif node.item != letter:
                node.next = Trie.TrieNode(letter)
                node = node.next

    def __contains(node, item):
        """# This is the recursive membership test.
        pass """
        pass

    class TrieNode:
        def __init__(self, item, next=None, follows=None):
            self.item = item
            self.next = next
            self.follows = follows

    def __init__(self):
        self.start = None

    def insert(self, item):
        self.start = Trie.__insert(self.start, item)

    def __contains__(self, item):
        return Trie.__contains(self.start, item)


def main():
    words = []
    with open("wordsEn.txt") as openfile:
        words = openfile.readlines()

    trie = Trie()
    for word in words:
        word = word.strip()
        word += '$'
        trie.insert(word)


"""     # count = 0
    with open("declaration.txt") as openfile:
        exclude = set(string.punctuation)
        for line in openfile:
            for word in line.split():
                # removing any punctuation
                word = ''.join(ch for ch in word if ch not in exclude)
                # lowering
                word = word.lower()
                if word not in bloom:
                    # count += 1
                    print(word)
    # print(count) """


if __name__ == "__main__":
    main()
