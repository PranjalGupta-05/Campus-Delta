from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

# --- API Request Models ---

class ChatRequest(BaseModel):
    """
    Structure for the incoming chat message from the frontend.
    """
    message: str

class ComplaintRequest(BaseModel):
    """
    Structure for registering a new complaint.
    """
    category: str
    text: str

# --- Database Response Models (Optional but good practice) ---

class FacultySchema(BaseModel):
    id: int
    name: str
    department: str
    subject: str
    cabin: str

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str

class ComplaintRequest(BaseModel):
    category: str
    text: str

# --- NEW AUTH MODELS ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str