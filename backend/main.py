import sqlite3
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from better_profanity import profanity
from datetime import datetime
import random

# Import models from the file we created earlier
from models import ChatRequest, ComplaintRequest, UserCreate, UserLogin

app = FastAPI(title="SmartCampus AI - Secure")

# --- Security & Semantics Setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
profanity.load_censor_words() # Load default bad words

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "campus_data.db"

# --- 1. Database & Security Functions ---

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Existing tables
    c.execute('''CREATE TABLE IF NOT EXISTS faculty 
                 (id INTEGER PRIMARY KEY, name TEXT, department TEXT, subject TEXT, cabin TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS complaints 
                 (id INTEGER PRIMARY KEY, type TEXT, description TEXT, status TEXT, date TEXT)''')
    
    # NEW: Users Table for Auth
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password_hash TEXT, role TEXT)''')
    
    # Dummy Faculty Data
    c.execute("SELECT count(*) FROM faculty")
    if c.fetchone()[0] == 0:
        faculty_data = [
            ("Dr. Sharma", "CS", "Data Structures", "Cabin 204, Block A"),
            ("Prof. Anjali", "CS", "OOPs & Java", "Cabin 101, Block B"),
        ]
        c.executemany("INSERT INTO faculty (name, department, subject, cabin) VALUES (?,?,?,?)", faculty_data)
        conn.commit()
    conn.close()

init_db()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- 2. Auth Endpoints (Sign Up / Sign In) ---

@app.post("/register")
async def register(user: UserCreate):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Check if user exists
    c.execute("SELECT * FROM users WHERE username=?", (user.username,))
    if c.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Hash password and save
    hashed_pw = get_password_hash(user.password)
    c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
              (user.username, hashed_pw, "student"))
    conn.commit()
    conn.close()
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: UserLogin):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username=?", (user.username,))
    row = c.fetchone()
    conn.close()
    
    if not row or not verify_password(user.password, row[0]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {"message": "Login successful", "user": user.username}

# --- 3. AI Brain with Semantic Guardrails ---

def get_ai_response(query: str):
    # SEMANTIC GUARDRAIL: Check for inappropriate language
    if profanity.contains_profanity(query):
        return "⚠️ **System Alert:** Your message contains inappropriate language. Please maintain academic decorum."

    query = query.lower()
    
    # ... (Keep your existing Intent Logic for Faculty, Mess, Labs here) ...
    # ... Copied from previous code ...
    
    if "teach" in query or "faculty" in query:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM faculty")
        rows = c.fetchall()
        conn.close()
        for row in rows:
            if row[3].lower() in query:
                return f"👨‍🏫 {row[1]} teaches {row[3]}. Cabin: {row[4]}."
        return "👨‍🏫 I couldn't find that faculty. Try asking 'Who teaches Java?'"

    if "mess" in query:
        return "🍛 Today's Menu: Rajma Chawal & Curd. Dinner: Egg Curry."

    if "complaint" in query:
        return "🛠️ Type 'Complaint: [Issue]' to register a ticket."

    if query.startswith("complaint:"):
        issue = query.replace("complaint:", "").strip()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO complaints (type, description, status, date) VALUES (?, ?, ?, ?)", 
                  ("General", issue, "Open", str(datetime.now())))
        conn.commit()
        conn.close()
        return f"✅ Complaint Registered. ID #{random.randint(1000,9999)}."

    return "🤖 I am SmartCampus AI. Ask me about Faculty, Mess, or Complaints."

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    response_text = get_ai_response(req.message)
    return {"reply": response_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)