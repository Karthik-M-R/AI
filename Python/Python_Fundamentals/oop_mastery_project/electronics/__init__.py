# ============================================================================
# __init__.py — Package Initializer
# ============================================================================
#
# WHAT IS THIS FILE?
# ------------------
# When Python sees a folder with an __init__.py file inside it, it treats
# that folder as a "package" — a collection of related modules (.py files).
#
# Without this file, Python would NOT recognize 'electronics/' as a package,
# and you could NOT do:   from electronics import base_device
#
# WHAT DOES THIS FILE DO?
# -----------------------
# 1. It runs automatically when someone imports anything from this package.
# 2. We use it to make imports cleaner for anyone using our package.
#
# Instead of writing:
#     from electronics.base_device import Device
#     from electronics.smart_devices import SmartPhone, Laptop
#
# The user can simply write:
#     from electronics import Device, SmartPhone, Laptop
#
# This is because we "re-export" them here.
# ============================================================================

from electronics.base_device import Device          # Import Device from base_device module
from electronics.smart_devices import SmartPhone, Laptop  # Import SmartPhone & Laptop

# __all__ defines what gets exported when someone does: from electronics import *
# It's a whitelist — only these names are publicly available.
__all__ = ["Device", "SmartPhone", "Laptop"]
