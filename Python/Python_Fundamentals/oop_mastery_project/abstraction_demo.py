# ============================================================================
#              abstraction_demo.py — ABSTRACTION (ABC)
# ============================================================================
# Abstraction = HIDING complex details, showing only what's needed.
#
# In Python, we use Abstract Base Classes (ABC) + @abstractmethod.
#
# KEY RULES:
#   1. You CANNOT create an object from an abstract class directly.
#   2. Child classes MUST implement ALL abstract methods.
#   3. Abstract classes CAN also have regular methods.
#
# Analogy: "Vehicle" says every vehicle must start() and stop(),
#          but HOW they do it is different for Car vs Motorcycle.
# ============================================================================

from abc import ABC, abstractmethod
import math


# --- Abstract Base Class ---
# Inherit from ABC + use @abstractmethod on methods children MUST implement.

class Shape(ABC):
    """Abstract class — you CANNOT create Shape() directly."""

    def __init__(self, color: str = "black"):
        self.color = color

    @abstractmethod
    def area(self) -> float:
        """Children MUST implement this."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Children MUST implement this."""
        pass

    # Regular method — children inherit this for free
    def describe(self):
        print(
            f"🎨 {self.__class__.__name__} | Color: {self.color} | "
            f"Area: {self.area():.2f} | Perimeter: {self.perimeter():.2f}"
        )


# --- Concrete Classes — They fill in the "blanks" ---

class Circle(Shape):
    def __init__(self, radius: float, color: str = "red"):
        super().__init__(color)
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float, color: str = "blue"):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float, color: str = "green"):
        super().__init__(color)
        self.a, self.b, self.c = a, b, c

    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c


# ============================================================================
#                      🚀 EXECUTION SECTION
# ============================================================================

if __name__ == "__main__":

    def section(title):
        print(f"\n{'='*55}")
        print(f"  {title}")
        print(f"{'='*55}\n")

    # 1. Can't create abstract class directly
    section("Abstract Class — Can't Instantiate")
    try:
        s = Shape("red")
    except TypeError as e:
        print(f"❌ {e}")

    # 2. Concrete classes work fine
    section("Concrete Classes Work")
    circle = Circle(5, "red")
    rect = Rectangle(4, 6, "blue")
    tri = Triangle(3, 4, 5, "green")

    circle.describe()
    rect.describe()
    tri.describe()

    # 3. All shapes guaranteed to have area() and perimeter()
    section("Uniform Interface — Guaranteed by ABC")
    for shape in [circle, rect, tri]:
        print(f"  {shape.__class__.__name__:10s} → Area: {shape.area():8.2f}")

    print("""
    KEY: ABC says "you MUST have these methods"
         Each child says "here's MY way of doing it"
    """)
