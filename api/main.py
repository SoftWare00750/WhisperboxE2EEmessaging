from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI(title="WhisperBox E2EE Backend")

# Enable CORS so your Vercel frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Vercel URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-Memory Database (Replace with PostgreSQL/MongoDB for production) ---
users = {}          # { username: {"public_key": str, "password": str} }
message_store = []  # List of encrypted message blobs

# --- Schemas ---
class UserRegister(BaseModel):
    username: str
    password: str
    public_key: str

class MessageEnvelope(BaseModel):
    sender: str
    recipient: str
    ciphertext: str
    iv: str
    encrypted_key: str

# --- Endpoints ---

@app.post("/auth/register")
async def register(user: UserRegister):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    users[user.username] = {
        "password": user.password,
        "public_key": user.public_key
    }
    return {"status": "success", "message": "User registered and public key stored"}

@app.get("/users/{username}")
async def get_public_key(username: str):
    """Fetch a recipient's public key to encrypt a message for them."""
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": username, "public_key": users[username]["public_key"]}

@app.post("/messages")
async def send_message(msg: MessageEnvelope):
    """Store an encrypted blob. The server cannot read the 'ciphertext'."""
    if msg.recipient not in users:
        raise HTTPException(status_code=404, detail="Recipient does not exist")
    
    payload = msg.dict()
    payload["timestamp"] = time.time()
    message_store.append(payload)
    return {"status": "sent"}

@app.get("/messages/{username}")
async def get_messages(username: str):
    """Retrieve encrypted blobs for a specific user."""
    user_msgs = [m for m in message_store if m["recipient"] == username]
    return user_msgs

@app.get("/")
async def health_check():
    return {"status": "online", "app": "WhisperBox E2EE Relay"}