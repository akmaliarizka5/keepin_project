# loker_service.py
from fastapi import FastAPI, HTTPException, Query
from psycopg2.extras import RealDictCursor

from database import get_loker_db_conn

app = FastAPI(title="KeepIn Loker Service")

DEFAULT_LATITUDE = -7.7956
DEFAULT_LONGITUDE = 110.3695


def enrich_locker(row, index):
    lokasi = row.get("lokasi") or "Lokasi belum tersedia"
    nama_area = lokasi.split(",")[0].strip()
    jarak_km = round(0.35 + (index * 0.18), 2)
    latitude = row.get("latitude") if row.get("latitude") is not None else DEFAULT_LATITUDE + (index * 0.0031)
    longitude = row.get("longitude") if row.get("longitude") is not None else DEFAULT_LONGITUDE + (index * 0.0038)

    return {
        **row,
        "nama_tempat": f"Loker {nama_area}",
        "alamat_ringkas": lokasi,
        "jarak_km": jarak_km,
        "estimasi_menit": max(3, int(jarak_km * 12)),
        "latitude": float(latitude),
        "longitude": float(longitude),
        "status_label": "Tersedia" if row.get("status") == "READY" else row.get("status"),
    }


@app.get("/api/loker")
def get_lockers(
    lokasi: str | None = None,
    search: str | None = None,
    sort_by: str = Query("jarak", pattern="^(jarak|harga_asc|harga_desc|ukuran)$"),
    ukuran: str | None = None,
):
    query = """
        SELECT id_loker, id_usaha, tipe_loker, harga_per_jam, lokasi, status, latitude, longitude
        FROM loker
        WHERE status = 'READY'
    """
    params = []

    if lokasi:
        query += " AND lokasi ILIKE %s"
        params.append(f"%{lokasi}%")

    if search:
        search_terms = [term.strip() for term in search.replace(",", " ").split() if term.strip()]
        for term in search_terms:
            query += " AND (lokasi ILIKE %s OR tipe_loker ILIKE %s OR id_loker ILIKE %s)"
            params.extend([f"%{term}%", f"%{term}%", f"%{term}%"])

    if ukuran and ukuran.lower() != "semua":
        query += " AND tipe_loker ILIKE %s"
        params.append(f"%{ukuran}%")

    if sort_by == "harga_asc":
        query += " ORDER BY harga_per_jam ASC, id_loker ASC"
    elif sort_by == "harga_desc":
        query += " ORDER BY harga_per_jam DESC, id_loker ASC"
    elif sort_by == "ukuran":
        query += " ORDER BY tipe_loker ASC, id_loker ASC"
    else:
        query += " ORDER BY lokasi ASC, id_loker ASC"

    try:
        conn = get_loker_db_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, tuple(params))
        lockers = [enrich_locker(dict(row), idx) for idx, row in enumerate(cur.fetchall())]
        cur.close()
        conn.close()
        return {
            "status": "success",
            "total": len(lockers),
            "filters": {
                "lokasi": lokasi,
                "search": search,
                "sort_by": sort_by,
                "ukuran": ukuran,
            },
            "data": lockers,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
