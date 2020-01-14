"""
Imports
"""


class HashTable:
    current_size = 0

    def __init__(self, size=13):
        self.size = size
        self.array = [None] * size
        self.prime = 7

    def first_hash(self, key) -> int:
        """
        computes an index that suggests where the entry can be found
        """
        return int(key) % self.size

    def second_hash(self, key) -> int:
        """
        function to calculate second hash
        """
        return (self.prime - (int(key) % self.prime))

    def is_full(self):
        """
        function to check if hash table is full 
        """
        # if hash size reaches maximum size
        return self.current_size == self.size

    def double_hash(self):
        hasht2 = HashTable(size=len(self.array) * 2)

        for item in self.array:
            if item is None:
                continue
            else:
                hasht2.insert_hash(item[0], item[1])
        self.array = hasht2.array

    def insert_hash(self, key, value):
        """
        function to insert key into hash table 
        """
        index = self.first_hash(key)

        if self.is_full():
            self.double_hash()
        if self.array[index] is not None:
            # array at this position contains a value
            for item in self.array:
                if item is not None:
                    if item[0] == key:
                        item = (key, value)
                        break
            else:
                self.array.append((key, value))
        else:
            # if no collision occurs
            self.array[index] = (key, value)

    def get(self, key):
        """
        Get a value by key
        """
        index = self.first_hash(key)
        if self.array[index] is not None:
            for item in self.array:
                if item[0] == key:
                    return item[1]
        else:
            raise KeyError()
