from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor

from database import get_usaha_db_conn

app = FastAPI(title="KeepIn Usaha Service")


class CreateUsahaRequest(BaseModel):
    id_owner: int
    nama_usaha: str
    alamat: str
    phone: str = "-"
    jumlah_slot: int = 1


@app.post("/api/usaha/create", status_code=status.HTTP_201_CREATED)
def create_usaha(data: CreateUsahaRequest):
    query = """
        INSERT INTO usaha (id_owner, nama_usaha, alamat, phone, jumlah_slot, status_verifikasi)
        VALUES (%s, %s, %s, %s, %s, 'MENUNGGU')
        RETURNING *;
    """
    try:
        conn = get_usaha_db_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (data.id_owner, data.nama_usaha, data.alamat, data.phone, data.jumlah_slot))
        usaha = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": "Usaha berhasil diajukan", "data": usaha}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan usaha: {str(e)}")


@app.get("/api/usaha/owner/{id_owner}")
def get_usaha_by_owner(id_owner: int):
    query = "SELECT * FROM usaha WHERE id_owner = %s ORDER BY id_usaha DESC"
    try:
        conn = get_usaha_db_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (id_owner,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {"status": "success", "data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")


@app.get("/api/usaha/owner/{id_owner}/summary")
def get_usaha_summary(id_owner: int):
    query = """
        SELECT
            COUNT(*) AS total_usaha,
            COALESCE(SUM(jumlah_slot), 0) AS total_loker,
            COUNT(*) FILTER (WHERE status_verifikasi = 'TERVERIFIKASI') AS usaha_aktif
        FROM usaha
        WHERE id_owner = %s
    """
    try:
        conn = get_usaha_db_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (id_owner,))
        summary = cur.fetchone()
        cur.close()
        conn.close()
        return {"status": "success", "data": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8003)
