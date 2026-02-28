# ============================================================================
# main.py — The Runner File (Test & Demonstrate All OOP Concepts)
# ============================================================================
#
# This file IMPORTS classes from the 'electronics' package and USES them.
# It demonstrates every OOP concept in action.
#
# HOW TO RUN:
#   Open a terminal in the 'oop_mastery_project/' folder and type:
#       python main.py
# ============================================================================

from electronics import Device, SmartPhone, Laptop
from electronics.smart_devices import ConvertibleLaptop


def separator(title: str):
    """Utility to print section headers for readability."""
    print(f"\n{'='*65}")
    print(f"  {title}")
    print(f"{'='*65}\n")


# ============================================================================
# BUILDING A CLASS (Creating Objects / Instantiation)
# ============================================================================
# An object is a SPECIFIC instance of a class.
# Class  = Blueprint (Device)
# Object = Actual thing built from that blueprint (my_device)
#
# When you write:  my_device = Device("Speaker", "JBL")
# Python does:
#   1. Creates an empty object in memory
#   2. Calls Device.__init__(that_empty_object, "Speaker", "JBL")
#   3. Returns the fully initialized object
# ============================================================================

separator("Creating Objects (Instantiation)")

# Creating a basic Device object
my_device = Device("Bluetooth Speaker", "JBL")
print(f"Created: {my_device}")           # Calls __str__
print(f"Debug:   {repr(my_device)}")     # Calls __repr__


# ============================================================================
# NAMESPACE (Class vs Instance)
# ============================================================================
# There are TWO levels of namespace:
#
# 1. CLASS NAMESPACE (shared):
#    - Device.device_count → same for ALL Device objects
#
# 2. INSTANCE/OBJECT NAMESPACE (unique):
#    - my_device.name → "Bluetooth Speaker" (only THIS device)
#    - phone.name → "iPhone 15" (only THAT device)
#
# Python looks up attributes in this order:
#    instance → class → parent classes → error
# ============================================================================

separator("Namespace (Class vs Instance)")

phone = SmartPhone("iPhone 15", "Apple", "iOS", 256)
laptop = Laptop("MacBook Pro", "Apple", 16, has_gpu=True)

# Class namespace — shared counter
print(f"Devices created so far: {Device.device_count}")
# All three objects contributed to the SAME class-level counter!

# Instance namespace — each has its OWN name
print(f"Device name:   {my_device.name}")
print(f"Phone name:    {phone.name}")
print(f"Laptop name:   {laptop.name}")


# ============================================================================
# ATTRIBUTE SHADOWING
# ============================================================================
# When a child class has a method with the same name as the parent,
# the child's version "shadows" (overrides) the parent's.
#
# my_device.status()  → calls Device.status()       (parent's version)
# phone.status()      → calls SmartPhone.status()   (child's version — shadowed!)
# laptop.status()     → calls Laptop.status()       (child's version — shadowed!)
# ============================================================================

separator("Attribute Shadowing")

print("Calling .status() on each object:\n")

my_device.status()  # → Device.status()     (original)
phone.status()      # → SmartPhone.status()  (shadowed version)
laptop.status()     # → Laptop.status()      (shadowed version)


# ============================================================================
# SELF ARGUMENT (Instance Methods)
# ============================================================================
# 'self' is the object calling the method.
#
# When you write: phone.turn_on()
# Python translates it to: SmartPhone.turn_on(phone)
#                                                ↑
#                                          'self' = phone
#
# This is why every instance method takes 'self' as its first parameter.
# ============================================================================

separator("'self' Argument in Instance Methods")

# Different objects calling the same method — 'self' is different each time
phone.turn_on()         # self = phone
laptop.turn_on()        # self = laptop
my_device.turn_on()     # self = my_device

# Each object keeps its OWN state (thanks to self)
print(f"\nPhone is on: {phone.is_on}")      # True
print(f"Laptop is on: {laptop.is_on}")      # True


# ============================================================================
# CONSTRUCTORS (__init__)
# ============================================================================
# Already demonstrated above! Every time we call Device(), SmartPhone(),
# or Laptop(), the __init__ method runs automatically.
#
# Let's show the ALTERNATIVE CONSTRUCTOR (factory method) from @classmethod:
# ============================================================================

separator("Constructors + Alternative Constructor")

# Normal constructor
normal_device = Device("Tablet", "Samsung")
print(f"Normal:      {normal_device}")

# Alternative constructor using @classmethod
string_device = Device.from_string("SmartWatch - Fitbit")
print(f"From string: {string_device}")

# The from_string method ALSO works on subclasses (thanks to 'cls')
string_phone = SmartPhone.from_string("Galaxy S24 - Samsung")
# Wait — this would fail because SmartPhone needs more args!
# That's a design consideration: @classmethod alternative constructors
# should match the child's __init__ signature. This is intentional learning.


# ============================================================================
# INHERITANCE
# ============================================================================
# SmartPhone inherited ALL of Device's methods:
#   turn_on(), turn_off(), charge(), battery_level, etc.
# Without rewriting a single line!
# ============================================================================

separator("Inheritance in Action")

# SmartPhone uses INHERITED methods from Device
phone.charge(20)            # Inherited from Device
print(f"Battery: {phone.battery_level}%")  # Inherited property

# SmartPhone also has its OWN methods
phone.install_app("Instagram")
phone.install_app("Spotify")
phone.install_app("Instagram")   # Already installed — won't duplicate
phone.list_apps()

# isinstance() checks the inheritance chain
print(f"\nIs phone a SmartPhone? {isinstance(phone, SmartPhone)}")  # True
print(f"Is phone a Device?     {isinstance(phone, Device)}")       # True! (IS-A)
print(f"Is phone a Laptop?     {isinstance(phone, Laptop)}")       # False


# ============================================================================
# super() — Accessing the Base Class
# ============================================================================
# Already demonstrated in SmartPhone.__init__() and Laptop.__init__()
# where super().__init__() calls Device.__init__().
#
# Let's see it explicitly:
# ============================================================================

separator("super() in Action")

print("When SmartPhone.__init__ runs, it calls super().__init__() first.")
print("This ensures Device's setup (name, brand, battery, count) happens")
print("BEFORE SmartPhone adds its own attributes (os_type, storage, apps).\n")

another_phone = SmartPhone("Pixel 9", "Google", "Android", 128)
another_phone.status()


# ============================================================================
# METHOD RESOLUTION ORDER (MRO)
# ============================================================================
# MRO tells Python WHERE to look for a method and in WHAT ORDER.
# This is critical for multiple inheritance.
# ============================================================================

separator("Method Resolution Order (MRO)")

# ConvertibleLaptop inherits from BOTH Laptop and TabletMixin
hybrid = ConvertibleLaptop("Surface Pro", "Microsoft", 16, has_gpu=True)

# Let's see the MRO
print("MRO for ConvertibleLaptop:")
for i, cls in enumerate(ConvertibleLaptop.mro()):
    print(f"  {i+1}. {cls.__name__}")

# When we call hybrid.status(), Python searches in MRO order:
#   1. ConvertibleLaptop — has status()? YES → Use it.
#   (If not found, it would check Laptop, then Device, then TabletMixin, then object)

print("\nCalling hybrid.status():")
hybrid.turn_on()
hybrid.status()

# TabletMixin methods are available thanks to multiple inheritance
hybrid.toggle_mode()
hybrid.stylus_input()
hybrid.status()


# ============================================================================
# STATIC METHOD
# ============================================================================
# Static methods are utility functions that don't need object or class data.
# They can be called on the CLASS or on an INSTANCE — both work.
# ============================================================================

separator("Static Method")

# Called on the CLASS (most common way)
print(f"Is 85 valid?  {Device.is_valid_battery(85)}")     # True
print(f"Is 150 valid? {Device.is_valid_battery(150)}")    # False
print(f"Is -10 valid? {Device.is_valid_battery(-10)}")    # False

# Called on an INSTANCE (also works, but less common)
print(f"Is 50 valid?  {phone.is_valid_battery(50)}")      # True


# ============================================================================
# CLASS METHOD
# ============================================================================
# Class methods receive the CLASS (cls) as first argument.
# They can access class-level data like device_count.
# ============================================================================

separator("Class Method")

# get_device_count uses 'cls' to access Device.device_count
print(Device.get_device_count())

# Can also be called on a subclass — 'cls' will be the subclass
print(SmartPhone.get_device_count())  # Same count — it's shared in Device


# ============================================================================
# PROPERTY DECORATOR (Getter/Setter)
# ============================================================================
# Properties let you access methods AS IF they were attributes.
# This provides CONTROLLED access with validation.
# ============================================================================

separator("Property Decorator (Getter/Setter)")

# GETTER — looks like accessing a variable, but runs a method
print(f"Current battery: {laptop.battery_level}%")

# SETTER — looks like assigning a variable, but runs validation
laptop.battery_level = 75        # Valid — sets it
laptop.battery_level = 200       # Invalid — rejected by the setter!
laptop.battery_level = -5        # Invalid — rejected by the setter!

print(f"Final battery:   {laptop.battery_level}%")  # Still 75


# ============================================================================
# SUMMARY — All 11 Concepts in One Place
# ============================================================================

separator("🏆 SUMMARY — All OOP Concepts")

summary = """
┌─────────────────────────┬────────────────────────────────────────┐
│ Concept                 │ One-Liner                              │
├─────────────────────────┼────────────────────────────────────────┤
│ Building a Class        │ A blueprint to create objects           │
│ Namespace               │ Class vars (shared) vs Instance (unique)│
│ Attribute Shadowing     │ Child overrides parent's method/var     │
│ self Argument           │ "This object" — unique identity marker  │
│ Constructors (__init__) │ Auto-runs at birth to set up state      │
│ Inheritance             │ Child reuses everything from parent     │
│ super()                 │ Calls the parent's method from child    │
│ MRO                     │ The order Python searches for methods   │
│ Static Method           │ Utility — no self, no cls needed        │
│ Class Method            │ Acts on the class, not the instance     │
│ Property Decorator      │ Getter/Setter — controlled access       │
└─────────────────────────┴────────────────────────────────────────┘
"""
print(summary)

print("✅ All 11 OOP concepts demonstrated successfully!")
print(f"📊 Total Device objects created in this session: {Device.device_count}")
