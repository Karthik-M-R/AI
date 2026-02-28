from pydantic import BaseModel, ValidationError

# 1. Define the structure
class User(BaseModel):
    username: str
    age: int
    is_premium: bool = False

# --- CASE 1: VALID DATA ---
# This dictionary has a string for age, but Pydantic will "coerce" (fix) it into an int.
valid_data = {
    "username": "coder_123",
    "age": "25", 
    "is_premium": True
}

user = User(**valid_data) # The ** unpacks the dictionary into arguments
print(f"User: {user.username}, Age: {user.age}") 
# Output: User: coder_123, Age: 25 (as an integer)


# --- CASE 2: INVALID DATA ---
# This will fail for two reasons:
# 1. 'age' cannot be converted from "old" to a number.
# 2. 'username' is missing entirely.
invalid_data = {
    "age": "old",
    "is_premium": False
}

try:
    User(**invalid_data)
except ValidationError as e:
    print("\nErrors found:")
    print(e) 
    # Logic: Pydantic will report: "Field required [type=missing_keyword, loc=('username',)]"
    # and: "Input should be a valid integer [type=int_parsing, loc=('age',)]"