"""
THE COMPREHENSION & GENERATOR MASTERCLASS
File: comprehensions_pro.py
Covers: List, Set, Dict Comprehensions + Generator Expressions & yield.
"""

import sys  # Provides interpreter internals like getsizeof for memory insights.

# 1. LIST COMPREHENSION (The most common)
# Syntax: [expression for item in iterable if condition]
numbers = [1, 2, 3, 4, 5, 6]

# Goal: Create squares of even numbers only
squares_of_evens = [n**2 for n in numbers if n % 2 == 0]
print(f"List Comp (Squares of Evens): {squares_of_evens}")
# Sample Output: [4, 16, 36] -> squares of only the even inputs 2, 4, 6.


# 2. SET COMPREHENSION (Unique items, no order)
# Syntax: {expression for item in iterable}
duplicate_data = ["apple", "banana", "apple", "CHERRY", "banana"]

# Goal: Unique lowercase names
unique_fruits = {f.lower() for f in duplicate_data}
print(f"Set Comp (Unique lowercase): {unique_fruits}")
# Sample Output: {'cherry', 'banana', 'apple'} -> lowercase unique names (order may vary).
# 


# 3. DICTIONARY COMPREHENSION (Key-Value mapping)
# Syntax: {key: value for item in iterable}
users = [("id_1", "Alice"), ("id_2", "Bob")]

# Goal: Map IDs to Names
user_map = {uid: name for uid, name in users}
print(f"Dict Comp: {user_map}")
# Sample Output: {'id_1': 'Alice', 'id_2': 'Bob'} -> ID to name lookup table.


# 4. GENERATOR EXPRESSION (Memory Optimization)
# Syntax: (expression for item in iterable)
# Unlike lists, this does NOT store the data. It calculates on the fly.
big_range = range(1000000)

list_ver = [x * 2 for x in big_range[:1000]] # Stores all in RAM
gen_ver = (x * 2 for x in big_range)         # Stores only the formula

print(f"List Memory: {sys.getsizeof(list_ver)} bytes")
print(f"Generator Memory: {sys.getsizeof(gen_ver)} bytes")
# Sample Output: List Memory ~9016 bytes vs Generator ~112 bytes (values differ by platform).
# 


# 5. THE YIELD KEYWORD (The "Lazy" Function)
# Used to create complex generators that a single line cannot handle.
def countdown(n):
    """A generator function that counts down."""
    while n > 0:
        yield n # Execution 'pauses' here and returns n
        n -= 1

print("Starting Generator Countdown:")
for count in countdown(3):
    print(count)
# 


# 6. COMPREHENSION WITH IF-ELSE (Transformation)
# Note: If-Else goes BEFORE the 'for' loop for transformation
prices = [10, 50, 100, 20]
# Tag items as Expensive or Cheap
price_tags = ["Expensive" if p >= 50 else "Cheap" for p in prices]
print(f"Price Tags: {price_tags}")
# Sample Output: ['Cheap', 'Expensive', 'Expensive', 'Cheap'] -> one tag per price.


# 7. NESTED COMPREHENSION (Flattening)
matrix = [[1, 2], [3, 4], [5, 6]]
# Goal: Turn into [1, 2, 3, 4, 5, 6]
flat = [num for row in matrix for num in row]
print(f"Flattened Matrix: {flat}")
# Sample Output: [1, 2, 3, 4, 5, 6] -> flattens nested rows into a single list.