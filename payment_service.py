from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor

from database import get_payment_db_conn

app = FastAPI(title="KeepIn Payment Service")


class CreatePaymentRequest(BaseModel):
    booking_id: int
    amount: float
    method: str = "QRIS"


class UpdatePaymentStatusRequest(BaseModel):
    status: str


@app.post("/api/payment/create", status_code=status.HTTP_201_CREATED)
def create_payment(data: CreatePaymentRequest):
    query = """
        INSERT INTO payments (booking_id, amount, method, status, reference)
        VALUES (%s, %s, %s, 'PENDING', %s)
        RETURNING id_payment, booking_id, amount, method, status, reference, created_at;
    """
    reference = f"KEEPIN-PAY-{data.booking_id:05d}"
    try:
        conn = get_payment_db_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (data.booking_id, data.amount, data.method, reference))
        payment = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {
            "status": "success",
            "message": "Payment link berhasil dibuat",
            "data": payment,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal membuat payment: {str(e)}")


@app.get("/api/payment/booking/{booking_id}")
def get_payment_by_booking(booking_id: int):
    query = "SELECT * FROM payments WHERE booking_id = %s ORDER BY id_payment DESC LIMIT 1"
    try:
        conn = get_payment_db_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (booking_id,))
        payment = cur.fetchone()
        cur.close()
        conn.close()
        return {"status": "success", "data": payment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")


@app.patch("/api/payment/{payment_id}/status")
def update_payment_status(payment_id: int, data: UpdatePaymentStatusRequest):
    query = """
        UPDATE payments
        SET status = %s
        WHERE id_payment = %s
        RETURNING id_payment, booking_id, amount, method, status, reference, created_at;
    """
    try:
        conn = get_payment_db_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (data.status.upper(), payment_id))
        payment = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment tidak ditemukan")
        return {"status": "success", "data": payment}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal update payment: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8004)
