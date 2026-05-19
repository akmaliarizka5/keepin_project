# loker_service.py
from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

from database import get_loker_db_conn

app = FastAPI(title="KeepIn Loker Service")

@app.get("/api/loker")
def get_lockers_by_location(lokasi: str):
    # PERBAIKAN QUERY: Menyesuaikan nama kolom baru (tipe_loker, harga_per_jam, status='READY')
    query = """
        SELECT id_loker, id_usaha, tipe_loker, harga_per_jam, lokasi, status 
        FROM loker 
        WHERE lokasi = %s AND status = 'READY'
        ORDER BY id_loker ASC
    """
    try:
        conn = get_loker_db_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (lokasi,))
        lockers = cur.fetchall()
        cur.close()
        conn.close()
        return {"status": "success", "data": lockers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)