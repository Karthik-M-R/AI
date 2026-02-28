"""
This is the __init__.py file.
It makes Python treat the 'Functions_python' directory as a package.
You can use it to initialize the package or expose specific functions.
"""

# You can optionally import things here to make them easier to access
# from .Function_py import make_pizza, calculate_discount
# This file runs as soon as you 'import Functions_python'
print("Initializing Functions_python...")

# You can use this to provide version info or shortcuts
__version__ = "1.0.0"

# Hoisting: Importing a function here makes it available as Functions_python.greet_user()
from .Function_py import greet_user