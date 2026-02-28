"""
THE COMPLETE DECORATORS GUIDE

Covers: Basic wrappers, @ syntax, *args/**kwargs in decorators, and real-world examples.
"""

from functools import wraps

# 1. THE BASIC CONCEPT 
# A decorator is just a function that takes another function as input.
# Think of it like saying "wrap this function with extra steps before and after it runs."
def simple_decorator(original_func):
    @wraps(original_func)
    def wrapper():
        print("--- Logic before the function ---")
        original_func()
        print("--- Logic after the function ---")
    return wrapper

@simple_decorator
def say_hello():
    print("Hello World!")

# Running say_hello() now includes the extra print statements
say_hello()
# Sample output:
# --- Logic before the function ---
# Hello World!
# --- Logic after the function ---
#


# 2. DECORATORS WITH ARGUMENTS (The *args and **kwargs trick)
# If the original function takes arguments (like a, b), the wrapper must accept them too.
# This pattern lets a single decorator work for any function signature.
def reporter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # *args packs positional values, **kwargs packs keyword pairs so the decorator can forward any signature
        print(f"Executing: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished: {func.__name__}")
        return result
    return wrapper

@reporter
def add(a, b):
    return a + b

print(f"Result: {add(10, 20)}")
# Sample output:
# Executing: add
# Finished: add
# Result: 30


# 3. BUILD A LOGGER DECORATOR 
# Used to track what is happening in an application.
# Great when you want to print or store "who called what and when" without touching every function.
def logger(func):
    import datetime
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Calling {func.__name__} with {args}")
        return func(*args, **kwargs)
    return wrapper

@logger
def save_user_profile(username):
    print(f"Saving profile for {username}...")

save_user_profile("coder_pro_99")
# Sample output:
# [2026-02-25 10:00:00] Calling save_user_profile with ('coder_pro_99',)
# Saving profile for coder_pro_99...


# 4. BUILD AN AUTHORIZATION DECORATOR 
# Used to protect sensitive functions.
# Pretend this is the currently logged-in user pulled from your auth system.
current_user = {"name": "Bob", "is_admin": False}

def admin_only(func):
    # This decorator simply blocks the function unless current_user says "is_admin: True".
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.get("is_admin"):
            print(f"SECURITY ALERT: User {current_user['name']} tried to access {func.__name__}!")
            return "Access Denied"
        return func(*args, **kwargs)
    return wrapper

@admin_only
def delete_database():
    print("Database deleted successfully.")

# This will fail because Bob is not an admin
print(delete_database())
# Sample output:
# SECURITY ALERT: User Bob tried to access delete_database!
# Access Denied
#


# 5. MULTIPLE DECORATORS (Stacking)
# You can stack decorators. They run from top to bottom.
# Picture it like passing text through italic formatting first, then bold formatting.
def bold(func):
    @wraps(func)
    def wrapper():
        return f"<b>{func()}</b>"
    return wrapper

def italic(func):
    @wraps(func)
    def wrapper():
        return f"<i>{func()}</i>"
    return wrapper

@bold
@italic
def get_text():
    return "Python is awesome"

print(get_text()) # Result: <b><i>Python is awesome</i></b>
# Sample output:
# <b><i>Python is awesome</i></b>


# 6. WHY USE @wraps? (Pro Tip)
# When you decorate a function, it "loses" its original identity (its name becomes 'wrapper').
# We use functools.wraps to fix this.
# wraps copies over the original function's name, docstring, and other metadata so debugging stays easy.

def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@debug
def my_secret_function():
    """This is a secret."""
    pass

print(my_secret_function.__name__) # 'my_secret_function' (instead of 'wrapper')
# Sample output:
# my_secret_function


#"If you don't use @wraps, every decorated function in your entire project effectively becomes named 'wrapper'.
#  When a bug happens, your computer tells you 'The wrapper is broken,' which is like a mechanic telling you 
# 'The metal part of the car is broken.' It's true, but it's useless for fixing the problem."