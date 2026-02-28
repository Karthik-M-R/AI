# ============================================================================
# base_device.py — The Foundation Class
# ============================================================================
#
# This file contains the BASE CLASS: Device.
# Every electronic device (Phone, Laptop, etc.) will inherit from this.
#
# CONCEPTS COVERED HERE:
#   Building a Class       — The 'Device' class itself
#   Namespace              — Class vs Object namespace
#   'self' argument        — How each instance knows about itself
#   Constructors (__init__) — The "birth" of each object
#   Static Method          — Utility function that doesn't need self/cls
#   Class Method           — Method that acts on the class, not the instance
#   Property Decorator     — Getter/Setter for controlled attribute access
# ============================================================================


class Device:
    """
    =========================================================================
    BUILDING A CLASS
    =========================================================================
    A class is a BLUEPRINT. It describes WHAT an object will be.
    Think of it as a cookie cutter — it defines the shape, but is not a cookie.

    'Device' is our blueprint for all electronic devices.
    Creating an object from it (e.g., d = Device("TV", "Sony")) makes a real
    device — that process is called "instantiation."
    =========================================================================
    """

    # -----------------------------------------------------------------------
    # NAMESPACE (Class-Level / Shared Variables)
    # -----------------------------------------------------------------------
    # Variables defined HERE (outside any method, directly inside the class)
    # live in the CLASS NAMESPACE.
    #
    # They are SHARED by ALL instances of this class.
    # Every Device object will see the same 'device_count'.
    #
    # Analogy: This is like a SCOREBOARD on the factory wall.
    #          Every device built adds 1 to this shared number.
    # -----------------------------------------------------------------------

    device_count = 0  # Class Namespace variable — shared by all Device objects

    # -----------------------------------------------------------------------
    # CONSTRUCTOR (__init__)
    # -----------------------------------------------------------------------
    # __init__ is a SPECIAL METHOD (called a "dunder" method).
    # It runs AUTOMATICALLY the moment you create an object:
    #     d = Device("TV", "Sony")   ← __init__ fires right here
    #
    # Its job is to set up the object's INITIAL STATE — like giving a newborn
    # baby its name, weight, and hospital band.
    #
    # Parameters:
    #   self  — the object being created (explained below)
    #   name  — what the device is called (e.g., "TV")
    #   brand — who made it (e.g., "Sony")
    # -----------------------------------------------------------------------

    def __init__(self, name: str, brand: str):
        """
        The Constructor — called automatically when a Device is created.
        Sets up instance-level (unique-per-object) attributes.
        """

        # -------------------------------------------------------------------
        # THE 'self' ARGUMENT
        # -------------------------------------------------------------------
        # 'self' is a REFERENCE to the CURRENT OBJECT being operated on.
        #
        # When you write:
        #     tv = Device("TV", "Sony")
        #     phone = Device("Phone", "Apple")
        #
        # Inside __init__:
        #   - For tv:    self → tv     (self.name = "TV")
        #   - For phone: self → phone  (self.name = "Phone")
        #
        # 'self' is how each object keeps its OWN data separate from others.
        #
        # Analogy: Imagine 10 students in a class. When the teacher says
        #          "Write YOUR name on YOUR paper," the word "YOUR" is 'self'.
        #          Each student writes THEIR OWN name.
        # -------------------------------------------------------------------

        # NAMESPACE (Object-Level / Instance Variables)
        # These live in the OBJECT NAMESPACE (unique to each instance).
        # 'tv.name' and 'phone.name' are DIFFERENT variables in memory.
        self.name = name        # Public attribute — anyone can access
        self.brand = brand      # Public attribute — anyone can access

        # The underscore prefix (_battery) is a CONVENTION (not enforced)
        # that says: "Hey developer, treat this as private. Don't touch
        # it directly. Use the property instead."
        self._battery = 100     # "Private" attribute — use property to access
        self._is_on = False     # "Private" attribute — device starts OFF

        # Updating the CLASS-level counter.
        # We use Device.device_count (not self.device_count) to make it
        # clear we're modifying the SHARED class variable, not creating
        # a new instance variable.
        Device.device_count += 1

    # -----------------------------------------------------------------------
    # INSTANCE METHODS (Regular Methods using 'self')
    # -----------------------------------------------------------------------
    # Instance methods are the most common type. They take 'self' as their
    # first parameter, which gives them access to the specific object's data.
    #
    # self.name, self._battery, etc. are all instance-specific.
    # -----------------------------------------------------------------------

    def turn_on(self):
        """Turn the device ON — modifies this specific object's state."""
        if not self._is_on:
            self._is_on = True
            print(f"✅ {self.name} is now ON.")
        else:
            print(f"⚡ {self.name} is already ON.")

    def turn_off(self):
        """Turn the device OFF — modifies this specific object's state."""
        if self._is_on:
            self._is_on = False
            print(f"🔴 {self.name} is now OFF.")
        else:
            print(f"💤 {self.name} is already OFF.")

    def status(self):
        """Print a status report for this specific device."""
        state = "ON" if self._is_on else "OFF"
        print(
            f"📱 Device: {self.name} | Brand: {self.brand} | "
            f"Battery: {self._battery}% | State: {state}"
        )

    def charge(self, amount: int):
        """
        Charge the device by a given amount.
        Demonstrates basic validation inside an instance method.
        """
        if amount < 0:
            print("❌ Cannot charge by a negative amount!")
            return
        # Cap the battery at 100%
        self._battery = min(100, self._battery + amount)
        print(f"🔋 {self.name} charged to {self._battery}%.")

    # -----------------------------------------------------------------------
    # STATIC METHOD (@staticmethod)
    # -----------------------------------------------------------------------
    # A Static Method is a function that LIVES INSIDE the class but does NOT
    # need access to the instance (self) or the class (cls).
    #
    # It's just a regular function that's logically grouped with the class.
    #
    # When to use:
    #   - Utility/helper functions that relate to the class's concept
    #     but don't need any object or class data.
    #
    # Analogy: A calculator on the factory wall. Any worker can use it,
    #          but it doesn't know which worker pressed the buttons.
    # -----------------------------------------------------------------------

    @staticmethod
    def is_valid_battery(value):
        """
        Checks if a battery value is valid (0–100).
        This doesn't need 'self' or 'cls' — it's a pure utility.
        """
        return isinstance(value, (int, float)) and 0 <= value <= 100

    # -----------------------------------------------------------------------
    # CLASS METHOD (@classmethod)
    # -----------------------------------------------------------------------
    # A Class Method receives the CLASS ITSELF as its first argument ('cls'),
    # not a specific instance.
    #
    # It can access and modify CLASS-LEVEL variables (like device_count)
    # but cannot access instance-level variables (like self.name).
    #
    # Common uses:
    #   1. Alternative constructors (factory methods)
    #   2. Accessing/modifying class-level state
    #
    # Analogy: The factory manager. They know how many devices the factory
    #          has made (cls.device_count), but they don't know the details
    #          of any specific device.
    # -----------------------------------------------------------------------

    @classmethod
    def get_device_count(cls):
        """
        Returns the total number of Device objects ever created.
        'cls' refers to the Device class itself.
        """
        return f"📊 Total devices created: {cls.device_count}"

    @classmethod
    def from_string(cls, device_string: str):
        """
        ALTERNATIVE CONSTRUCTOR — a factory method.
        Creates a Device from a string like "TV-Sony" instead of
        two separate arguments.

        This is a classic use case for @classmethod:
            Device.from_string("TV-Sony")  →  Device("TV", "Sony")

        We use 'cls' instead of 'Device' so that subclasses (SmartPhone,
        Laptop) will correctly create instances of THEIR OWN type.
        """
        name, brand = device_string.split("-")
        return cls(name.strip(), brand.strip())  # cls() = Device() or subclass()

    # -----------------------------------------------------------------------
    # PROPERTY DECORATOR (@property / @setter)
    # -----------------------------------------------------------------------
    # Properties let you access a method AS IF it were a simple attribute.
    #
    # Instead of:   device.get_battery()       ← ugly function call
    # You write:    device.battery_level        ← clean attribute access
    #
    # BUT behind the scenes, Python runs a method! This lets you add:
    #   - Validation (reject bad values)
    #   - Computation (calculate on the fly)
    #   - Logging (track who changed what)
    #
    # There are TWO parts:
    #   @property           → the GETTER (what happens when you READ)
    #   @name.setter        → the SETTER (what happens when you WRITE)
    #
    # Analogy: A bank teller. You say "I want to deposit $500."
    #          The teller CHECKS the money is real before putting it in.
    #          You don't walk into the vault yourself.
    # -----------------------------------------------------------------------

    @property
    def battery_level(self):
        """
        GETTER — Runs when you READ the battery_level.
        Usage:  print(device.battery_level)   ← looks like an attribute
        """
        return self._battery

    @battery_level.setter
    def battery_level(self, value):
        """
        SETTER — Runs when you WRITE to battery_level.
        Usage:  device.battery_level = 85     ← looks like simple assignment

        But behind the scenes, this method runs and validates the value!
        """
        if not Device.is_valid_battery(value):
            # Reject invalid values — the "bouncer" at the door
            print(f"❌ Invalid battery level: {value}. Must be 0–100.")
        else:
            self._battery = value
            print(f"🔋 {self.name} battery set to {self._battery}%.")

    @property
    def is_on(self):
        """Read-only property — no setter defined, so it can't be changed directly."""
        return self._is_on

    # -----------------------------------------------------------------------
    # MAGIC / DUNDER METHODS (Bonus)
    # -----------------------------------------------------------------------
    # __str__  → called when you do print(device) or str(device)
    # __repr__ → called in the debugger or when you type 'device' in REPL
    # These make your objects "speak" in human-readable ways.
    # -----------------------------------------------------------------------

    def __str__(self):
        """Human-readable string — for print() and str()."""
        return f"Device(name='{self.name}', brand='{self.brand}', battery={self._battery}%)"

    def __repr__(self):
        """Developer-readable string — for debugging."""
        return f"Device('{self.name}', '{self.brand}')"
