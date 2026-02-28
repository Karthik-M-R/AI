from pydantic import BaseModel, Field, model_validator

class UserSignup(BaseModel):
    username: str
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    # This function runs automatically to compare fields
    @model_validator(mode="after")#mode="after" means it runs your custom validation logic after Pydantic has already finished its 
    #own internal checks (like checking types, min_length, and required fields).
    def check_passwords_match(self):
        # Check if the two fields are NOT the same
        if self.password != self.confirm_password:
            raise ValueError("mismatched passwords")
        
        # If they match, we return 'self' to say "all good!"
        return self

# --- THE CONCEPT ---

# 1. This will work perfectly:
user_ok = UserSignup(
    username="bolt", 
    password="super-secret", 
    confirm_password="super-secret"
)
print(f"Validated: {user_ok.username}")

# 2. This would CRASH the program with a 'ValueError':
# user_bad = UserSignup(username="bolt", password="password123", confirm_password="different")