# ============================================================================
#             composition_demo.py — COMPOSITION (HAS-A)
# ============================================================================
# Composition = a class CONTAINS objects of other classes.
#
# Inheritance:  "SmartPhone IS-A Device"    (IS-A)
# Composition:  "Car HAS-A Engine"          (HAS-A)
#
# WHY use it?
#   - More flexible than inheritance
#   - You can swap components at runtime
#   - Avoids deep inheritance chains
#   - "Favor composition over inheritance" — design principle
# ============================================================================


# --- Components — small, reusable, independent parts ---

class Engine:
    """Standalone engine — doesn't know it's inside a Car."""

    def __init__(self, horsepower: int, fuel_type: str = "Petrol"):
        self.horsepower = horsepower
        self.fuel_type = fuel_type
        self._is_running = False

    def start(self):
        if not self._is_running:
            self._is_running = True
            print(f"🔧 Engine started! ({self.horsepower}HP, {self.fuel_type})")

    def stop(self):
        if self._is_running:
            self._is_running = False
            print("🔴 Engine stopped.")

    @property
    def is_running(self):
        return self._is_running

    def __str__(self):
        state = "Running" if self._is_running else "Off"
        return f"Engine({self.horsepower}HP, {self.fuel_type}, {state})"


class Battery:
    """Standalone battery — manages charge independently."""

    def __init__(self, capacity_kwh: float):
        self.capacity_kwh = capacity_kwh
        self._charge = 100

    def drain(self, amount: float):
        self._charge = max(0, self._charge - amount)
        print(f"🔋 Battery: {self._charge}% remaining")

    def recharge(self):
        self._charge = 100
        print(f"⚡ Battery recharged to 100%!")

    @property
    def charge_level(self):
        return self._charge

    def __str__(self):
        return f"Battery({self.capacity_kwh}kWh, {self._charge}%)"


class GPS:
    """Standalone GPS — handles navigation."""

    def __init__(self):
        self._destination = None

    def navigate(self, destination: str):
        self._destination = destination
        print(f"📍 GPS: Navigating to '{destination}'")

    def __str__(self):
        return f"GPS(to='{self._destination}')"


# --- Car — COMPOSED of Engine + Battery + GPS ---
# Car doesn't inherit from Engine. It HAS an Engine.

class Car:
    """Car HAS-A Engine, HAS-A Battery, HAS-A GPS (optional)."""

    def __init__(self, model: str, engine: Engine, battery: Battery, gps: GPS = None):
        self.model = model
        self.engine = engine      # HAS-A Engine
        self.battery = battery    # HAS-A Battery
        self.gps = gps            # HAS-A GPS (optional)

    def start(self):
        print(f"\n🚗 Starting {self.model}...")
        if self.battery.charge_level > 0:
            self.engine.start()
            self.battery.drain(5)
        else:
            print("❌ Can't start — battery is dead!")

    def drive(self, destination: str, distance_km: float):
        if not self.engine.is_running:
            print(f"❌ Start the engine first!")
            return
        if self.gps:
            self.gps.navigate(destination)
        self.battery.drain(distance_km * 0.5)
        print(f"🚗 {self.model} drove {distance_km}km to '{destination}'")

    def status(self):
        print(f"\n📊 {self.model}: {self.engine} | {self.battery}")


# ============================================================================
#                      🚀 EXECUTION SECTION
# ============================================================================

if __name__ == "__main__":

    def section(title):
        print(f"\n{'='*55}")
        print(f"  {title}")
        print(f"{'='*55}\n")

    # 1. Create components, then compose them
    section("Composing a Car from Components")
    engine = Engine(450, "Petrol")
    battery = Battery(75.0)
    gps = GPS()

    car = Car("Tesla Model S", engine, battery, gps)
    car.start()
    car.drive("Mall", 15)
    car.status()

    # 2. Swap components at runtime — try this with inheritance!
    section("Swapping Components at Runtime")
    car.engine = Engine(600, "Electric")
    car.start()
    car.status()

    # 3. Car without GPS — optional composition
    section("Optional Components")
    basic = Car("Maruti 800", Engine(50, "Petrol"), Battery(30.0))
    basic.start()
    basic.drive("Market", 5)

    print("""
    KEY: Inheritance = IS-A  (Dog IS-A Animal)
         Composition = HAS-A (Car HAS-A Engine)
         Components are reusable and swappable!
    """)
