from pydantic import BaseModel
from typing import List

# 1. The "Child" Model
class Address(BaseModel):
    city: str
    zip_code: int

# 2. The "Parent" Model
class User(BaseModel):
    name: str
    # We use 'Address' just like we use 'str' or 'int'
    home_address: Address 
    
    # You can even have a LIST of nested models
    past_addresses: List[Address] = []

# --- THE CONCEPT ---

# The input data matches the nested structure
data = {
    "name": "Alice",
    "home_address": {
        "city": "New York",
        "zip_code": 10001
    },
    "past_addresses": [
        {"city": "Boston", "zip_code": 2108},
        {"city": "Chicago", "zip_code": 60601}
    ]
}

# Pydantic creates all the objects automatically!
user = User(**data)

print(f"{user.name} lives in {user.home_address.city}")
# Accessing nested data: user.home_address is now an Address object!