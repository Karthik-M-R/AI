from pydantic import BaseModel
from typing import List, Optional

class Folder(BaseModel):
    name: str
    # We put 'Folder' in quotes because the class isn't "finished" yet
    # This allows a folder to contain a list of other Folders
    subfolders: List["Folder"] = []

# This is the "Magic" command. 
# It tells Pydantic: "Now that the class is finished, go back and 
# link all those 'Folder' strings to the actual Folder class."
Folder.model_rebuild()

# --- THE CONCEPT ---

data = {
    "name": "Root",
    "subfolders": [
        {
            "name": "Movies",
            "subfolders": [{"name": "Action", "subfolders": []}]
        },
        {
            "name": "Music",
            "subfolders": []
        }
    ]
}

root = Folder(**data)
print(f"Root folder: {root.name}")
print(f"First subfolder: {root.subfolders[0].name}")
print(f"Deep nested folder: {root.subfolders[0].subfolders[0].name}")
