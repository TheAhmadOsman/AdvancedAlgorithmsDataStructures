# Ahmad M. Osman - Dr. Kent Lee, CS360

# Dr. Lee, please notice that if multiple words were seperated by nothing but punctuation, like "Happiness.--That", my string manipulation to remove punctuation will transfer it into "happinessthat". I did not want to put more time into cleaning the words as leaving "happinessthat" like it is is helps in testing the Bloom Filter.


import math
import string


class BloomFilter:
    def __init__(self, num_items, false_positive_percent):
        self.num_bits = (num_items * math.log(false_positive_percent)) / (math.log(2) ** 2) 
        self.num_bits = int(abs(self.num_bits))
        # print("Items:", num_items)
        # print("Bits:", self.num_bits)
        
        self.num_hashes = (self.num_bits / num_items) * math.log(2) 
        self.num_hashes = abs(self.num_hashes)
        self.num_hashes = int(math.ceil(self.num_hashes))
        # print("Hashes:", self.num_hashes)
        
        # a bytearray is initialized with 0s 
        self.data = bytearray((self.num_bits + 7) // 8)
        # print("ByteArray Size:", self.data.__sizeof__())

        self.masks = {}
        for i in range(8):
            self.masks[i] = 1 << i
    
    def add(self, word):
        for i in range(self.num_hashes):
            hash_item = word + str(i)
            hash_val = hash(hash_item)
            bit_idx = hash_val % self.num_bits
            byte_idx = bit_idx >> 3
            exponent = bit_idx & 7
            mask = self.masks[exponent]
            #print(byte_idx)
            self.data[byte_idx] |= mask
    
    def __contains__(self, word):
        for i in range(self.num_hashes):
            hash_item = word + str(i)
            hash_val = hash(hash_item)
            bit_idx = hash_val % self.num_bits
            byte_idx = bit_idx >> 3
            exponent = bit_idx & 7
            mask = self.masks[exponent]
            checkbit = self.data[byte_idx] & mask
            if checkbit == 0:
                # print("\tWord:", word)
                # print("\t\tBYTE:", self.data[byte_idx])
                # print("\t\tMASK:", mask)
                # print("\t\tCHECKBIT:", checkbit)
                return False
        return True


def main():
    words = []
    with open("wordsEn.txt") as openfile:
        words = openfile.readlines()
    
    bloom = BloomFilter(len(words), 0.005)
    for word in words:
        word = word.strip()
        bloom.add(word)

    # count = 0
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
    # print(count)

if __name__ == "__main__":
    main()
