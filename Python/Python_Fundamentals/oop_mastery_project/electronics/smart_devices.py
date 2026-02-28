# ============================================================================
# smart_devices.py — Child Classes
# ============================================================================
#
# This file contains classes that INHERIT from Device (in base_device.py).
# It demonstrates the "IS-A" relationship and how children extend parents.
#
# CONCEPTS COVERED HERE:
#   Attribute Shadowing  — Child overrides parent's method/variable
#   Inheritance          — SmartPhone IS-A Device, Laptop IS-A Device
#   super()              — Calling the parent's methods from the child
#   MRO (Method Resolution Order) — How Python searches for methods
# ============================================================================

from electronics.base_device import Device


# ===========================================================================
# INHERITANCE
# ===========================================================================
# Inheritance lets a NEW class (child/subclass) REUSE everything from an
# EXISTING class (parent/superclass), then ADD or CHANGE things.
#
# Syntax:   class Child(Parent):
#               ...
#
# WHY use inheritance?
#   - Avoid copy-pasting code (DRY — Don't Repeat Yourself)
#   - Create a hierarchy: Device → SmartPhone → GamingPhone
#   - If you fix a bug in Device, ALL children get the fix for free!
#
# Analogy: A SmartPhone IS-A Device (just like a Car IS-A Vehicle).
#          The SmartPhone gets everything a Device has (battery, brand, etc.)
#          PLUS it adds its own features (apps, camera, etc.)
# ===========================================================================


class SmartPhone(Device):
    """
    SmartPhone inherits from Device.
    It has everything a Device has, plus phone-specific features.

    Inheritance chain: SmartPhone → Device → object
    """

    # -----------------------------------------------------------------------
    # super() — ACCESSING THE PARENT CLASS
    # -----------------------------------------------------------------------
    # super() returns a temporary object of the PARENT class, allowing
    # you to call the parent's methods.
    #
    # WHY use super()?
    #   - To REUSE the parent's __init__ instead of rewriting it.
    #   - To EXTEND (not replace) the parent's behavior.
    #   - It correctly handles multiple inheritance (MRO).
    #
    # Without super():
    #   You'd have to manually copy all of Device.__init__'s code here.
    #   If Device changes, you'd have to update SmartPhone too. Nightmare!
    #
    # Analogy: When you're born, your parents give you a name and a home
    #          (that's super().__init__). Then YOU add your own preferences
    #          (favorite color, hobbies) — that's the extra code below.
    # -----------------------------------------------------------------------

    def __init__(self, name: str, brand: str, os_type: str, storage_gb: int):
        """
        SmartPhone constructor.

        Parameters:
            name       — device name (passed UP to Device.__init__)
            brand      — device brand (passed UP to Device.__init__)
            os_type    — "Android" or "iOS" (SmartPhone-specific)
            storage_gb — storage in GB (SmartPhone-specific)
        """
        # STEP 1: Let the PARENT (Device) do its setup first.
        # This sets self.name, self.brand, self._battery, self._is_on,
        # and increments Device.device_count.
        super().__init__(name, brand)

        # STEP 2: Add SmartPhone-specific attributes.
        # These exist ONLY on SmartPhone objects, not on plain Device objects.
        self.os_type = os_type          # "Android" or "iOS"
        self.storage_gb = storage_gb    # Storage capacity
        self._installed_apps = []       # List of installed apps (private)

    # -----------------------------------------------------------------------
    # ATTRIBUTE SHADOWING (Method Override)
    # -----------------------------------------------------------------------
    # When a child class defines a method with the SAME NAME as the parent,
    # the child's version "shadows" (overrides) the parent's version.
    #
    # When you call phone.status(), Python finds status() in SmartPhone
    # FIRST (because of MRO), so it uses the child's version.
    #
    # The parent's status() still EXISTS — it's just hidden behind the
    # child's version. You can still call it via super().status().
    #
    # Analogy: Your parent taught you to cook pasta one way.
    #          You learned a new recipe. When someone says "make pasta",
    #          you use YOUR recipe (shadowing), but you could still use
    #          your parent's if you wanted (super().status()).
    # -----------------------------------------------------------------------

    def status(self):
        """
        SHADOWS Device.status() — this version runs instead of the parent's.
        Adds phone-specific info (OS, storage, apps) to the report.
        """
        # We could call super().status() here to include the parent's output,
        # but we're completely replacing it to show shadowing clearly.
        state = "ON" if self.is_on else "OFF"
        print(
            f"📱 SmartPhone: {self.name} | Brand: {self.brand} | "
            f"OS: {self.os_type} | Storage: {self.storage_gb}GB | "
            f"Battery: {self.battery_level}% | State: {state} | "
            f"Apps: {len(self._installed_apps)}"
        )

    def install_app(self, app_name: str):
        """Install an app — SmartPhone-specific method."""
        if app_name in self._installed_apps:
            print(f"⚠️  '{app_name}' is already installed on {self.name}.")
        else:
            self._installed_apps.append(app_name)
            print(f"✅ '{app_name}' installed on {self.name}.")

    def list_apps(self):
        """List all installed apps."""
        if not self._installed_apps:
            print(f"📭 No apps installed on {self.name}.")
        else:
            print(f"📦 Apps on {self.name}: {', '.join(self._installed_apps)}")


class Laptop(Device):
    """
    Laptop inherits from Device.
    Demonstrates inheritance with a different set of child-specific features.

    Inheritance chain: Laptop → Device → object
    """

    def __init__(self, name: str, brand: str, ram_gb: int, has_gpu: bool = False):
        """
        Laptop constructor.

        Parameters:
            name    — device name (passed UP to Device)
            brand   — device brand (passed UP to Device)
            ram_gb  — RAM in gigabytes (Laptop-specific)
            has_gpu — whether it has a dedicated GPU (Laptop-specific)
        """
        # Let the parent Device set up the basics
        super().__init__(name, brand)

        # Laptop-specific attributes
        self.ram_gb = ram_gb
        self.has_gpu = has_gpu
        self._running_processes = []  # Private: list of running programs

    # SHADOWING: Laptop has its own version of status()
    def status(self):
        """Shadows Device.status() with laptop-specific information."""
        state = "ON" if self.is_on else "OFF"
        gpu_status = "🎮 GPU: Yes" if self.has_gpu else "💻 GPU: No"
        print(
            f"💻 Laptop: {self.name} | Brand: {self.brand} | "
            f"RAM: {self.ram_gb}GB | {gpu_status} | "
            f"Battery: {self.battery_level}% | State: {state} | "
            f"Processes: {len(self._running_processes)}"
        )

    def run_program(self, program_name: str):
        """Start a program — Laptop-specific method."""
        if not self.is_on:
            print(f"❌ Cannot run '{program_name}' — {self.name} is OFF!")
            return
        self._running_processes.append(program_name)
        print(f"▶️  '{program_name}' is now running on {self.name}.")

    def list_processes(self):
        """List all running processes."""
        if not self._running_processes:
            print(f"📭 No processes running on {self.name}.")
        else:
            print(f"⚙️  Running on {self.name}: {', '.join(self._running_processes)}")


# ===========================================================================
# METHOD RESOLUTION ORDER (MRO)
# ===========================================================================
# MRO defines the ORDER in which Python searches for a method when you
# call it on an object.
#
# WHY does this matter?
#   With single inheritance (A → B), it's obvious: check A first, then B.
#   With MULTIPLE inheritance (A inherits from B AND C), it gets tricky:
#     - What if B and C both have a method called 'status()'? Which one wins?
#     - Python uses the C3 Linearization algorithm to decide.
#
# THE RULE (simplified):
#   Python searches LEFT to RIGHT in the inheritance list, going DEPTH-FIRST,
#   but never visiting the same class twice.
#
# Analogy: Imagine you lost your keys. You check:
#   1. Your pockets (the object itself)
#   2. Your desk (first parent)
#   3. The kitchen counter (second parent)
#   4. The junk drawer (grandparent)
#   You stop as soon as you find them!
# ===========================================================================


class TabletMixin:
    """
    A MIXIN class — provides extra functionality that can be "mixed in"
    to other classes via multiple inheritance.

    Mixins are not meant to be used alone. They add specific features
    to classes that inherit from them.
    """
    def stylus_input(self):
        """Simulate stylus/touch input — unique to tablets."""
        print(f"✏️  {self.name} received stylus input!")

    def tablet_mode(self):
        """Switch to tablet mode."""
        print(f"📐 {self.name} switched to tablet mode.")


class ConvertibleLaptop(Laptop, TabletMixin):
    """
    A 2-in-1 laptop that is both a Laptop AND has Tablet features.

    MULTIPLE INHERITANCE: ConvertibleLaptop inherits from BOTH Laptop AND TabletMixin.

    MRO for ConvertibleLaptop:
        ConvertibleLaptop → Laptop → Device → TabletMixin → object

    You can check this at runtime with:
        ConvertibleLaptop.mro()
    or:
        ConvertibleLaptop.__mro__

    HOW PYTHON DECIDED THIS ORDER:
    1. Start with ConvertibleLaptop itself
    2. Go to Laptop (first parent, listed LEFT)
    3. Go to Device (Laptop's parent)
    4. Go to TabletMixin (second parent, listed RIGHT)
    5. End at 'object' (the ultimate base class of everything in Python)
    """

    def __init__(self, name: str, brand: str, ram_gb: int, has_gpu: bool = False):
        # super() follows the MRO chain automatically!
        # It calls Laptop.__init__, which in turn calls Device.__init__.
        super().__init__(name, brand, ram_gb, has_gpu)
        self._is_tablet_mode = False

    def status(self):
        """Extended status showing tablet mode."""
        mode = "Tablet Mode 📐" if self._is_tablet_mode else "Laptop Mode 💻"
        state = "ON" if self.is_on else "OFF"
        gpu_status = "🎮 GPU: Yes" if self.has_gpu else "💻 GPU: No"
        print(
            f"🔄 Convertible: {self.name} | Brand: {self.brand} | "
            f"RAM: {self.ram_gb}GB | {gpu_status} | "
            f"Battery: {self.battery_level}% | State: {state} | "
            f"Mode: {mode}"
        )

    def toggle_mode(self):
        """Toggle between laptop and tablet mode."""
        self._is_tablet_mode = not self._is_tablet_mode
        mode = "Tablet" if self._is_tablet_mode else "Laptop"
        print(f"🔄 {self.name} switched to {mode} mode.")
