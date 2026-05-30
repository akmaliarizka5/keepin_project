# booking_service.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor

from database import get_booking_db_conn

app = FastAPI(title="KeepIn Booking Service")

# --- SCHEMA REQUEST VALIDATION ---
class CreateBookingRequest(BaseModel):
    id_user: int
    id_loker: str
    nama_tempat: str
    durasi_sewa: int
    total_biaya: float
    metode_bayar: str = "QRIS"

# --- API ENDPOINTS ---

@app.post("/api/booking/create", status_code=status.HTTP_201_CREATED)
def create_booking(data: CreateBookingRequest):
    insert_query = """
        INSERT INTO booking (id_user, id_loker, nama_tempat, durasi_sewa, satuan_durasi, total_biaya, status_booking, metode_bayar)
        VALUES (%s, %s, %s, %s, 'JAM', %s, 'PENDING', %s)
        RETURNING id_booking, status_booking;
    """
    try:
        conn = get_booking_db_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(insert_query, (data.id_user, data.id_loker, data.nama_tempat, data.durasi_sewa, data.total_biaya, data.metode_bayar))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # [NEXT DEVELOPMENT COMMENT]:
        # Setelah booking sukses tersimpan dengan status 'PENDING', service ini idealnya 
        # memicu hit ke `payment_service` untuk men-generate kode QRIS / Payment Link (Midtrans/Xendit)
        
        return {
            "status": "success",
            "message": "Pemesanan loker berhasil dibuat!",
            "booking_id": result["id_booking"],
            "status_booking": result["status_booking"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses booking: {str(e)}")


@app.get("/api/booking/user/{id_user}")
def get_user_bookings(id_user: int):
    """Endpoint untuk mengambil semua riwayat booking milik penyewa tertentu"""
    query = "SELECT * FROM booking WHERE id_user = %s ORDER BY id_booking DESC"
    try:
        conn = get_booking_db_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (id_user,))
        bookings = cur.fetchall()
        cur.close()
        conn.close()
        return {"status": "success", "data": bookings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Dijalankan di port 8001 agar tidak bentrok dengan Auth Service
    uvicorn.run(app, host="127.0.0.1", port=8001)
