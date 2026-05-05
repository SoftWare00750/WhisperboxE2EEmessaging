from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import time

app = FastAPI(title="WhisperBox E2EE Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-Memory Database ---
users = {}          # { username: {"public_key": str, "password": str} }
message_store = []  # List of encrypted message blobs
msg_id_counter = [0]

# --- Schemas ---
class UserRegister(BaseModel):
    username: str
    password: str
    public_key: str

class UserLogin(BaseModel):
    username: str
    password: str

class MessageEnvelope(BaseModel):
    sender: Optional[str] = None
    recipient: str
    ciphertext: str
    iv: str
    encrypted_key: str

# --- Endpoints ---

@app.get("/")
async def health_check():
    return {"status": "online", "app": "WhisperBox E2EE Relay"}

@app.post("/auth/register")
async def register(user: UserRegister):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already taken")
    users[user.username] = {
        "password": user.password,
        "public_key": user.public_key,
    }
    return {"status": "success", "message": "User registered and public key stored"}

@app.post("/auth/login")
async def login(credentials: UserLogin):
    user = users.get(credentials.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # Return a simple token (username acts as token for this demo)
    return {
        "status": "success",
        "access_token": credentials.username,
        "username": credentials.username,
    }

@app.get("/users/{username}")
async def get_public_key(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": username, "public_key": users[username]["public_key"]}

@app.post("/messages")
async def send_message(msg: MessageEnvelope, sender: Optional[str] = None):
    if msg.recipient not in users:
        raise HTTPException(status_code=404, detail="Recipient does not exist")
    msg_id_counter[0] += 1
    payload = {
        "id": msg_id_counter[0],
        "sender": msg.sender or sender or "unknown",
        "recipient": msg.recipient,
        "ciphertext": msg.ciphertext,
        "iv": msg.iv,
        "encrypted_key": msg.encrypted_key,
        "timestamp": time.time(),
    }
    message_store.append(payload)
    return {"status": "sent", "id": payload["id"]}

@app.get("/messages/{username}")
async def get_messages(username: str):
    user_msgs = [m for m in message_store if m["recipient"] == username or m["sender"] == username]
    return user_msgs
