# ============================================================================
#              polymorphism_demo.py — POLYMORPHISM
# ============================================================================
# "Poly" = Many, "Morph" = Forms → Same method, different behavior.
#
# TWO TYPES:
#   1. Method Overriding — Child redefines parent's method
#   2. Duck Typing — "If it has .speak(), I can call .speak()"
#      (Python doesn't care about type, only about available methods)
# ============================================================================


# --- Method Overriding ---
# Same method name, different behavior per class.

class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self):
        print(f"🐾 {self.name} makes a generic sound.")


class Dog(Animal):
    def speak(self):  # Overrides Animal.speak()
        print(f"🐕 {self.name} says: Woof!")


class Cat(Animal):
    def speak(self):  # Overrides Animal.speak()
        print(f"🐱 {self.name} says: Meow!")


class Bird(Animal):
    def speak(self):
        print(f"🐦 {self.name} says: Tweet!")


class Fish(Animal):
    pass  # Does NOT override → uses Animal.speak()


# --- Duck Typing ---
# These classes are NOT related to Animal at all,
# but they have .speak() — and that's enough!

class Robot:
    def __init__(self, model: str):
        self.name = model

    def speak(self):
        print(f"🤖 {self.name} says: BEEP BOOP.")


class Parrot:
    def __init__(self, name: str, phrase: str):
        self.name = name
        self.phrase = phrase

    def speak(self):
        print(f"🦜 {self.name} says: '{self.phrase}'")


# --- Polymorphic Function ---
# ONE function that works with ANY object that has .speak()

def make_it_speak(thing):
    """Doesn't check type — just calls .speak(). That's duck typing!"""
    thing.speak()


# ============================================================================
#                      🚀 EXECUTION SECTION
# ============================================================================

if __name__ == "__main__":

    def section(title):
        print(f"\n{'='*55}")
        print(f"  {title}")
        print(f"{'='*55}\n")

    # 1. Method Overriding
    section("Method Overriding — Same Method, Different Output")
    dog = Dog("Buddy")
    cat = Cat("Whiskers")
    bird = Bird("Tweety")
    fish = Fish("Nemo")

    dog.speak()    # Dog's version
    cat.speak()    # Cat's version
    bird.speak()   # Bird's version
    fish.speak()   # Falls back to Animal's version

    # 2. Polymorphic function — one function handles all types
    section("Polymorphic Function — One Function, Many Types")
    for animal in [dog, cat, bird, fish]:
        make_it_speak(animal)

    # 3. Duck Typing — unrelated classes, same method
    section("Duck Typing — 'If It Has .speak(), It Works'")
    robot = Robot("T-800")
    parrot = Parrot("Polly", "Polly wants a cracker!")

    # Mix Animals, Robots, Parrots — ALL work with the same function!
    everything = [dog, cat, robot, parrot, bird]
    for thing in everything:
        make_it_speak(thing)

    print("""
    KEY: Same method name → different behavior per object.
         Duck typing: Python only cares "can it .speak()?"
    """)
