# In the world of Pydantic,validators are "Automatic Triggers." 
# You define the rules once using the decorator, and Pydantic 
# handles the "calling" part for you every single time a new object is created.

from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str

    # 1. THE DECORATOR (@field_validator)
    # Think of this as a "Subscription." 
    # This function is now "subscribed" to watch the "username" field.
    @field_validator("username")
    def check_name_simple(cls, v: str) -> str:
        # 2. THE ARGUMENTS
        # 'cls' refers to the User class itself.
        # 'v' is the ACTUAL VALUE the user tried to provide (e.g., "Admin!").

        # 3. THE LOGIC (The Bouncer)
        # We check the value 'v'. If it fails our rule, we raise an error.
        if "!" in v:
            # This stops the code immediately and tells the user what's wrong.
            raise ValueError("No exclamation marks!")
            
        # 4. THE RETURN (The Pass)
        # You MUST return 'v'. If you don't, the username will become None.
        # This is also where you could do: return v.lower() to fix the data.
        return v  

# --- HOW IT WORKS ---
# user = User(username="John")   <- WORKS (returns "John")
# user = User(username="John!")  <- CRASHES (raises ValueError)