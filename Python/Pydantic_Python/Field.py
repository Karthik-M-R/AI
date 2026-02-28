from pydantic import BaseModel, Field

class Employee(BaseModel):
    # '...' means this is REQUIRED. User must provide a name.
    # min_length ensures the string isn't empty or just a single letter.
    name: str = Field(..., min_length=2, description="The full name of the employee")

    # 'ge=18' (Greater than or Equal to 18)
    # 'le=65' (Less than or Equal to 65)
    age: int = Field(..., ge=18, le=65, description="Age must be between 18 and 65")

    # We provide a default value (0.0), so this is NOT required.
    # 'gt=0' (Must be strictly Greater Than 0)
    salary: float = Field(default=0.0, gt=0, description="Monthly salary in USD")

    # 'max_length' limits the string size
    office_code: str = Field(..., min_length=3, max_length=5)

# --- SUCCESSFUL INPUT ---
# Pydantic validates all these rules at the moment of creation
emp = Employee(
    name="Alice", 
    age=30, 
    salary=5000.50, 
    office_code="NYC01"
)

print(f"Name: {emp.name}")
print(f"Description of age field: {Employee.model_fields['age'].description}")