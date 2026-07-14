import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def parse_results(csv_path):
    """Lee el CSV de resultados y devuelve una lista de diccionarios normalizados."""
    records = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.strptime(row["sale_date"], "%Y-%m-%d")
                real = float(row["real_sales"])
                predicted = float(row["predicted_sales"])
                diff = float(row["difference"])
                pct_error_str = row["percentage_error"].replace("%", "")
                pct_error = float(pct_error_str)
                records.append({
                    "date": date,
                    "month": date.month,
                    "month_name": date.strftime("%B").capitalize(),
                    "product_name": row["product_name"].strip(),
                    "category_name": row["category_name"].strip(),
                    "zone_name": row["zone_name"].strip(),
                    "real_sales": real,
                    "predicted_sales": predicted,
                    "difference": diff,
                    "percentage_error": pct_error,
                })
            except Exception:
                continue
    return records


def month_name_es(month_number):
    nombres = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
    }
    return nombres.get(month_number, "")


def aggregate_by_month(records):
    """Agrega ventas reales y predichas por mes."""
    months = defaultdict(lambda: {"real_total": 0.0, "predicted_total": 0.0, "errors": []})
    for r in records:
        m = r["month"]
        months[m]["real_total"] += r["real_sales"]
        months[m]["predicted_total"] += r["predicted_sales"]
        months[m]["errors"].append(r["percentage_error"])

    sorted_months = []
    for m in sorted(months.keys()):
        entry = months[m]
        entry["month_name"] = month_name_es(m)
        entry["avg_error"] = sum(entry["errors"]) / len(entry["errors"])
        sorted_months.append((m, entry))
    return sorted_months


def aggregate_by_category(records):
    """Agrega ventas reales y predichas por categoría."""
    cats = defaultdict(lambda: {"real_total": 0.0, "predicted_total": 0.0, "errors": []})
    for r in records:
        c = r["category_name"]
        cats[c]["real_total"] += r["real_sales"]
        cats[c]["predicted_total"] += r["predicted_sales"]
        cats[c]["errors"].append(r["percentage_error"])

    result = []
    for c, entry in sorted(cats.items()):
        entry["avg_error"] = sum(entry["errors"]) / len(entry["errors"])
        result.append((c, entry))
    return result


def aggregate_by_zone(records):
    """Agrega ventas reales y predichas por zona."""
    zones = defaultdict(lambda: {"real_total": 0.0, "predicted_total": 0.0, "errors": []})
    for r in records:
        z = r["zone_name"]
        zones[z]["real_total"] += r["real_sales"]
        zones[z]["predicted_total"] += r["predicted_sales"]
        zones[z]["errors"].append(r["percentage_error"])

    result = []
    for z, entry in sorted(zones.items()):
        entry["avg_error"] = sum(entry["errors"]) / len(entry["errors"])
        result.append((z, entry))
    return result


def top_products_by_predicted(records, n=10):
    """Top N productos con mayor venta estimada (suma de predicciones)."""
    products = defaultdict(lambda: {"predicted_total": 0.0, "real_total": 0.0, "category": ""})
    for r in records:
        p = r["product_name"]
        products[p]["predicted_total"] += r["predicted_sales"]
        products[p]["real_total"] += r["real_sales"]
        products[p]["category"] = r["category_name"]

    sorted_products = sorted(products.items(), key=lambda x: x[1]["predicted_total"], reverse=True)
    return sorted_products[:n]


def top_products_by_difference(records, n=10):
    """Top N productos con mayor diferencia absoluta entre real y predicho."""
    products = defaultdict(lambda: {"diff_total": 0.0, "real_total": 0.0, "predicted_total": 0.0, "category": ""})
    for r in records:
        p = r["product_name"]
        products[p]["diff_total"] += abs(r["difference"])
        products[p]["real_total"] += r["real_sales"]
        products[p]["predicted_total"] += r["predicted_sales"]
        products[p]["category"] = r["category_name"]

    sorted_products = sorted(products.items(), key=lambda x: x[1]["diff_total"], reverse=True)
    return sorted_products[:n]


def overall_metrics(records):
    total_real = sum(r["real_sales"] for r in records)
    total_predicted = sum(r["predicted_sales"] for r in records)
    total_diff = sum(abs(r["difference"]) for r in records)
    avg_error = sum(r["percentage_error"] for r in records) / len(records)
    mae = sum(abs(r["real_sales"] - r["predicted_sales"]) for r in records) / len(records)
    rmse = (sum((r["real_sales"] - r["predicted_sales"]) ** 2 for r in records) / len(records)) ** 0.5

    mean_real = total_real / len(records)
    ss_tot = sum((r["real_sales"] - mean_real) ** 2 for r in records)
    ss_res = sum((r["real_sales"] - r["predicted_sales"]) ** 2 for r in records)
    r2 = 1 - (ss_res / ss_tot) if ss_tot else 0

    return {
        "total_records": len(records),
        "total_real": total_real,
        "total_predicted": total_predicted,
        "total_difference": total_diff,
        "avg_error": avg_error,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
    }


def build_top_predicted_rows(top_predicted):
    rows = ""
    for idx, (name, data) in enumerate(top_predicted, 1):
        rows += f"""
        <tr>
            <td>{idx}</td>
            <td>{name}</td>
            <td>{data['category']}</td>
            <td>${data['predicted_total']:,.2f}</td>
            <td>${data['real_total']:,.2f}</td>
        </tr>
        """
    return rows


def build_top_difference_rows(top_diff):
    rows = ""
    for idx, (name, data) in enumerate(top_diff, 1):
        diff_pct = (data["diff_total"] / data["real_total"] * 100) if data["real_total"] > 0 else 0
        rows += f"""
        <tr>
            <td>{idx}</td>
            <td>{name}</td>
            <td>{data['category']}</td>
            <td>${data['diff_total']:,.2f}</td>
            <td>{diff_pct:.2f}%</td>
            <td>${data['real_total']:,.2f}</td>
            <td>${data['predicted_total']:,.2f}</td>
        </tr>
        """
    return rows


def build_conclusions(metrics, monthly_data, category_data, zone_data, top_predicted, top_diff):
    """Genera conclusiones automáticas basadas en los datos."""
    best_month = min(monthly_data, key=lambda x: x[1]["avg_error"])
    worst_month = max(monthly_data, key=lambda x: x[1]["avg_error"])
    highest_real_month = max(monthly_data, key=lambda x: x[1]["real_total"])
    lowest_real_month = min(monthly_data, key=lambda x: x[1]["real_total"])

    best_cat = min(category_data, key=lambda x: x[1]["avg_error"])
    worst_cat = max(category_data, key=lambda x: x[1]["avg_error"])
    highest_cat = max(category_data, key=lambda x: x[1]["predicted_total"])

    best_zone = min(zone_data, key=lambda x: x[1]["avg_error"])
    worst_zone = max(zone_data, key=lambda x: x[1]["avg_error"])
    highest_zone = max(zone_data, key=lambda x: x[1]["predicted_total"])

    bias_text = "sobrestima" if metrics["total_predicted"] > metrics["total_real"] else "subestima"
    bias_pct = abs((metrics["total_predicted"] - metrics["total_real"]) / metrics["total_real"] * 100)

    # Detectar categorías/zonas con alto error (>50%) como riesgos.
    risk_cats = [c for c in category_data if c[1]["avg_error"] > 50]
    risk_zones = [z for z in zone_data if z[1]["avg_error"] > 50]

    opportunities = [
        f"<strong>Mayor potencial de ventas:</strong> {highest_cat[0]} con ${highest_cat[1]['predicted_total']:,.2f} estimados; priorizar inventario y promociones.",
        f"<strong>Zona más valiosa:</strong> {highest_zone[0]} (${highest_zone[1]['predicted_total']:,.2f} predichas), candidata a campañas focalizadas.",
        f"<strong>Producto más prometedor:</strong> {top_predicted[0][0]} con ${top_predicted[0][1]['predicted_total']:,.2f} en ventas estimadas.",
        f"<strong>Mejor mes predicho:</strong> {best_month[1]['month_name']} (error {best_month[1]['avg_error']:.2f}%), aprovechar para lanzamientos.",
    ]

    risks = [
        f"<strong>Diferencia total:</strong> el modelo {bias_text} las ventas en un {bias_pct:.2f}%.",
        f"<strong>Peor mes predicho:</strong> {worst_month[1]['month_name']} con error promedio de {worst_month[1]['avg_error']:.2f}%.",
        f"<strong>Categoría menos precisa:</strong> {worst_cat[0]} (error {worst_cat[1]['avg_error']:.2f}%).",
        f"<strong>Zona menos precisa:</strong> {worst_zone[0]} (error {worst_zone[1]['avg_error']:.2f}%).",
    ]

    if risk_cats:
        risk_cat_names = ", ".join([c[0] for c in risk_cats])
        risks.append(f"<strong>Categorías con alto riesgo de error:</strong> {risk_cat_names} requieren revisión de variables o más datos.")
    if risk_zones:
        risk_zone_names = ", ".join([z[0] for z in risk_zones])
        risks.append(f"<strong>Zonas con alto riesgo de error:</strong> {risk_zone_names}; validar comportamiento regional.")

    risk_top = top_diff[0]
    risks.append(f"<strong>Producto con mayor desviación:</strong> {risk_top[0]} con ${risk_top[1]['diff_total']:,.2f} de diferencia acumulada.")

    recommendations = [
        "Revisar el modelo para categorías y zonas con error >50%; podría necesitarse ingeniería de características o más registros históricos.",
        "Ajustar inventarios y compras en función de las predicciones por categoría, especialmente en los productos top 10 estimados.",
        "Diseñar promociones locales en las zonas con mayores ventas predichas (Guayaquil y Quito) para maximizar el retorno.",
        "Investigar los productos con mayor diferencia absoluta; pueden indicar eventos puntuales, datos atípicos o limitaciones del modelo.",
        "Usar el dashboard mensual para calibrar metas de ventas y alertas tempranas cuando las predicciones se desvíen del real.",
    ]

    return opportunities, risks, recommendations


def generate_html(records, output_path):
    monthly_data = aggregate_by_month(records)
    category_data = aggregate_by_category(records)
    zone_data = aggregate_by_zone(records)
    top_predicted = top_products_by_predicted(records)
    top_diff = top_products_by_difference(records)
    metrics = overall_metrics(records)

    months = [m[1]["month_name"] for m in monthly_data]
    real_monthly = [round(m[1]["real_total"], 2) for m in monthly_data]
    predicted_monthly = [round(m[1]["predicted_total"], 2) for m in monthly_data]
    error_monthly = [round(m[1]["avg_error"], 2) for m in monthly_data]

    categories = [c[0] for c in category_data]
    real_category = [round(c[1]["real_total"], 2) for c in category_data]
    predicted_category = [round(c[1]["predicted_total"], 2) for c in category_data]
    error_category = [round(c[1]["avg_error"], 2) for c in category_data]

    zones = [z[0] for z in zone_data]
    real_zone = [round(z[1]["real_total"], 2) for z in zone_data]
    predicted_zone = [round(z[1]["predicted_total"], 2) for z in zone_data]
    error_zone = [round(z[1]["avg_error"], 2) for z in zone_data]

    top_predicted_labels = [p[0] for p in top_predicted]
    top_predicted_values = [round(p[1]["predicted_total"], 2) for p in top_predicted]

    top_diff_labels = [p[0] for p in top_diff]
    top_diff_values = [round(p[1]["diff_total"], 2) for p in top_diff]

    top_predicted_rows = build_top_predicted_rows(top_predicted)
    top_diff_rows = build_top_difference_rows(top_diff)
    opportunities, risks, recommendations = build_conclusions(metrics, monthly_data, category_data, zone_data, top_predicted, top_diff)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Predicción de Ventas</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --primary: #2563eb;
            --secondary: #7c3aed;
            --success: #16a34a;
            --danger: #dc2626;
            --warning: #ca8a04;
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #1e293b;
            --muted: #64748b;
            --border: #e2e8f0;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}
        header {{
            text-align: center;
            padding: 2rem 0;
            border-bottom: 4px solid var(--primary);
            margin-bottom: 2rem;
        }}
        h1 {{ margin: 0; font-size: 2.2rem; color: var(--primary); }}
        .subtitle {{ color: var(--muted); margin-top: 0.5rem; font-size: 1.1rem; }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .card {{
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .card:hover {{ transform: translateY(-2px); }}
        .card h3 {{
            margin: 0 0 0.75rem 0;
            font-size: 0.85rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .card .value {{
            font-size: 1.7rem;
            font-weight: 700;
            color: var(--text);
        }}
        .card .value.positive {{ color: var(--success); }}
        .card .value.negative {{ color: var(--danger); }}
        .card .value.warning {{ color: var(--warning); }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .chart-container {{
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}
        .chart-container.full-width {{
            grid-column: 1 / -1;
        }}
        .chart-title {{
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--primary);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--card);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}
        th, td {{ padding: 0.875rem 1rem; text-align: right; }}
        th {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.8rem;
        }}
        td {{ border-bottom: 1px solid var(--border); }}
        tr:hover {{ background: #f1f5f9; }}
        td:first-child, th:first-child {{ text-align: left; }}
        .insights {{
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}
        .insights h2 {{ color: var(--primary); margin-top: 0; }}
        .insights h3 {{ color: var(--secondary); margin-top: 1.5rem; }}
        .insights ul {{ padding-left: 1.25rem; }}
        .insights li {{ margin-bottom: 0.75rem; }}
        footer {{
            text-align: center;
            color: var(--muted);
            padding: 2rem 0;
            font-size: 0.875rem;
        }}
        @media (max-width: 768px) {{
            .chart-grid {{ grid-template-columns: 1fr; }}
            .container {{ padding: 1rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Dashboard de Predicción de Ventas</h1>
            <div class="subtitle">Ventas reales vs. predichas · Análisis por mes, categoría y zona</div>
        </header>

        <div class="kpi-grid">
            <div class="card">
                <h3>Registros Analizados</h3>
                <div class="value">{metrics['total_records']:,}</div>
            </div>
            <div class="card">
                <h3>Ventas Reales Totales</h3>
                <div class="value">${metrics['total_real']:,.2f}</div>
            </div>
            <div class="card">
                <h3>Ventas Predichas Totales</h3>
                <div class="value">${metrics['total_predicted']:,.2f}</div>
            </div>
            <div class="card">
                <h3>Diferencia Total</h3>
                <div class="value {'negative' if metrics['total_predicted'] > metrics['total_real'] else 'positive'}">${abs(metrics['total_predicted'] - metrics['total_real']):,.2f}</div>
            </div>
            <div class="card">
                <h3>Error Porcentual Promedio</h3>
                <div class="value {'positive' if metrics['avg_error'] < 30 else 'warning' if metrics['avg_error'] < 50 else 'negative'}">{metrics['avg_error']:.2f}%</div>
            </div>
            <div class="card">
                <h3>R² del Modelo</h3>
                <div class="value {'positive' if metrics['r2'] > 0.7 else 'warning' if metrics['r2'] > 0.4 else 'negative'}">{metrics['r2']:.4f}</div>
            </div>
            <div class="card">
                <h3>MAE</h3>
                <div class="value">${metrics['mae']:,.2f}</div>
            </div>
            <div class="card">
                <h3>RMSE</h3>
                <div class="value">${metrics['rmse']:,.2f}</div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart-container full-width">
                <div class="chart-title">Ventas Reales vs. Predichas por Mes</div>
                <canvas id="salesMonthChart"></canvas>
            </div>

            <div class="chart-container">
                <div class="chart-title">Error Promedio de Predicción por Mes</div>
                <canvas id="errorMonthChart"></canvas>
            </div>

            <div class="chart-container">
                <div class="chart-title">Predicción por Categoría</div>
                <canvas id="categoryChart"></canvas>
            </div>

            <div class="chart-container">
                <div class="chart-title">Error Promedio por Categoría</div>
                <canvas id="errorCategoryChart"></canvas>
            </div>

            <div class="chart-container">
                <div class="chart-title">Predicción por Zona</div>
                <canvas id="zoneChart"></canvas>
            </div>

            <div class="chart-container">
                <div class="chart-title">Error Promedio por Zona</div>
                <canvas id="errorZoneChart"></canvas>
            </div>

            <div class="chart-container">
                <div class="chart-title">Top 10 Productos con Mayor Venta Estimada</div>
                <canvas id="topPredictedChart"></canvas>
            </div>

            <div class="chart-container">
                <div class="chart-title">Top 10 Productos con Mayor Diferencia</div>
                <canvas id="topDiffChart"></canvas>
            </div>
        </div>

        <div class="chart-container full-width">
            <div class="chart-title">Top 10 Productos con Mayor Venta Estimada</div>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Producto</th>
                        <th>Categoría</th>
                        <th>Venta Estimada</th>
                        <th>Venta Real</th>
                    </tr>
                </thead>
                <tbody>
                    {top_predicted_rows}
                </tbody>
            </table>
        </div>

        <div class="chart-container full-width">
            <div class="chart-title">Top 10 Productos con Mayor Diferencia (Real vs. Predicho)</div>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Producto</th>
                        <th>Categoría</th>
                        <th>Diferencia Abs.</th>
                        <th>Diferencia %</th>
                        <th>Venta Real</th>
                        <th>Venta Predicha</th>
                    </tr>
                </thead>
                <tbody>
                    {top_diff_rows}
                </tbody>
            </table>
        </div>

        <div class="insights">
            <h2>Conclusiones: Oportunidades, Riesgos y Recomendaciones</h2>
            <h3>🚀 Oportunidades</h3>
            <ul>
                {''.join(f'<li>{o}</li>' for o in opportunities)}
            </ul>
            <h3>⚠️ Riesgos</h3>
            <ul>
                {''.join(f'<li>{r}</li>' for r in risks)}
            </ul>
            <h3>💡 Recomendaciones Comerciales</h3>
            <ul>
                {''.join(f'<li>{r}</li>' for r in recommendations)}
            </ul>
        </div>

        <footer>
            Generado automáticamente por dashboard_prediccion.py · MLNETModelBuilder-PowerBI
        </footer>
    </div>

    <script>
        const months = {months};
        const realMonthly = {real_monthly};
        const predictedMonthly = {predicted_monthly};
        const errorMonthly = {error_monthly};

        const categories = {categories};
        const realCategory = {real_category};
        const predictedCategory = {predicted_category};
        const errorCategory = {error_category};

        const zones = {zones};
        const realZone = {real_zone};
        const predictedZone = {predicted_zone};
        const errorZone = {error_zone};

        const topPredictedLabels = {top_predicted_labels};
        const topPredictedValues = {top_predicted_values};

        const topDiffLabels = {top_diff_labels};
        const topDiffValues = {top_diff_values};

        const formatCurrency = (value) => '$' + value.toLocaleString();

        // Ventas reales vs predichas por mes
        new Chart(document.getElementById('salesMonthChart'), {{
            type: 'bar',
            data: {{
                labels: months,
                datasets: [
                    {{
                        label: 'Ventas Reales',
                        data: realMonthly,
                        backgroundColor: '#2563eb',
                        borderRadius: 6
                    }},
                    {{
                        label: 'Ventas Predichas',
                        data: predictedMonthly,
                        backgroundColor: '#16a34a',
                        borderRadius: 6
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'top' }},
                    tooltip: {{ mode: 'index', intersect: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{ callback: formatCurrency }}
                    }}
                }}
            }}
        }});

        // Error promedio por mes
        new Chart(document.getElementById('errorMonthChart'), {{
            type: 'line',
            data: {{
                labels: months,
                datasets: [{{
                    label: 'Error Promedio (%)',
                    data: errorMonthly,
                    borderColor: '#dc2626',
                    backgroundColor: 'rgba(220, 38, 38, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 5,
                    pointBackgroundColor: '#dc2626'
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{ beginAtZero: true, ticks: {{ callback: v => v + '%' }} }}
                }}
            }}
        }});

        // Predicción por categoría
        new Chart(document.getElementById('categoryChart'), {{
            type: 'bar',
            data: {{
                labels: categories,
                datasets: [
                    {{
                        label: 'Ventas Reales',
                        data: realCategory,
                        backgroundColor: '#2563eb',
                        borderRadius: 6
                    }},
                    {{
                        label: 'Ventas Predichas',
                        data: predictedCategory,
                        backgroundColor: '#16a34a',
                        borderRadius: 6
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'top' }},
                    tooltip: {{ mode: 'index', intersect: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{ callback: formatCurrency }}
                    }}
                }}
            }}
        }});

        // Error por categoría
        new Chart(document.getElementById('errorCategoryChart'), {{
            type: 'bar',
            data: {{
                labels: categories,
                datasets: [{{
                    label: 'Error Promedio (%)',
                    data: errorCategory,
                    backgroundColor: errorCategory.map(v => v < 30 ? '#16a34a' : v < 50 ? '#ca8a04' : '#dc2626'),
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ beginAtZero: true, ticks: {{ callback: v => v + '%' }} }}
                }}
            }}
        }});

        // Predicción por zona
        new Chart(document.getElementById('zoneChart'), {{
            type: 'bar',
            data: {{
                labels: zones,
                datasets: [
                    {{
                        label: 'Ventas Reales',
                        data: realZone,
                        backgroundColor: '#7c3aed',
                        borderRadius: 6
                    }},
                    {{
                        label: 'Ventas Predichas',
                        data: predictedZone,
                        backgroundColor: '#06b6d4',
                        borderRadius: 6
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'top' }},
                    tooltip: {{ mode: 'index', intersect: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{ callback: formatCurrency }}
                    }}
                }}
            }}
        }});

        // Error por zona
        new Chart(document.getElementById('errorZoneChart'), {{
            type: 'bar',
            data: {{
                labels: zones,
                datasets: [{{
                    label: 'Error Promedio (%)',
                    data: errorZone,
                    backgroundColor: errorZone.map(v => v < 30 ? '#16a34a' : v < 50 ? '#ca8a04' : '#dc2626'),
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ beginAtZero: true, ticks: {{ callback: v => v + '%' }} }}
                }}
            }}
        }});

        // Top 10 productos con mayor venta estimada
        new Chart(document.getElementById('topPredictedChart'), {{
            type: 'bar',
            data: {{
                labels: topPredictedLabels,
                datasets: [{{
                    label: 'Venta Estimada',
                    data: topPredictedValues,
                    backgroundColor: '#16a34a',
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                indexAxis: 'y',
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{
                        beginAtZero: true,
                        ticks: {{ callback: formatCurrency }}
                    }}
                }}
            }}
        }});

        // Top 10 productos con mayor diferencia
        new Chart(document.getElementById('topDiffChart'), {{
            type: 'bar',
            data: {{
                labels: topDiffLabels,
                datasets: [{{
                    label: 'Diferencia Absoluta',
                    data: topDiffValues,
                    backgroundColor: '#dc2626',
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                indexAxis: 'y',
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{
                        beginAtZero: true,
                        ticks: {{ callback: formatCurrency }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard HTML generado exitosamente: {output_path}")


def main():
    csv_path = Path("resultados_prediccion.csv")
    if not csv_path.exists():
        print(f"Error: No se encontró el archivo {csv_path}")
        return

    records = parse_results(csv_path)
    if not records:
        print("Error: No se pudieron leer registros del CSV.")
        return

    output_path = Path("dashboard_prediccion.html")
    generate_html(records, output_path)


if __name__ == "__main__":
    main()
