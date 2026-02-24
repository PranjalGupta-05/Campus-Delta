import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from better_profanity import profanity
from datetime import datetime
import random

from models import ChatRequest, ComplaintRequest, UserCreate, UserLogin

app = FastAPI(title="SmartCampus AI - Final Email Version")

# --- Security Setup ---
profanity.load_censor_words()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pranjal@2005",  # <--- MUST UPDATE THIS
        database="smartcampus"
    )

def init_db():
    try:
        server_conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pranjal@2005"   # <--- MUST UPDATE THIS
        )
        cursor = server_conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS smartcampus")
        server_conn.close()

        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS faculty (
                     id INT AUTO_INCREMENT PRIMARY KEY, 
                     name VARCHAR(100), department VARCHAR(50), 
                     subject VARCHAR(100), cabin VARCHAR(100))''')
                     
        c.execute('''CREATE TABLE IF NOT EXISTS complaints (
                     id INT AUTO_INCREMENT PRIMARY KEY, 
                     type VARCHAR(50), description TEXT, 
                     status VARCHAR(20), date VARCHAR(50))''')
                     
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                     email VARCHAR(100) PRIMARY KEY, 
                     password_hash VARCHAR(255), role VARCHAR(20))''')
        
        c.execute("SELECT count(*) FROM faculty")
        if c.fetchone()[0] == 0:
            sql = "INSERT INTO faculty (name, department, subject, cabin) VALUES (%s, %s, %s, %s)"
            faculty_data = [
                ("Dr. Sharma", "CS", "Data Structures", "Cabin 204, Block A"),
                ("Prof. Anjali", "CS", "OOPs & Java", "Cabin 101, Block B"),
            ]
            c.executemany(sql, faculty_data)
            conn.commit()
            print("✅ MySQL Database Initialized for EMAIL!")
            
        conn.close()
    except Exception as e:
        print(f"❌ Database Setup Error: {e}")

init_db()

def get_password_hash(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.post("/register")
async def register(user: UserCreate):
    conn = get_db_connection()
    c = conn.cursor()
    # Check if email exists
    c.execute("SELECT * FROM users WHERE email=%s", (user.email,))
    if c.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = get_password_hash(user.password)
    # Insert new user using email
    c.execute("INSERT INTO users (email, password_hash, role) VALUES (%s, %s, %s)", 
              (user.email, hashed_pw, "student"))
    conn.commit()
    conn.close()
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: UserLogin):
    conn = get_db_connection()
    c = conn.cursor()
    # Fetch user by email
    c.execute("SELECT password_hash FROM users WHERE email=%s", (user.email,))
    row = c.fetchone()
    conn.close()
    
    if not row or not verify_password(user.password, row[0]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {"message": "Login successful", "user": user.email}

def get_ai_response(query: str):
    if profanity.contains_profanity(query):
        return "⚠️ **System Alert:** Your message contains inappropriate language."

    query = query.lower()
    
    if "teach" in query or "faculty" in query:
        conn = get_db_connection()
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
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO complaints (type, description, status, date) VALUES (%s, %s, %s, %s)", 
                  ("General", issue, "Open", str(datetime.now())))
        conn.commit()
        conn.close()
        return f"✅ Complaint Registered. ID #{random.randint(1000,9999)}."

    return "🤖 I am SmartCampus AI. Ask me about Faculty, Mess, or Complaints."

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    return {"reply": get_ai_response(req.message)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)