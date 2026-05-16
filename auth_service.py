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
    # 1. Query mencari user berdasarkan email menggunakan helper milikmu
    # Sesuaikan nama kolom ('email', 'password', 'role') dengan yang ada di tabel database-mu
    query = "SELECT email, password, role FROM users WHERE email = %s"
    
    try:
        # Menembak fungsi helper fetch_one bawaan database.py kamu
        user = fetch_one(get_auth_db_conn, query, (data.email,))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal terhubung ke database: {str(e)}")
    
    # 2. Cek apakah user ditemukan
    if not user:
        raise HTTPException(status_code=404, detail="Email tidak terdaftar")
    
    # 3. Validasi password yang di-hash
    # Catatan: Jika password di DB kamu masih teks biasa (plain text), ganti bagian ini dengan:
    # if user['password'] != data.password:
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