
# To understand Serialization, think of your Pydantic model as a "Living Object" in Python memory. 
# Serialization is the process of turning that living object into a format that can be stored
#  or sent elsewhere (like a Dictionary or a JSON string).

from pydantic import BaseModel, ConfigDict

class Product(BaseModel):
    # 1. THE CONFIGURATION (Settings for the whole Model)
      
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Automatically removes "  " from strings
        extra="forbid",             # Crashes if user gives extra unknown fields
        frozen=True                 # Makes the object "Read-Only" once created
    )

    name: str
    price: float
    category: str

# --- 2. CREATING THE OBJECT ---
# Notice the extra spaces in "  Gadgets  " - ConfigDict will clean this!
item = Product(name="Laptop", price=999.99, category="  Gadgets  ")

print(f"Cleaned Category: '{item.category}'") # Output: 'Gadgets'

# --- 3. SERIALIZATION (Exporting Data) ---

# A. Convert to a Python DICTIONARY
# Use 'exclude' to hide specific fields from the output
product_dict = item.model_dump(exclude={"category"})
print(f"Dictionary (No Category): {product_dict}")
# Output: {'name': 'Laptop', 'price': 999.99}

# B. Convert to a JSON STRING
# Use 'indent' to make the string pretty and readable
product_json = item.model_dump_json(indent=2)
print(f"JSON String:\n{product_json}")
"""
Output:
{
  "name": "Laptop",
  "price": 999.99,
  "category": "Gadgets"
}
"""

# --- 4. THE 'FROZEN' RULE ---
# Because we set frozen=True in ConfigDict, this line would cause an Error:
# item.price = 500.0