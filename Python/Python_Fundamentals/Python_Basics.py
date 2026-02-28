"""
THE COMPLETE PYTHON BASICS CRASH COURSE
Covers: Variables, Data Types, Control Flow, Functions, OOP,
Tuples, Lists, Sets, Dicts, Bytearrays, NamedTuples, 
Match-Case, Operators, Collections, File I/O, and Loop Control.
"""

from collections import namedtuple, Counter, deque
import math

# --- 0. VARIABLES & BASIC DATA TYPES ---

# Python is dynamically typed
age = 25                # int
height = 5.9            # float
name = "John Doe"       # str
is_student = True       # bool
empty_value = None      # NoneType

# --- 0.5. BASIC OPERATORS & CONTROL FLOW ---

# Arithmetic: +, -, *, /, // (floor division), % (modulo), ** (power)
math_result = (10 + 5) * 2 // 3 

# Logical: and, or, not
if age >= 18 and is_student:
    print("Adult student")
elif age < 18 or not is_student:
    print("Minor or not a student")
else:
    print("Adult non-student")

# While Loop
count = 0
while count < 3:
    print(f"Count is {count}")
    count += 1


# --- 1. DATA STRUCTURES (Lists, Tuples, Sets, Dicts) ---

# List: Mutable, ordered, allows duplicates
fruits = ["apple", "banana"]
fruits.append("cherry")   # Adding
fruits[0] = "apricot"     # Changing
# 

# Tuple: Immutable, ordered
coordinates = (10, 20)
# coordinates[0] = 15     # This would fail (immutable)

# Set: Unique items, unordered
unique_ids = {101, 102, 103, 101} # The second 101 is ignored
# 

# Dictionary: Key-Value pairs
user = {"name": "Alice", "role": "admin"}
user_name = user.get("name", "Guest") # Safe access with default


# --- 2. ADVANCED TYPES & COLLECTIONS ---

# Bytearray: Mutable sequence of bytes (integers 0-255)
data = bytearray("hello", "utf-8")
data[0] = 72 # Change 'h' to 'H'

# NamedTuple: Tuples with field names
# A namedtuple is a factory function for creating tuple subclasses with named fields.
# It provides the memory efficiency of a regular tuple but allows you to access 
# elements by name (like an object attribute) instead of just by index.
# This makes code much more readable and self-documenting.
Point = namedtuple('Point', ['x', 'y'])
pt = Point(10, 20) 
# Access via name (preferred): pt.x -> 10, pt.y -> 20
# Access via index (still works): pt[0] -> 10, pt[1] -> 20
# Like regular tuples, namedtuples are IMMUTABLE (you cannot do pt.x = 15)

# Counter: Tallying items
tally = Counter("mississippi") # {'i': 4, 's': 4, 'p': 2, 'm': 1}


# --- 3. OPERATORS & THE WALRUS ---

# Walrus Operator (:=): Assign and evaluate in one line
if (n := len(fruits)) > 2:
    print(f"List is long! Length is {n}")

# Member Testing (in / not in)
is_apple = "apple" in fruits # Returns True/False


# --- 4. LOOP CONTROL & ENUMERATE/ZIP ---

# Enumerate: Get index and value
for i, val in enumerate(fruits, start=1):
    print(f"Item {i}: {val}")

# Zip: Pair two lists together
scores = [10, 20, 30]
for fruit, score in zip(fruits, scores):
    print(f"{fruit} scored {score}")
# 


# --- 5. CONDITIONAL LOGIC (Match-Case & Fallbacks) ---

# Match-Case (Python 3.10+): Structural Pattern Matching
status = 404
match status:
    case 200:
        print("Success")
    case 404 | 405:
        print("Not Found/Allowed")
    case _:
        print("Default Case")

# Break, Continue, and Else Fallback
for x in range(5):
    if x == 2:
        continue # Skip 2
    if x == 4:
        break    # Stop at 4
else:
    # Only runs if NO break occurred
    print("Loop finished naturally")


# --- 6. OPERATOR OVERLOADING (Dunder Methods) ---

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # Overloading the + operator
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2) # Uses __add__ to result in Vector(4, 6)


# --- 7. ERROR HANDLING  ---

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
finally:
    print("Cleanup code goes here.")


# --- 8. FUNCTIONS & LAMBDAS ---

# Basic function with default arguments and type hinting
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# *args (variable positional arguments) and **kwargs (variable keyword arguments)
def flexible_function(*args, **kwargs):
    print("Positional:", args)   # Tuple of arguments
    print("Keyword:", kwargs)    # Dictionary of keyword arguments

# Lambda functions (anonymous, inline functions)
square = lambda x: x ** 2
print(square(5)) # 25


# --- 9. COMPREHENSIONS ---

# List comprehension: concise way to create lists
squares = [x**2 for x in range(5)] # [0, 1, 4, 9, 16]

# Dictionary comprehension
sq_dict = {x: x**2 for x in range(3)} # {0: 0, 1: 1, 2: 4}


# --- 10. FILE I/O ---

# Using 'with' context manager ensures the file is properly closed
with open("sample.txt", "w") as file:
    file.write("Hello, World!\n")

with open("sample.txt", "r") as file:
    content = file.read()
    print(content)


# --- 11. OOP BASICS (Classes & Inheritance) ---

class Animal:
    def __init__(self, species):
        self.species = species
        
    def make_sound(self):
        pass # Abstract method concept

class Dog(Animal): # Inheritance
    def __init__(self, name):
        super().__init__("Canine") # Call parent constructor
        self.name = name
        
    def make_sound(self):
        return "Woof!"

my_dog = Dog("Buddy")
print(f"{my_dog.name} is a {my_dog.species} and says {my_dog.make_sound()}")