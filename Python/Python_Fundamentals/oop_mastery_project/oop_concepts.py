# ============================================================================
#                    oop_concepts.py — THE MASTER FILE
# ============================================================================
#
# This SINGLE FILE contains ALL 11 OOP concepts for quick study.
# Run this file directly:  python oop_concepts.py
#
# For the PROFESSIONAL multi-file version, see the 'electronics/' package.
#
# TABLE OF CONTENTS:
#   Line ~30   — Building a Class
#   Line ~40   — Namespace (Class vs Instance)
#   Line ~75   — self Argument
#   Line ~85   — Constructors (__init__)
#   Line ~130  — Static Method
#   Line ~150  — Class Method
#   Line ~175  — Property Decorator (Getter/Setter)
#   Line ~220  — Inheritance
#   Line ~250  — Attribute Shadowing
#   Line ~275  — super()
#   Line ~310  — MRO (Method Resolution Order)
#   Line ~360  — EXECUTION SECTION (Testing everything)
# ============================================================================

from functools import wraps


# ============================================================================
# BUILDING A CLASS
# ============================================================================
# A CLASS is a blueprint/template.
# An OBJECT is a real thing ("instance") created from that blueprint.
#
#   Class  = Cookie Cutter      (defines the shape)
#   Object = Cookie             (the actual thing you eat)
#
# Syntax:
#   class ClassName:
#       ...
#
#   my_object = ClassName()     ← Creating an object (instantiation)
# ============================================================================

class Robot:
    """
    Robot is our blueprint. Every Robot object will have a name,
    a battery level, and a version number.
    """

    # ========================================================================
    # NAMESPACE
    # ========================================================================
    # Python has TWO types of namespaces inside a class:
    #
    # 1. CLASS NAMESPACE — Variables defined directly in the class body.
    #    These are SHARED by ALL instances. Like a whiteboard on the wall
    #    that every robot can see and update.
    #
    # 2. INSTANCE NAMESPACE — Variables assigned to 'self' inside methods.
    #    These are UNIQUE to each object. Like a name tag on each robot.
    #
    # LOOKUP ORDER: When you access robot.something, Python checks:
    #    instance namespace → class namespace → parent class → error
    # ========================================================================

    population = 0  # CLASS namespace — shared by ALL Robot objects

    # ========================================================================
    # CONSTRUCTORS (__init__)
    # ========================================================================
    # __init__ (pronounced "dunder init") is the CONSTRUCTOR.
    # It runs AUTOMATICALLY when you create a new object:
    #     robot = Robot("R2D2", 1.0)
    #             ↑ This triggers __init__
    #
    # Purpose: Set up the object's INITIAL STATE (its "DNA at birth").
    #
    # Parameters:
    #   self    — the new object being created (see 'self' section)
    #   name    — the robot's name
    #   version — the robot's software version
    # ========================================================================

    def __init__(self, name, version):
        # ====================================================================
        # self ARGUMENT
        # ====================================================================
        # 'self' is a REFERENCE to the CURRENT OBJECT (the one being created
        # or the one calling the method).
        #
        # When you create two robots:
        #     r1 = Robot("R2D2", 1.0)    → inside __init__, self = r1
        #     r2 = Robot("C3PO", 2.0)    → inside __init__, self = r2
        #
        # 'self' is how each object keeps its own data separate.
        #
        # Think of 'self' as the word "MY":
        #   r1 says: "MY name is R2D2"      → self.name = "R2D2"
        #   r2 says: "MY name is C3PO"      → self.name = "C3PO"
        #
        # NOTE: 'self' is just a convention. You COULD name it anything
        #       (like 'this'), but ALWAYS use 'self' — it's the Python way.
        # ====================================================================

        # INSTANCE namespace variables (unique per object)
        self.name = name                # Public — anyone can access
        self._battery = 100             # "Private" by convention (underscore)
        self.version = version          # Public

        # Updating the CLASS namespace variable (shared counter)
        # We use Robot.population (not self.population) to be explicit
        # that we're modifying the shared class variable.
        Robot.population += 1
        print(f"🤖 Robot '{self.name}' v{self.version} initialized. "
              f"(Total robots: {Robot.population})")

    # ========================================================================
    # INSTANCE METHODS (continued)
    # ========================================================================
    # Instance methods are regular methods that take 'self'.
    # They can access and modify the specific object's data.
    # ========================================================================

    def report(self):
        """Instance method — uses 'self' to access THIS robot's data."""
        print(f"📋 I am {self.name}. Battery: {self._battery}%. Version: {self.version}")

    def use_battery(self, amount):
        """Drain the battery by a given amount."""
        self._battery = max(0, self._battery - amount)
        if self._battery == 0:
            print(f"🔴 {self.name} has run out of battery!")
        else:
            print(f"⚡ {self.name} used {amount}% battery. Remaining: {self._battery}%")

    # ========================================================================
    # STATIC METHOD
    # ========================================================================
    # @staticmethod marks a method that:
    #   - Does NOT receive 'self' (no object access)
    #   - Does NOT receive 'cls' (no class access)
    #   - Is just a regular function that LOGICALLY BELONGS to the class
    #
    # When to use:
    #   When you have a utility function related to the class, but it
    #   doesn't need any object or class data to do its job.
    #
    # Analogy: A calculator hanging on the robot factory wall.
    #          Any worker can use it. It doesn't know which worker pressed
    #          the buttons, and it doesn't care.
    #
    # Can be called via:
    #   Robot.utility_check_system()      ← on the class
    #   my_robot.utility_check_system()   ← on an instance (also works)
    # ========================================================================

    @staticmethod
    def utility_check_system():
        """
        Static method — doesn't need 'self' or 'cls'.
        It's a helper tool, like a standalone function inside the class.
        """
        return "✅ System signals are green. All systems operational."

    @staticmethod
    def is_valid_version(version):
        """Another static method: validates a version number."""
        return isinstance(version, (int, float)) and version > 0

    # ========================================================================
    # CLASS METHOD
    # ========================================================================
    # @classmethod marks a method that:
    #   - Receives the CLASS ITSELF as the first argument ('cls')
    #   - Can access/modify CLASS-LEVEL data (like population)
    #   - Cannot access instance-level data (no 'self')
    #
    # When to use:
    #   1. To access/modify class variables (like a global counter)
    #   2. As ALTERNATIVE CONSTRUCTORS (factory methods)
    #
    # Analogy: The factory manager. They know how many robots the factory
    #          has made total (cls.population), but they don't know the
    #          specific battery level of Robot #47.
    #
    # 'cls' vs 'self':
    #   self → "this specific robot"
    #   cls  → "the Robot class itself (the factory)"
    # ========================================================================

    @classmethod
    def total_robots(cls):
        """
        Class method — acts on the CLASS, not an instance.
        'cls' refers to the Robot class itself.
        """
        return f"📊 Total robots in existence: {cls.population}"

    @classmethod
    def create_from_string(cls, robot_string):
        """
        ALTERNATIVE CONSTRUCTOR — a factory method.
        Creates a Robot from a string like "R2D2:1.0"

        Usage:
            robot = Robot.create_from_string("R2D2:1.0")
            # Instead of: robot = Robot("R2D2", 1.0)

        WHY use 'cls' instead of 'Robot'?
            So subclasses (WorkingRobot, Drone) create instances of
            THEIR OWN type, not always a plain Robot.
        """
        name, version = robot_string.split(":")
        return cls(name.strip(), float(version.strip()))

    # ========================================================================
    # PROPERTY DECORATOR (Getter / Setter)
    # ========================================================================
    # @property lets you access a METHOD as if it were a SIMPLE VARIABLE.
    #
    # Instead of:  print(robot.get_battery())     ← ugly function call
    # You write:   print(robot.battery_level)     ← clean, like a variable!
    #
    # BUT Python is running a method behind the scenes! This lets you:
    #   - VALIDATE data (reject bad values)
    #   - COMPUTE data on the fly
    #   - LOG access (track who reads/writes)
    #
    # TWO PARTS:
    #   @property           → the GETTER (runs when you READ)
    #   @name.setter        → the SETTER (runs when you WRITE)
    #
    # Analogy: A bank teller (property) vs walking into the vault yourself.
    #   - Reading:  "What's my balance?" → teller looks it up (getter)
    #   - Writing:  "Deposit $500" → teller checks the money first (setter)
    # ========================================================================

    @property
    def battery_level(self):
        """
        GETTER — runs when you READ battery_level.

        Usage:
            print(robot.battery_level)    ← Looks like a variable
            # But this method is actually running!
        """
        return f"{self._battery}%"

    @battery_level.setter
    def battery_level(self, value):
        """
        SETTER — runs when you WRITE to battery_level.

        Usage:
            robot.battery_level = 85      ← Looks like assignment
            # But this method runs and VALIDATES the value first!
        """
        if isinstance(value, (int, float)) and 0 <= value <= 100:
            self._battery = value
            print(f"🔋 {self.name} battery set to {self._battery}%.")
        else:
            print(f"❌ Invalid battery level: {value}! Must be 0–100.")

    def __str__(self):
        """Human-readable string for print()."""
        return f"Robot(name='{self.name}', v{self.version}, battery={self._battery}%)"


# ============================================================================
# INHERITANCE (IS-A Relationship)
# ============================================================================
# Inheritance lets a NEW class (child) REUSE all code from an EXISTING class
# (parent), then ADD or CHANGE things.
#
# Syntax: class Child(Parent):
#
# WorkingRobot IS-A Robot:
#   - It has everything a Robot has (name, battery, report, etc.)
#   - PLUS its own feature: a tool
#
# Without inheritance, you'd copy-paste all of Robot's code. Nightmare!
# With inheritance, you write ONLY the new/changed parts.
# ============================================================================

class WorkingRobot(Robot):
    """
    WorkingRobot IS-A Robot, but with an extra feature: a tool.
    Inheritance chain: WorkingRobot → Robot → object
    """

    def __init__(self, name, version, tool):
        # ==================================================================
        # super() — ACCESSING THE BASE (PARENT) CLASS
        # ==================================================================
        # super() gives you a REFERENCE to the parent class, so you can
        # call its methods.
        #
        # super().__init__(name, version) calls Robot.__init__() which:
        #   - Sets self.name, self._battery, self.version
        #   - Increments Robot.population
        #
        # WITHOUT super():
        #   You'd have to copy ALL of Robot.__init__'s code here.
        #   If Robot changes, you'd have to update WorkingRobot too.
        #
        # WITH super():
        #   Robot's __init__ handles its own setup.
        #   WorkingRobot only adds what's NEW (self.tool).
        #
        # Analogy: Your parents gave you a name and a home (super().__init__).
        #          Then YOU chose your own career (self.tool).
        # ==================================================================
        super().__init__(name, version)  # Let Robot do its standard setup
        self.tool = tool                # WorkingRobot-specific attribute

    # ========================================================================
    # ATTRIBUTE SHADOWING (Method Override)
    # ========================================================================
    # When a child defines a method with the SAME NAME as the parent,
    # the child's version SHADOWS (overrides) the parent's.
    #
    # Calling worker.report():
    #   Python checks WorkingRobot first → finds report() → uses IT.
    #   Robot.report() still exists but is hidden behind the child's version.
    #
    # Calling robot.report():
    #   Python checks Robot → finds report() → uses IT.
    #   (No shadowing here because it's a plain Robot.)
    #
    # You can still access the parent's version via:
    #   super().report()  → explicitly calls Robot.report()
    # ========================================================================

    def report(self):
        """
        SHADOWS Robot.report().
        When WorkingRobot.report() is called, this version runs
        instead of the parent's.
        """
        print(f"🔧 Worker '{self.name}' is ready with a {self.tool}. "
              f"Battery: {self._battery}%")


# ============================================================================
# METHOD RESOLUTION ORDER (MRO)
# ============================================================================
# MRO is the ORDER in which Python searches for a method.
#
# With SINGLE inheritance (A → B), it's simple: check A, then B.
# With MULTIPLE inheritance (A inherits B AND C), Python needs a rule:
#
# THE C3 LINEARIZATION ALGORITHM:
#   - Go LEFT to RIGHT in the parent list
#   - Depth-first, but never visit the same class twice
#
# For the 'Drone' class below:
#   class Drone(WorkingRobot, CombatRobot):
#
# MRO: Drone → WorkingRobot → CombatRobot → Robot → object
#
# When you call drone.report():
#   1. Check Drone — has report()? NO
#   2. Check WorkingRobot — has report()? YES → Use WorkingRobot.report()
#   (Stops here. Never reaches CombatRobot or Robot.)
#
# When you call drone.action():
#   1. Check Drone — has action()? NO
#   2. Check WorkingRobot — has action()? NO
#   3. Check CombatRobot — has action()? YES → Use CombatRobot.action()
#
# Analogy: Lost your keys? Check:
#   1. Your pockets (Drone)
#   2. Your desk (WorkingRobot)
#   3. The kitchen (CombatRobot)
#   4. The junk drawer (Robot)
#   Stop as soon as you find them!
# ============================================================================

class CombatRobot(Robot):
    """A Robot with combat capabilities."""

    def __init__(self, name, version, weapon="Laser"):
        super().__init__(name, version)
        self.weapon = weapon

    def action(self):
        """Combat-specific action."""
        print(f"⚔️  {self.name} is defending with {self.weapon}!")


class Drone(WorkingRobot, CombatRobot):
    """
    Drone inherits from BOTH WorkingRobot AND CombatRobot.
    This is MULTIPLE INHERITANCE.

    MRO: Drone → WorkingRobot → CombatRobot → Robot → object

    Drone gets:
      - report() from WorkingRobot (shadowed)
      - action() from CombatRobot
      - battery_level, turn_on, etc. from Robot
    """

    def __init__(self, name, version, tool, weapon="Laser"):
        # In multiple inheritance, super() follows the MRO chain.
        # It calls WorkingRobot.__init__() which calls Robot.__init__().
        super().__init__(name, version, tool)
        self.weapon = weapon  # Also set the weapon from CombatRobot

    def fly(self):
        """Drone-specific method."""
        if self._battery > 0:
            self.use_battery(10)
            print(f"🚁 {self.name} is flying!")
        else:
            print(f"🔴 {self.name} can't fly — no battery!")


# ============================================================================
#                      🚀 EXECUTION SECTION
# ============================================================================
# Below we TEST everything. Run this file and see all concepts in action!
# ============================================================================

if __name__ == "__main__":

    def section(title):
        """Print a visual section divider."""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")

    # -----------------------------------------------------------------------
    # Creating Objects (Instantiation)
    # -----------------------------------------------------------------------
    section("Creating Objects from the Robot Blueprint")

    bot1 = Robot("R2D2", 1.0)
    bot2 = Robot("C3PO", 2.0)
    print(f"\nbot1: {bot1}")
    print(f"bot2: {bot2}")

    # -----------------------------------------------------------------------
    # Namespace — Class vs Instance
    # -----------------------------------------------------------------------
    section("Namespace: Shared (Class) vs Unique (Instance)")

    print(f"Robot.population (CLASS level): {Robot.population}")   # Shared: 2
    print(f"bot1.name (INSTANCE level): {bot1.name}")              # Unique: R2D2
    print(f"bot2.name (INSTANCE level): {bot2.name}")              # Unique: C3PO
    print(f"bot1.population: {bot1.population}")                   # Reads CLASS level
    print(f"bot2.population: {bot2.population}")                   # Same shared value

    # -----------------------------------------------------------------------
    # Attribute Shadowing
    # -----------------------------------------------------------------------
    section("Attribute Shadowing: Child Overrides Parent")

    worker = WorkingRobot("Wall-E", 2.0, "Compactor")
    print("\nCalling .report() on Robot vs WorkingRobot:\n")
    bot1.report()     # → Robot.report()        (parent's version)
    worker.report()   # → WorkingRobot.report()  (shadowed version!)

    # -----------------------------------------------------------------------
    # self — Different Object, Same Method
    # -----------------------------------------------------------------------
    section("'self' Argument: Each Object Calls Its Own")

    # bot1.report() passes bot1 as 'self'
    # bot2.report() passes bot2 as 'self'
    # Same method, different data!
    bot1.report()
    bot2.report()
    worker.report()

    # -----------------------------------------------------------------------
    # Constructor — Already demonstrated at object creation
    # -----------------------------------------------------------------------
    section("Constructor (__init__): Runs at Birth")

    print("Every Robot() call above triggered __init__ automatically.")
    print("Let's create one more to see it happen:\n")
    bot3 = Robot("BB-8", 3.5)

    # -----------------------------------------------------------------------
    # Inheritance — Child reuses Parent
    # -----------------------------------------------------------------------
    section("Inheritance: WorkingRobot IS-A Robot")

    print(f"Is worker a WorkingRobot? {isinstance(worker, WorkingRobot)}")  # True
    print(f"Is worker a Robot?        {isinstance(worker, Robot)}")         # True!
    print(f"Is bot1 a WorkingRobot?   {isinstance(bot1, WorkingRobot)}")    # False
    print(f"\nWorker can use Robot's methods (inherited):")
    worker.use_battery(20)  # Inherited from Robot

    # -----------------------------------------------------------------------
    # super() — Already demonstrated inside WorkingRobot.__init__
    # -----------------------------------------------------------------------
    section("super(): Calling the Parent")

    print("super().__init__() was called inside WorkingRobot.__init__().")
    print("This set up name, battery, version (Robot's job) before")
    print("WorkingRobot added 'tool' (its own job).")
    print(f"\nWorker name: {worker.name} (set by Robot via super)")
    print(f"Worker tool: {worker.tool} (set by WorkingRobot itself)")

    # -----------------------------------------------------------------------
    # MRO — Method Resolution Order
    # -----------------------------------------------------------------------
    section("MRO: The Method Search Order")

    drone = Drone("SkyNet", 5.0, "Scanner", "Missiles")

    print("MRO for Drone class:")
    for i, cls in enumerate(Drone.mro()):
        print(f"  {i+1}. {cls.__name__}")

    print(f"\ndrone.report() → found in WorkingRobot (step 2 of MRO):")
    drone.report()

    print(f"\ndrone.action() → found in CombatRobot (step 3 of MRO):")
    drone.action()

    print(f"\ndrone.fly() → found in Drone itself (step 1 of MRO):")
    drone.fly()

    # -----------------------------------------------------------------------
    # Static Method — Pure utility, no self/cls
    # -----------------------------------------------------------------------
    section("Static Method: Utility Functions")

    print(f"System check: {Robot.utility_check_system()}")
    print(f"Is version 3.0 valid? {Robot.is_valid_version(3.0)}")
    print(f"Is version -1 valid?  {Robot.is_valid_version(-1)}")
    print(f"Called on instance:   {bot1.utility_check_system()}")

    # -----------------------------------------------------------------------
    # Class Method — Acts on the class
    # -----------------------------------------------------------------------
    section("Class Method: Factory-Level Operations")

    print(Robot.total_robots())

    print("\nAlternative constructor — creating Robot from a string:")
    bot4 = Robot.create_from_string("Optimus : 7.0")
    print(f"Created: {bot4}")

    print(f"\nUpdated count: {Robot.total_robots()}")

    # -----------------------------------------------------------------------
    # Property — Getter/Setter with validation
    # -----------------------------------------------------------------------
    section("Property: Controlled Access (Getter/Setter)")

    print(f"Read battery (GETTER):   {bot1.battery_level}")

    print("\nSet battery to 85 (SETTER with validation):")
    bot1.battery_level = 85    # Valid — setter accepts it

    print("\nSet battery to 150 (SETTER rejects it!):")
    bot1.battery_level = 150   # Invalid — setter blocks it

    print(f"\nFinal battery: {bot1.battery_level}")  # Still 85%

    # -----------------------------------------------------------------------
    # Final Summary
    # -----------------------------------------------------------------------
    section("🏆 ALL OOP CONCEPTS DEMONSTRATED!")

    print(f"Total robots created: {Robot.population}")
    print("""
    ┌──────────────────────────┬─────────────────────────────────────┐
    │ Concept                  │ Remember This                       │
    ├──────────────────────────┼─────────────────────────────────────┤
    │ Building a Class         │ Blueprint → cookie cutter            │
    │ Namespace                │ Class=shared, Instance=unique        │
    │ Attribute Shadowing      │ Child's version wins                 │
    │ self                     │ "MY data" — each object's identity   │
    │ __init__                 │ Runs at birth, sets up DNA           │
    │ Inheritance              │ Child reuses parent's code (IS-A)    │
    │ super()                  │ "Hey parent, do your thing first"    │
    │ MRO                      │ Search order: left → right → up      │
    │ Static Method            │ Toolbox function, no self/cls        │
    │ Class Method             │ Factory manager, uses cls            │
    │ Property                 │ Bouncer/teller for your data         │
    └──────────────────────────┴─────────────────────────────────────┘
    """)
