from pydantic import BaseModel, ValidationError
## 'typing' is the toolbox that lets us describe complicated data structures
from typing import List, Dict, Optional 

class Player(BaseModel):
    # 1. SIMPLE TYPE
    name: str 

    # 2. OPTIONAL: Can be string or None. Defaults to None if missing.
    guild: Optional[str] = None 

    # 3. LIST: Every item inside must be an integer.
    scores: List[int] 

    # 4. DICT: Keys must be strings, Values must be Booleans.
    stats: Dict[str, bool]

# --- CASE 1: VALID INPUT ---
valid_data = {
    "name": "Aragorn",
    "guild": "Rangers",
    "scores": [10, 20, "30"], # Pydantic will convert "30" to 30 automatically!
    "stats": {"is_alive": True, "has_magic": False}
}

print("--- Attempting Valid Input ---")
player1 = Player(**valid_data)
print(f"Player Name: {player1.name}")
print(f"Player Scores: {player1.scores}")
print(f"Stats Dictionary: {player1.stats}")


# # --- CASE 2: INVALID INPUT ---
# # We wrap this in a try/except block because Pydantic will raise an error
# invalid_data = {
#     "name": "Gandalf",
#     "scores": [10, "high_score"], # ERROR: "high_score" cannot be turned into an int
#     "stats": {1: "Maybe"}         # ERROR: Value must be bool (True/False), not a string
# }

# print("\n--- Attempting Invalid Input ---")
# try:
#     player2 = Player(**invalid_data)
# except ValidationError as e:
#     # This prints a very detailed report of what exactly went wrong
#     print("Validation failed with the following errors:")
#     print(e)