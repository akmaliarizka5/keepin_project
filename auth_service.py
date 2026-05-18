import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
import jwt  # Menggunakan PyJWT (pip install pyjwt)
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIG DATABASE ---
DATABASE_URL = "sqlite:///./auth_db.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODEL DATABASE (Granularitas Level Kolom) ---
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nama_lengkap = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    no_telp = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False) # Nilai wajib: 'Penyewa' atau 'Mitra'

Base.metadata.create_all(bind=engine)

# --- CONFIG KEAMANAN & JWT ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

app = FastAPI(title="Keepin Auth Microservice")

# --- SCHEMA REQUEST (Validasi Input) ---
class RegisterSchema(BaseModel):
    nama_lengkap: str
    email: EmailStr
    no_telp: str
    password: str
    role: str # 'Penyewa' atau 'Mitra'

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

# --- UTILITY FUNCTIONS ---
def create_access_token(data: dict, expires_delta: datetime.timedelta):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


# --- API ENDPOINTS ---

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(user_data: RegisterSchema):
    db = SessionLocal()
    
    # Check jika email sudah terdaftar
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Email sudah terdaftar!")
    
    if user_data.role not in ["Penyewa", "Mitra"]:
        raise HTTPException(status_code=400, detail="Role tidak valid. Harus 'Penyewa' atau 'Mitra'")
        
    # Hashing Password
    hashed_pwd = pwd_context.hash(user_data.password)
    
    # Simpan ke auth_db
    new_user = UserModel(
        nama_lengkap=user_data.nama_lengkap,
        email=user_data.email,
        no_telp=user_data.no_telp,
        hashed_password=hashed_pwd,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    
    # [NEXT DEVELOPMENT COMMENT]: 
    # Setelah user berhasil masuk ke auth_db, idealnya service ini memicu event/message broker (misal: RabbitMQ/Kafka)
    # untuk memberitahu `profile_service` agar membuat row profile kosong atau sinkronisasi awal data profile
    # berdasarkan user_id yang baru terbentuk.
    
    db.close()
    return {"message": f"Registrasi sebagai {user_data.role} berhasil!"}


@app.post("/api/auth/login")
def login(user_data: LoginSchema):
    db = SessionLocal()
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    db.close()
    
    if not user or not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email atau kata sandi salah")
    
    # Membuat JWT Token bawaan data User Identity
    token_expiry = datetime.timedelta(hours=2)
    access_token = create_access_token(
        data={
            "user_id": user.id, 
            "email": user.email, 
            "role": user.role,
            "nama": user.nama_lengkap
        }, 
        expires_delta=token_expiry
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "role": user.role, 
        "nama": user.nama_lengkap
    }