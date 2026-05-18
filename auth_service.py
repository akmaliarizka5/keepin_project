# auth_service.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

# Import fungsi dari file database.py milikmu
from database import get_auth_db_conn, fetch_one, execute_query # Pastikan execute_query ada di database.py

app = FastAPI(title="KeepIn Auth Service")

# Konfigurasi untuk verifikasi password yang di-hash (Bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==================== VALIDASI DATA (PYDANTIC) ====================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: str

class RegisterRequest(BaseModel):
    nama_lengkap: str
    email: EmailStr
    no_telp: str
    password: str
    role: str # 'Mitra', 'Penyewa', atau 'Admin'

# ==================== ENDPOINT API ====================

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest):
    # 1. Cek apakah email sudah terdaftar
    check_query = "SELECT email FROM users WHERE email = %s"
    try:
        existing_user = fetch_one(get_auth_db_conn, check_query, (data.email,))
        if existing_user:
            raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
        
    # 2. Hash Password demi keamanan data
    hashed_pwd = pwd_context.hash(data.password)
    
    # 3. Simpan user baru ke database
    # Menyesuaikan penamaan kolom tabel user asli (nama_lengkap, email, no_telp, hashed_password, role)
    insert_query = """
        INSERT INTO users (nama_lengkap, email, no_telp, hashed_password, role)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        # Menggunakan koneksi database mu untuk eksekusi insert
        conn = get_auth_db_conn()
        cur = conn.cursor()
        cur.execute(insert_query, (data.nama_lengkap, data.email, data.no_telp, hashed_pwd, data.role))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan data user: {str(e)}")
        
    # [NEXT DEVELOPMENT COMMENT]:
    # Setelah simpan di auth_db sukses, memicu message broker ke `profile_service` / `usaha_service`
    # jika role-nya 'Mitra' agar otomatis menyiapkan struktur dashboard mitra miliknya.

    return {"status": "success", "message": f"Registrasi sebagai {data.role} berhasil!"}


@app.post("/api/auth/login")
def login(data: LoginRequest):
    query = "SELECT email, hashed_password AS password, role FROM users WHERE email = %s"
    try:
        user = fetch_one(get_auth_db_conn, query, (data.email,))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    
    if not user:
        raise HTTPException(status_code=404, detail="Email tidak terdaftar")
    
    if not pwd_context.verify(data.password, user['password']):
        raise HTTPException(status_code=401, detail="Kata sandi salah")
        
    if user['role'].lower() != data.role.lower():
        raise HTTPException(status_code=403, detail="Role tidak sesuai untuk akun ini")
        
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