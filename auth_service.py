# auth_service.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

# Import fungsi dari file database.py milikmu
from database import get_auth_db_conn, fetch_one

app = FastAPI(title="KeepIn Auth Service")

# Konfigurasi untuk verifikasi password yang di-hash (Bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==================== VALIDASI DATA (PYDANTIC) ====================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: str

# ==================== ENDPOINT API ====================
@app.post("/api/auth/login")
def login(data: LoginRequest):
    # 1. PERBAIKAN QUERY: Mengubah password_hash menjadi hashed_password sesuai kolom asli PostgreSQL-mu
    query = "SELECT email, hashed_password AS password, role FROM users WHERE email = %s"
    
    try:
        # Menembak fungsi helper fetch_one bawaan database.py kamu
        user = fetch_one(get_auth_db_conn, query, (data.email,))
    except Exception as e:
        # PERBAIKAN: Mengembalikan HTTP 500 dalam format JSON standar FastAPI agar app.py tidak mengalami JSONDecodeError
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    
    # 2. Cek apakah user ditemukan
    if not user:
        raise HTTPException(status_code=404, detail="Email tidak terdaftar")
    
    # 3. Validasi password yang di-hash
    if not pwd_context.verify(data.password, user['password']):
        raise HTTPException(status_code=401, detail="Kata sandi salah")
        
    # 4. Validasi kesesuaian Role
    if user['role'].lower() != data.role.lower():
        raise HTTPException(status_code=403, detail="Role tidak sesuai untuk akun ini")
        
    # Jika sukses, kembalikan response
    return {
        "status": "success",
        "message": "Login berhasil",
        "token": f"mock-jwt-token-for-{user['role']}-{user['email']}",
        "user": {
            "email": user['email'],
            "role": user['role']
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)