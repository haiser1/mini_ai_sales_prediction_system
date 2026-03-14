"""
Seeder script to import sales_data.csv into the PostgreSQL database.
Run: ./venv/bin/python scripts/seed_sales_data.py
"""
import asyncio
import csv
import os
import sys

# Add backend directory to path so we can import app modules
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BACKEND_DIR)

from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal
from app.models.sales_data import SalesData


CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "sales_data.csv",
)


async def seed_sales_data():
    async with AsyncSessionLocal() as session:
        # Check if data is already seeded
        result = await session.execute(select(func.count(SalesData.id)))
        count = result.scalar() or 0
        if count > 0:
            print(f"⚠️  Database sudah berisi {count} data penjualan. Skip seeding.")
            return

        # Read CSV
        if not os.path.exists(CSV_PATH):
            print(f"❌ File CSV tidak ditemukan: {CSV_PATH}")
            return

        with open(CSV_PATH, "r") as f:
            reader = csv.DictReader(f)
            rows = []
            for row in reader:
                rows.append(
                    SalesData(
                        product_id=row["product_id"],
                        product_name=row["product_name"],
                        jumlah_penjualan=int(row["jumlah_penjualan"]),
                        harga=float(row["harga"]),
                        diskon=int(row["diskon"]),
                        status=row["status"],
                    )
                )

        session.add_all(rows)
        await session.commit()
        print(f"✅ Berhasil seed {len(rows)} data penjualan ke database!")


if __name__ == "__main__":
    asyncio.run(seed_sales_data())
