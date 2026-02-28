"""
THE COMPLETE FUNCTIONS MASTERCLASS

"""

# 1. BASIC FUNCTION & DOCSTRINGS (Topic 39 & 46)
def greet_user(name, role="Guest"):
    """
    This is a Docstring. It documents what the function does.
    It reduces duplication by allowing us to reuse this greeting logic.
    """
    return f"Hello {name}, you are logged in as {role}."

# 2. HANDLING ARGUMENTS: *args and **kwargs (Topic 43)
def make_pizza(size, *toppings, **details):
    """
    *toppings (args): Collects extra positional arguments into a TUPLE.
    **details (kwargs): Collects extra keyword arguments into a DICTIONARY.
    """
    print(f"\nMaking a {size} pizza.")
    print(f"Toppings: {toppings}")
    print(f"Delivery Details: {details}")

# 3. SCOPE: Global vs Local vs Non-local (Topic 41 & 42)
global_score = 100 # GLOBAL Scope (top level)

def game_setup():
    local_high_score = 50 # ENCLOSING Scope (local to game_setup)
    
    def update_score():
        # Use 'nonlocal' to modify variable in the parent function
        nonlocal local_high_score
        local_high_score += 10
        
        # Use 'global' to modify variable at the very top level
        global global_score
        global_score += 1
        
    update_score()
    return local_high_score

# 4. MULTIPLE RETURNS (Topic 44)
def get_coordinates():
    # Returns a tuple, which can be unpacked
    return 10.5, 20.8, 30.0 

# 5. LAMBDAS & PURE VS IMPURE (Topic 45)
# Lambda: One-liner anonymous function
square = lambda x: x * x

# Pure Function: Same input = same output, no side effects
def pure_add(a, b):
    return a + b

# Impure Function: Interacts with external state (side effects)
external_list = []
def impure_append(item):
    external_list.append(item) # Modifies something OUTSIDE the function

# 6. TYPE HINTING / ANNOTATIONS
def calculate_discount(price: float, discount_rate: float = 0.1) -> float:
    """
    Type hints specify the expected data types for arguments and the return value.
    They don't enforce types at runtime, but help with IDE autocompletion and static analysis.
    """
    return price - (price * discount_rate)

# 7. HIGHER-ORDER FUNCTIONS
def apply_operation(x, y, operation):
    """
    A higher-order function takes another function as an argument or returns a function.
    """
    return operation(x, y)

# 8. RECURSION
def factorial(n):
    """
    Recursion is when a function calls itself to solve smaller instances of the same problem.
    Must have a base case to prevent infinite loops.
    """
    if n == 0 or n == 1: # Base case
        return 1
    return n * factorial(n - 1) # Recursive step

# 9. POSITIONAL-ONLY & KEYWORD-ONLY ARGUMENTS
def advanced_args(pos_only, /, standard, *, kw_only):
    """
    '/' enforces that arguments before it MUST be positional (cannot use pos_only=value).
    '*' enforces that arguments after it MUST be keyword arguments (must use kw_only=value).
    """
    print(f"Positional: {pos_only}, Standard: {standard}, Keyword: {kw_only}")

# --- EXECUTION EXAMPLES ---

# Calling with arguments
make_pizza("Large", "Pepperoni", "Mushrooms", address="123 Main St", tip=5)

# Unpacking multiple returns
x, y, z = get_coordinates()

# Scoping check
print(f"New High Score: {game_setup()}")
print(f"Updated Global: {global_score}")

# Built-in Functions (Topic 46)
numbers = [1, 5, 10]
print(f"Sum via built-in: {sum(numbers)}")

# Type Hinting
print(f"Discounted Price: {calculate_discount(100.0, 0.2)}")

# Higher-Order Functions (passing the pure_add function)
print(f"Higher-Order (Add): {apply_operation(5, 3, pure_add)}")

# Recursion
print(f"Factorial of 5: {factorial(5)}")

# Positional-only & Keyword-only arguments
advanced_args(10, 20, kw_only=30) # 10 must be positional, kw_only must be keyword