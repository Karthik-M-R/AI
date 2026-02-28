from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    # 1. We use @property so we can call 'rect.area' instead of 'rect.area()'
    # 2. We use @computed_field so 'area' shows up in model_dump() and JSON
    @computed_field
    @property
    def area(self) -> float:
        """Calculates area on the fly. No () needed to access."""
        print("--- Logic running inside the property ---")
        return self.width * self.height

# --- Execution ---

# Create the object with only width and height
rect = Rectangle(width=5.0, height=10.0)

# STEP A: Accessing like a variable (Property Power)
# Notice: No brackets used!
print(f"The area is: {rect.area}") 

# STEP B: Checking the Data Export (Computed Field Power)
# In standard Python, @property is HIDDEN from dicts. 
# Because of @computed_field, it is INCLUDED here.
print("Dictionary Output:", rect.model_dump())

# STEP C: Changing values
rect.width = 10.0
print(f"New area is automatically: {rect.area}")