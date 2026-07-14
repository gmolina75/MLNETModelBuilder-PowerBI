import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def parse_results(csv_path):
    """Lee el CSV de resultados y devuelve una lista de diccionarios."""
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
                    "year": date.year,
                    "product_name": row["product_name"],
                    "category_name": row["category_name"],
                    "zone_name": row["zone_name"],
                    "real_sales": real,
                    "predicted_sales": predicted,
                    "difference": diff,
                    "percentage_error": pct_error,
                })
            except Exception:
                continue
    return records


def parse_original_sales(csv_path):
    """Lee el CSV original de ventas (ej. 2025) y devuelve registros con ventas reales."""
    records = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.strptime(row["sale_date"], "%Y-%m-%d")
                total_sales = float(row["total_sales"])
                records.append({
                    "date": date,
                    "month": date.month,
                    "category_name": row.get("category_name", ""),
                    "total_sales": total_sales,
                })
            except Exception:
                continue
    return records


def aggregate_sales_by_month(records):
    """Agrega únicamente ventas totales por mes a partir de registros originales."""
    months = defaultdict(lambda: {"month_name": "", "count": 0, "total": 0.0})
    month_names_es = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
    }
    for r in records:
        m = r["month"]
        months[m]["month_name"] = month_names_es.get(m, r["date"].strftime("%B").capitalize())
        months[m]["count"] += 1
        months[m]["total"] += r["total_sales"]

    sorted_months = []
    for m in range(1, 13):
        if m in months:
            sorted_months.append((m, months[m]))
    return sorted_months


def aggregate_by_month(records):
    """Agrega métricas por mes."""
    months = defaultdict(lambda: {
        "month_name": "",
        "count": 0,
        "real_total": 0.0,
        "predicted_total": 0.0,
        "difference_total": 0.0,
        "errors": [],
        "records": [],
    })

    month_names_es = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
    }

    for r in records:
        m = r["month"]
        entry = months[m]
        entry["month_name"] = month_names_es.get(m, r["month_name"])
        entry["count"] += 1
        entry["real_total"] += r["real_sales"]
        entry["predicted_total"] += r["predicted_sales"]
        entry["difference_total"] += r["difference"]
        entry["errors"].append(r["percentage_error"])
        entry["records"].append(r)

    # Ordenar por número de mes.
    sorted_months = []
    for m in range(1, 13):
        if m in months:
            entry = months[m]
            entry["avg_error"] = sum(entry["errors"]) / len(entry["errors"])
            entry["max_error"] = max(entry["errors"])
            entry["min_error"] = min(entry["errors"])
            sorted_months.append((m, entry))

    return sorted_months


def overall_metrics(records):
    total_real = sum(r["real_sales"] for r in records)
    total_predicted = sum(r["predicted_sales"] for r in records)
    total_diff = sum(r["difference"] for r in records)
    avg_error = sum(r["percentage_error"] for r in records) / len(records)
    max_error = max(r["percentage_error"] for r in records)
    min_error = min(r["percentage_error"] for r in records)
    return {
        "total_records": len(records),
        "total_real": total_real,
        "total_predicted": total_predicted,
        "total_difference": total_diff,
        "avg_error": avg_error,
        "max_error": max_error,
        "min_error": min_error,
    }


def generate_html(records, monthly_data, original_monthly, metrics, year, output_path):
    months = [m[1]["month_name"] for m in monthly_data]
    real_totals = [round(m[1]["real_total"], 2) for m in monthly_data]
    predicted_totals = [round(m[1]["predicted_total"], 2) for m in monthly_data]
    avg_errors = [round(m[1]["avg_error"], 2) for m in monthly_data]
    counts = [m[1]["count"] for m in monthly_data]

    # Datos de 2025 para comparación: alinear por número de mes.
    original_by_month = {m: entry for m, entry in original_monthly}
    original_totals = [round(original_by_month.get(m[0], {"total": 0})["total"], 2) for m in monthly_data]
    yoy_growth = []
    for m_idx, m in enumerate(monthly_data):
        orig = original_totals[m_idx]
        curr = real_totals[m_idx]
        if orig > 0:
            yoy_growth.append(round((curr - orig) / orig * 100, 2))
        else:
            yoy_growth.append(0)

    # Tabla HTML mensual con comparación 2025.
    table_rows = ""
    for idx, (m, entry) in enumerate(monthly_data):
        original_total = original_totals[idx]
        diff_pct = (entry["predicted_total"] - entry["real_total"]) / entry["real_total"] * 100 if entry["real_total"] else 0
        yoy = yoy_growth[idx]
        table_rows += f"""
        <tr>
            <td>{entry['month_name']}</td>
            <td>{entry['count']}</td>
            <td>${original_total:,.2f}</td>
            <td>${entry['real_total']:,.2f}</td>
            <td>{yoy:+.2f}%</td>
            <td>${entry['predicted_total']:,.2f}</td>
            <td>${abs(entry['predicted_total'] - entry['real_total']):,.2f}</td>
            <td>{diff_pct:+.2f}%</td>
            <td>{entry['avg_error']:.2f}%</td>
            <td>{entry['min_error']:.2f}%</td>
            <td>{entry['max_error']:.2f}%</td>
        </tr>
        """

    # Insights por mes: mayor/menor venta, mejor/peor predicción, comparación YoY.
    best_month = min(monthly_data, key=lambda x: x[1]["avg_error"])
    worst_month = max(monthly_data, key=lambda x: x[1]["avg_error"])
    highest_real = max(monthly_data, key=lambda x: x[1]["real_total"])
    lowest_real = min(monthly_data, key=lambda x: x[1]["real_total"])

    highest_yoy_idx = max(range(len(yoy_growth)), key=lambda i: yoy_growth[i])
    lowest_yoy_idx = min(range(len(yoy_growth)), key=lambda i: yoy_growth[i])
    highest_yoy_month = monthly_data[highest_yoy_idx]
    lowest_yoy_month = monthly_data[lowest_yoy_idx]
    total_2025 = sum(original_totals)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Predicción de Ventas {year}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --primary: #2563eb;
            --success: #16a34a;
            --danger: #dc2626;
            --warning: #ca8a04;
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #1e293b;
            --muted: #64748b;
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
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        header {{
            text-align: center;
            padding: 2rem 0;
            border-bottom: 3px solid var(--primary);
            margin-bottom: 2rem;
        }}
        h1 {{ margin: 0; font-size: 2rem; color: var(--primary); }}
        .subtitle {{ color: var(--muted); margin-top: 0.5rem; }}
        .grid {{
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
        }}
        .card h3 {{
            margin: 0 0 0.75rem 0;
            font-size: 0.9rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .card .value {{
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text);
        }}
        .card .value.positive {{ color: var(--success); }}
        .card .value.negative {{ color: var(--danger); }}
        .chart-container {{
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}
        .chart-title {{
            font-size: 1.25rem;
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
        th {{ background: var(--primary); color: white; font-weight: 600; text-transform: uppercase; font-size: 0.8rem; }}
        td {{ border-bottom: 1px solid #e2e8f0; }}
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
        .insights ul {{ padding-left: 1.25rem; }}
        .insights li {{ margin-bottom: 0.5rem; }}
        .tag {{
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            color: white;
        }}
        .tag.success {{ background: var(--success); }}
        .tag.danger {{ background: var(--danger); }}
        .tag.warning {{ background: var(--warning); }}
        footer {{
            text-align: center;
            color: var(--muted);
            padding: 2rem 0;
            font-size: 0.875rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Reporte de Predicción de Ventas {year}</h1>
            <div class="subtitle">Análisis mensual de ventas reales vs. predichas</div>
        </header>

        <div class="grid">
            <div class="card">
                <h3>Total de Predicciones</h3>
                <div class="value">{metrics['total_records']:,}</div>
            </div>
            <div class="card">
                <h3>Ventas Reales Totales</h3>
                <div class="value">${metrics['total_real']:,.2f}</div>
            </div>
            <div class="card">
                <h3>Ventas Reales Totales 2025</h3>
                <div class="value">${total_2025:,.2f}</div>
            </div>
            <div class="card">
                <h3>Ventas Predichas Totales</h3>
                <div class="value">${metrics['total_predicted']:,.2f}</div>
            </div>
            <div class="card">
                <h3>Diferencia Total</h3>
                <div class="value {'positive' if metrics['total_predicted'] >= metrics['total_real'] else 'negative'}">${abs(metrics['total_predicted'] - metrics['total_real']):,.2f}</div>
            </div>
            <div class="card">
                <h3>Error Porcentual Promedio</h3>
                <div class="value {'positive' if metrics['avg_error'] < 40 else 'negative'}">{metrics['avg_error']:.2f}%</div>
            </div>
            <div class="card">
                <h3>Error Máximo</h3>
                <div class="value negative">{metrics['max_error']:.2f}%</div>
            </div>
        </div>

        <div class="chart-container">
            <div class="chart-title">Ventas Reales vs. Predichas por Mes</div>
            <canvas id="salesChart"></canvas>
        </div>

        <div class="chart-container">
            <div class="chart-title">Error Porcentual Promedio por Mes</div>
            <canvas id="errorChart"></canvas>
        </div>

        <div class="chart-container">
            <div class="chart-title">Cantidad de Registros por Mes</div>
            <canvas id="countChart"></canvas>
        </div>

        <div class="chart-container">
            <div class="chart-title">Comparación de Ventas: 2025 vs {year}</div>
            <canvas id="comparisonChart"></canvas>
        </div>

        <div class="chart-container">
            <div class="chart-title">Crecimiento Año contra Año (YoY) - Ventas Reales {year} vs 2025</div>
            <canvas id="yoyChart"></canvas>
        </div>

        <div class="chart-container">
            <div class="chart-title">Tabla de Resultados Mensuales con Comparación 2025</div>
            <table>
                <thead>
                    <tr>
                        <th>Mes</th>
                        <th>Registros</th>
                        <th>Ventas 2025</th>
                        <th>Ventas {year} Reales</th>
                        <th>Crecimiento YoY</th>
                        <th>Ventas {year} Predichas</th>
                        <th>Diferencia</th>
                        <th>Diferencia %</th>
                        <th>Error Prom.</th>
                        <th>Error Mín.</th>
                        <th>Error Máx.</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>

        <div class="insights">
            <h2>Insights del Análisis</h2>
            <ul>
                <li><strong>Mejor mes predicho:</strong> {best_month[1]['month_name']} con un error promedio de {best_month[1]['avg_error']:.2f}%.</li>
                <li><strong>Peor mes predicho:</strong> {worst_month[1]['month_name']} con un error promedio de {worst_month[1]['avg_error']:.2f}%.</li>
                <li><strong>Mes con mayores ventas reales:</strong> {highest_real[1]['month_name']} (${highest_real[1]['real_total']:,.2f}).</li>
                <li><strong>Mes con menores ventas reales:</strong> {lowest_real[1]['month_name']} (${lowest_real[1]['real_total']:,.2f}).</li>
                <li>El modelo {'sobrestima' if metrics['total_predicted'] > metrics['total_real'] else 'subestima'} las ventas anuales en un {abs((metrics['total_predicted'] - metrics['total_real']) / metrics['total_real'] * 100):.2f}%.</li>
                <li>El R² general del modelo indica que {'captura bien' if metrics.get('r2', 0) > 0.7 else 'captura parcialmente' if metrics.get('r2', 0) > 0.4 else 'no captura bien'} la variabilidad de las ventas.</li>
                <li><strong>Comparación con 2025:</strong> las ventas totales de 2025 fueron ${total_2025:,.2f}, mientras que las ventas reales proyectadas para {year} son ${metrics['total_real']:,.2f} ({((metrics['total_real'] - total_2025) / total_2025 * 100) if total_2025 else 0:+.2f}%).</li>
                <li><strong>Mayor crecimiento YoY:</strong> {highest_yoy_month[1]['month_name']} ({yoy_growth[highest_yoy_idx]:+.2f}%).</li>
                <li><strong>Mayor decrecimiento YoY:</strong> {lowest_yoy_month[1]['month_name']} ({yoy_growth[lowest_yoy_idx]:+.2f}%).</li>
            </ul>
        </div>

        <footer>
            Generado por SalesPredictGenerator · MLNETModelBuilder-PowerBI
        </footer>
    </div>

    <script>
        const months = {months};
        const realTotals = {real_totals};
        const predictedTotals = {predicted_totals};
        const avgErrors = {avg_errors};
        const counts = {counts};

        new Chart(document.getElementById('salesChart'), {{
            type: 'bar',
            data: {{
                labels: months,
                datasets: [
                    {{
                        label: 'Ventas Reales',
                        data: realTotals,
                        backgroundColor: '#2563eb',
                        borderRadius: 6
                    }},
                    {{
                        label: 'Ventas Predichas',
                        data: predictedTotals,
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
                        ticks: {{
                            callback: function(value) {{ return '$' + value.toLocaleString(); }}
                        }}
                    }}
                }}
            }}
        }});

        new Chart(document.getElementById('errorChart'), {{
            type: 'line',
            data: {{
                labels: months,
                datasets: [{{
                    label: 'Error Promedio (%)',
                    data: avgErrors,
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
                plugins: {{
                    legend: {{ position: 'top' }}
                }},
                scales: {{
                    y: {{ beginAtZero: true, ticks: {{ callback: function(value) {{ return value + '%'; }} }} }}
                }}
            }}
        }});

        new Chart(document.getElementById('countChart'), {{
            type: 'bar',
            data: {{
                labels: months,
                datasets: [{{
                    label: 'Registros',
                    data: counts,
                    backgroundColor: '#ca8a04',
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{ beginAtZero: true }}
                }}
            }}
        }});

        const originalTotals = {original_totals};
        const yoyGrowth = {yoy_growth};

        new Chart(document.getElementById('comparisonChart'), {{
            type: 'bar',
            data: {{
                labels: months,
                datasets: [
                    {{
                        label: 'Ventas 2025',
                        data: originalTotals,
                        backgroundColor: '#94a3b8',
                        borderRadius: 6
                    }},
                    {{
                        label: 'Ventas {year} Reales',
                        data: realTotals,
                        backgroundColor: '#2563eb',
                        borderRadius: 6
                    }},
                    {{
                        label: 'Ventas {year} Predichas',
                        data: predictedTotals,
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
                        ticks: {{
                            callback: function(value) {{ return '$' + value.toLocaleString(); }}
                        }}
                    }}
                }}
            }}
        }});

        new Chart(document.getElementById('yoyChart'), {{
            type: 'bar',
            data: {{
                labels: months,
                datasets: [{{
                    label: 'Crecimiento YoY (%)',
                    data: yoyGrowth,
                    backgroundColor: yoyGrowth.map(v => v >= 0 ? '#16a34a' : '#dc2626'),
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{ return context.parsed.y + '%'; }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        ticks: {{ callback: function(value) {{ return value + '%'; }} }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    # Calcular R² general para el insight.
    mean_real = metrics["total_real"] / metrics["total_records"]
    ss_tot = sum((r["real_sales"] - mean_real) ** 2 for r in records)
    ss_res = sum((r["real_sales"] - r["predicted_sales"]) ** 2 for r in records)
    metrics["r2"] = 1 - (ss_res / ss_tot) if ss_tot else 0

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Reporte HTML generado exitosamente: {output_path}")


def main():
    year = 2027
    if len(sys.argv) > 1:
        year = sys.argv[1]

    csv_path = Path(f"resultados_prediccion_{year}.csv")
    if not csv_path.exists():
        print(f"Error: No se encontró el archivo {csv_path}")
        print("Ejecuta primero SalesPredictGenerator para generar las predicciones.")
        return

    output_path = Path(f"reporte_prediccion_{year}.html")

    records = parse_results(csv_path)
    if not records:
        print("Error: No se pudieron leer registros del CSV.")
        return

    # Leer datos históricos de 2025 para comparación.
    original_csv = Path("ventas_sinteticas_2025.csv")
    original_records = []
    if original_csv.exists():
        original_records = parse_original_sales(original_csv)
    else:
        print(f"Advertencia: No se encontró {original_csv}. El reporte no incluirá comparación con 2025.")

    monthly_data = aggregate_by_month(records)
    original_monthly = aggregate_sales_by_month(original_records)
    metrics = overall_metrics(records)
    generate_html(records, monthly_data, original_monthly, metrics, year, output_path)


if __name__ == "__main__":
    main()
