import csv
import random
from datetime import datetime, timedelta

# Reglas:
# Generar registros para años futuros (2026 y 2027 por defecto).
# Mismas dimensiones que el dataset original:
# 30 productos, 5 categorías, 50 clientes, 5 zonas, 8 vendedores, 3 bodegas.

YEARS = [2026, 2027]
num_records_per_year = 3000

categories = [
    {"name": "Alimentos", "base_price": 5.0, "demand_weight": 0.4},
    {"name": "Bebidas", "base_price": 2.0, "demand_weight": 0.3},
    {"name": "Limpieza", "base_price": 8.0, "demand_weight": 0.15},
    {"name": "Cuidado Personal", "base_price": 12.0, "demand_weight": 0.1},
    {"name": "Electrodomésticos", "base_price": 150.0, "demand_weight": 0.05}
]

products = []
product_counter = 1
for cat in categories:
    num_prods = 6  # 5 cat * 6 prods = 30
    for i in range(num_prods):
        price = round(cat["base_price"] * random.uniform(0.5, 1.5), 2)
        popularity = random.uniform(0.5, 2.0)
        products.append({
            "code": f"PROD-{product_counter:03d}",
            "name": f"Producto {cat['name']} {i+1}",
            "category": cat["name"],
            "unit_price": price,
            "weight": cat["demand_weight"] * popularity
        })
        product_counter += 1

customers = [{"code": f"CUST-{i:03d}", "name": f"Cliente {i}"} for i in range(1, 51)]

zones = [
    {"name": "Guayaquil", "weight": 0.4},
    {"name": "Quito", "weight": 0.3},
    {"name": "Cuenca", "weight": 0.15},
    {"name": "Manta", "weight": 0.1},
    {"name": "Ambato", "weight": 0.05}
]

salesmen = [f"Vendedor {i}" for i in range(1, 9)]
warehouses = ["Bodega Principal", "Bodega Norte", "Bodega Sur"]

records = []
sale_counter = 1

for year in YEARS:
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    date_range_days = (end_date - start_date).days

    for _ in range(num_records_per_year):
        # Generar fecha. Nov y Dic tienen mayor probabilidad
        while True:
            random_days = random.randint(0, date_range_days)
            sale_date = start_date + timedelta(days=random_days)
            month = sale_date.month
            day_of_week = sale_date.weekday()  # 0 = Lunes, 6 = Domingo

            # Estacionalidad: Aumentar probabilidad si es Nov o Dic
            prob = random.random()
            if month in [11, 12]:
                if prob < 0.8:  # Mayor probabilidad de aceptar esta fecha
                    break
            else:
                if prob < 0.4:
                    break

        # Zona
        zone = random.choices(zones, weights=[z["weight"] for z in zones], k=1)[0]["name"]

        # Producto
        prod = random.choices(products, weights=[p["weight"] for p in products], k=1)[0]

        customer = random.choice(customers)
        salesman = random.choice(salesmen)
        warehouse = random.choice(warehouses)

        # Cantidad influenciada por día de la semana y mes
        base_qty = random.randint(1, 20)
        if day_of_week >= 4:  # Viernes, Sab, Dom
            base_qty = int(base_qty * random.uniform(1.2, 1.5))
        if month in [11, 12]:
            base_qty = int(base_qty * random.uniform(1.3, 1.8))

        quantity = base_qty

        # Descuento
        discount_percentage = random.choice([0, 0, 0, 5, 10, 15, 20])

        # Total sales
        total_sales = round(quantity * prod["unit_price"] * (1 - discount_percentage / 100), 2)

        records.append({
            "sale_id": f"SALE-{sale_counter:05d}",
            "sale_date": sale_date.strftime("%Y-%m-%d"),
            "year_number": sale_date.year,
            "month_number": sale_date.month,
            "day_number": sale_date.day,
            "day_of_week": day_of_week + 1,  # 1=Lunes, 7=Domingo
            "customer_code": customer["code"],
            "customer_name": customer["name"],
            "product_code": prod["code"],
            "product_name": prod["name"],
            "category_name": prod["category"],
            "zone_name": zone,
            "salesman_name": salesman,
            "warehouse_name": warehouse,
            "quantity": quantity,
            "unit_price": prod["unit_price"],
            "discount_percentage": discount_percentage,
            "total_sales": total_sales
        })

        sale_counter += 1

# Sort records by date just in case
records.sort(key=lambda x: x["sale_date"])

filename = "ventas_futuras_2026_2027.csv"
fieldnames = [
    "sale_id", "sale_date", "year_number", "month_number", "day_number", "day_of_week",
    "customer_code", "customer_name", "product_code", "product_name", "category_name",
    "zone_name", "salesman_name", "warehouse_name", "quantity", "unit_price",
    "discount_percentage", "total_sales"
]

with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print(f"Archivo {filename} generado exitosamente con {len(records)} registros.")
