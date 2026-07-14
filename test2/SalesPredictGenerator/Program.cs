using System;
using System.IO;
using System.Diagnostics;
using System.Globalization;
using System.Linq;
using System.Collections.Generic;

namespace SalesPredict
{
    internal class Program
    {
        // Directorio de trabajo fijo: raíz del repositorio del proyecto.
        private const string ProjectRoot = @"G:\My Drive\estudios\ecotec\docencia\Modelos de Datos\MLNETModelBuilder-PowerBI";

        static void Main(string[] args)
        {
            // ── 0. Establecer directorio de trabajo ──────────────────────────
            try
            {
                if (Directory.Exists(ProjectRoot))
                {
                    Directory.SetCurrentDirectory(ProjectRoot);
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine($"⚠ No se encontró la raíz del proyecto: {ProjectRoot}");
                    Console.WriteLine("  Se usará el directorio actual.");
                    Console.ResetColor();
                    Console.WriteLine();
                }
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine($"⚠ No se pudo cambiar al directorio del proyecto: {ex.Message}");
                Console.ResetColor();
                Console.WriteLine();
            }

            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("╔══════════════════════════════════════════════════════════════════════╗");
            Console.WriteLine("║   SalesPredictGenerator - Asistente de predicción de ventas futuras  ║");
            Console.WriteLine("╚══════════════════════════════════════════════════════════════════════╝");
            Console.ResetColor();
            Console.WriteLine();
            Console.WriteLine($"Directorio de trabajo: {Directory.GetCurrentDirectory()}");
            Console.WriteLine();

            // ── 1. Pedir año objetivo ────────────────────────────────────────
            Console.WriteLine("[1/8] Configuración de la predicción");
            Console.WriteLine("      ─────────────────────────────────────────");

            int targetYear;
            while (true)
            {
                Console.Write("      → ¿Para qué año deseas generar las predicciones? (ejemplo: 2027): ");
                string yearInput = Console.ReadLine();

                if (int.TryParse(yearInput, out targetYear) && targetYear >= 2000 && targetYear <= 2100)
                {
                    break;
                }

                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("      ⚠ Por favor ingresa un año válido entre 2000 y 2100.");
                Console.ResetColor();
            }

            // ── 2. Pedir factor de crecimiento anual ─────────────────────────
            Console.WriteLine();
            Console.WriteLine($"      → Año seleccionado: {targetYear}");
            Console.WriteLine();
            Console.WriteLine("      Ahora define el crecimiento anual para extrapolar las ventas.");
            Console.WriteLine("      Ejemplo: 3 significa 3% de crecimiento por año respecto a 2025.");

            float annualGrowthPercent;
            while (true)
            {
                Console.Write("      → ¿Porcentaje de crecimiento anual? (0 para mantener valores, Enter = 0): ");
                string growthInput = Console.ReadLine();

                if (string.IsNullOrWhiteSpace(growthInput))
                {
                    annualGrowthPercent = 0f;
                    break;
                }

                if (float.TryParse(growthInput, NumberStyles.Float, CultureInfo.InvariantCulture, out annualGrowthPercent) && annualGrowthPercent >= -100 && annualGrowthPercent <= 1000)
                {
                    break;
                }

                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("      ⚠ Ingresa un número entre -100 y 1000, o deja en blanco para 0.");
                Console.ResetColor();
            }

            int yearsDifference = targetYear - 2025;
            float totalGrowthFactor = (float)Math.Pow(1 + annualGrowthPercent / 100.0, yearsDifference);

            Console.WriteLine($"      → Crecimiento anual: {annualGrowthPercent}%");
            Console.WriteLine($"      → Diferencia de años: {yearsDifference}");
            Console.WriteLine($"      → Factor de crecimiento acumulado: {totalGrowthFactor:F4}");
            Console.WriteLine("      ─────────────────────────────────────────");
            Console.WriteLine();

            string sourceCsvPath = Path.Combine(Directory.GetCurrentDirectory(), "ventas_sinteticas_2025.csv");
            string generatedCsvPath = Path.Combine(Directory.GetCurrentDirectory(), $"ventas_sinteticas_{targetYear}.csv");
            string outputCsvPath = Path.Combine(Directory.GetCurrentDirectory(), $"resultados_prediccion_{targetYear}.csv");

            // ── 3. Validar archivo fuente ────────────────────────────────────
            Console.WriteLine("[2/8] Buscando datos históricos...");
            Console.WriteLine($"      → Archivo base: {sourceCsvPath}");

            if (!File.Exists(sourceCsvPath))
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("      ✖ Error: No se encontró 'ventas_sinteticas_2025.csv'.");
                Console.ResetColor();
                Console.WriteLine();
                Console.WriteLine("Presiona ENTER para salir...");
                Console.ReadLine();
                return;
            }

            var sourceLines = File.ReadAllLines(sourceCsvPath);
            if (sourceLines.Length <= 1)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("      ✖ Error: El archivo base no contiene datos.");
                Console.ResetColor();
                Console.WriteLine();
                Console.WriteLine("Presiona ENTER para salir...");
                Console.ReadLine();
                return;
            }

            int totalRecords = sourceLines.Length - 1;
            Console.WriteLine($"      ✔ Archivo base encontrado con {totalRecords:N0} registros de 2025.");
            Console.WriteLine();

            // ── 4. Generar datos extrapolados para el año objetivo ───────────
            Console.WriteLine($"[3/8] Generando datos extrapolados para el año {targetYear}...");

            using (var writer = new StreamWriter(generatedCsvPath))
            {
                writer.WriteLine(sourceLines[0]);

                for (int i = 1; i < sourceLines.Length; i++)
                {
                    if (string.IsNullOrWhiteSpace(sourceLines[i])) continue;

                    var cols = sourceLines[i].Split(',');
                    if (cols.Length <= 17) continue;

                    if (!DateTime.TryParseExact(cols[1], "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out DateTime originalDate))
                    {
                        continue;
                    }

                    // Calcular nueva fecha en el año objetivo.
                    DateTime newDate = new DateTime(targetYear, originalDate.Month, originalDate.Day);

                    // Aplicar crecimiento a valores numéricos.
                    if (!float.TryParse(cols[14], NumberStyles.Float, CultureInfo.InvariantCulture, out float quantity)) quantity = 0f;
                    if (!float.TryParse(cols[15], NumberStyles.Float, CultureInfo.InvariantCulture, out float unitPrice)) unitPrice = 0f;
                    if (!float.TryParse(cols[16], NumberStyles.Float, CultureInfo.InvariantCulture, out float discountPercentage)) discountPercentage = 0f;
                    if (!float.TryParse(cols[17], NumberStyles.Float, CultureInfo.InvariantCulture, out float totalSales)) totalSales = 0f;

                    quantity = (float)Math.Round(quantity * totalGrowthFactor, 0);
                    unitPrice = (float)Math.Round(unitPrice * totalGrowthFactor, 2);
                    totalSales = (float)Math.Round(quantity * unitPrice * (1 - discountPercentage / 100), 2);

                    // Reconstruir el registro.
                    cols[0] = $"SALE-{targetYear}-{i:D5}";
                    cols[1] = newDate.ToString("yyyy-MM-dd");
                    cols[2] = targetYear.ToString();
                    cols[5] = (((int)newDate.DayOfWeek + 6) % 7 + 1).ToString(); // 1=Lunes, 7=Domingo
                    cols[14] = quantity.ToString(CultureInfo.InvariantCulture);
                    cols[15] = unitPrice.ToString(CultureInfo.InvariantCulture);
                    cols[17] = totalSales.ToString(CultureInfo.InvariantCulture);

                    writer.WriteLine(string.Join(",", cols));

                    if (i % 500 == 0)
                    {
                        Console.WriteLine($"      → {i:N0} de {totalRecords:N0} registros generados...");
                    }
                }
            }

            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine($"      ✔ Datos extrapolados guardados en: {generatedCsvPath}");
            Console.ResetColor();
            Console.WriteLine();

            // ── 5. Cargar modelo y predecir ──────────────────────────────────
            Console.WriteLine("[4/8] Cargando modelo predictivo SalesPredict.mlnet...");
            try
            {
                var _ = SalesPredict.PredictEngine.Value;
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("      ✔ Modelo cargado exitosamente.");
                Console.ResetColor();
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"      ✖ Error al cargar el modelo: {ex.Message}");
                Console.ResetColor();
                Console.WriteLine();
                Console.WriteLine("Presiona ENTER para salir...");
                Console.ReadLine();
                return;
            }
            Console.WriteLine();

            Console.WriteLine($"[5/8] Procesando predicciones para {targetYear}...");

            var predictionLines = File.ReadAllLines(generatedCsvPath);
            int processed = 0;
            int skipped = 0;
            float sumRealSales = 0f;
            float sumPredictedSales = 0f;
            float sumDifference = 0f;
            float sumSquaredDifference = 0f;
            float sumPercentageError = 0f;
            float minPercentageError = float.MaxValue;
            float maxPercentageError = 0f;
            float minRealSales = float.MaxValue;
            float maxRealSales = 0f;
            float minPredictedSales = float.MaxValue;
            float maxPredictedSales = 0f;
            int countErrorUnder5 = 0;
            int countErrorUnder10 = 0;
            int countErrorUnder20 = 0;
            int countErrorUnder30 = 0;
            var realSalesList = new List<float>();

            using (var writer = new StreamWriter(outputCsvPath))
            {
                writer.WriteLine("sale_date,product_name,category_name,zone_name,salesman_name,warehouse_name,real_sales,predicted_sales,difference,percentage_error");

                for (int i = 1; i < predictionLines.Length; i++)
                {
                    if (string.IsNullOrWhiteSpace(predictionLines[i]))
                    {
                        skipped++;
                        continue;
                    }

                    var cols = predictionLines[i].Split(',');
                    if (cols.Length <= 17)
                    {
                        skipped++;
                        continue;
                    }

                    string saleDate = cols[1];
                    string productName = cols[9];
                    string categoryName = cols[10];
                    string zoneName = cols[11];
                    string salesmanName = cols[12];
                    string warehouseName = cols[13];

                    if (!float.TryParse(cols[14], NumberStyles.Float, CultureInfo.InvariantCulture, out float quantity)) quantity = 0f;
                    if (!float.TryParse(cols[15], NumberStyles.Float, CultureInfo.InvariantCulture, out float unitPrice)) unitPrice = 0f;
                    if (!float.TryParse(cols[16], NumberStyles.Float, CultureInfo.InvariantCulture, out float discountPercentage)) discountPercentage = 0f;
                    if (!float.TryParse(cols[17], NumberStyles.Float, CultureInfo.InvariantCulture, out float realSales)) realSales = 0f;

                    var sampleData = new SalesPredict.ModelInput()
                    {
                        Sale_id = cols[0],
                        Sale_date = cols[1],
                        Year_number = float.Parse(cols[2], CultureInfo.InvariantCulture),
                        Month_number = float.Parse(cols[3], CultureInfo.InvariantCulture),
                        Day_number = float.Parse(cols[4], CultureInfo.InvariantCulture),
                        Day_of_week = float.Parse(cols[5], CultureInfo.InvariantCulture),
                        Customer_code = cols[6],
                        Customer_name = cols[7],
                        Product_code = cols[8],
                        Product_name = cols[9],
                        Category_name = cols[10],
                        Zone_name = cols[11],
                        Salesman_name = cols[12],
                        Warehouse_name = cols[13],
                        Quantity = quantity,
                        Unit_price = unitPrice,
                        Discount_percentage = discountPercentage,
                        Total_sales = realSales
                    };

                    var result = SalesPredict.Predict(sampleData);
                    float predictedSales = result.Score;

                    float difference = Math.Abs(realSales - predictedSales);
                    float percentageError = realSales == 0 ? 0 : (difference / realSales) * 100;

                    string outputLine = $"{saleDate},{productName},{categoryName},{zoneName},{salesmanName},{warehouseName}," +
                                        $"{Math.Round(realSales, 2).ToString(CultureInfo.InvariantCulture)}," +
                                        $"{Math.Round(predictedSales, 2).ToString(CultureInfo.InvariantCulture)}," +
                                        $"{Math.Round(difference, 2).ToString(CultureInfo.InvariantCulture)}," +
                                        $"{Math.Round(percentageError, 2).ToString(CultureInfo.InvariantCulture)}%";

                    writer.WriteLine(outputLine);

                    processed++;
                    sumRealSales += realSales;
                    sumPredictedSales += predictedSales;
                    sumDifference += difference;
                    sumSquaredDifference += difference * difference;
                    sumPercentageError += percentageError;
                    realSalesList.Add(realSales);

                    if (percentageError < minPercentageError) minPercentageError = percentageError;
                    if (percentageError > maxPercentageError) maxPercentageError = percentageError;
                    if (realSales < minRealSales) minRealSales = realSales;
                    if (realSales > maxRealSales) maxRealSales = realSales;
                    if (predictedSales < minPredictedSales) minPredictedSales = predictedSales;
                    if (predictedSales > maxPredictedSales) maxPredictedSales = predictedSales;
                    if (percentageError < 5) countErrorUnder5++;
                    if (percentageError < 10) countErrorUnder10++;
                    if (percentageError < 20) countErrorUnder20++;
                    if (percentageError < 30) countErrorUnder30++;

                    if (processed % 500 == 0)
                    {
                        Console.WriteLine($"      → {processed:N0} de {totalRecords:N0} predicciones completadas ({(processed * 100 / totalRecords)}%)...");
                    }
                }
            }

            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine($"      ✔ Predicciones completadas: {processed:N0} registros.");
            Console.ResetColor();
            if (skipped > 0)
            {
                Console.WriteLine($"        ({skipped:N0} registros omitidos por estar vacíos o mal formados).");
            }
            Console.WriteLine();

            // ── 6. Resumen final ─────────────────────────────────────────────
            Console.WriteLine("[6/8] Resumen de resultados");
            Console.WriteLine("      ─────────────────────────────────────────");
            Console.WriteLine($"      Año proyectado:        {targetYear}");
            Console.WriteLine($"      Archivo de entrada:    {generatedCsvPath}");
            Console.WriteLine($"      Archivo de resultados: {outputCsvPath}");
            Console.WriteLine($"      Total predicciones:    {processed:N0}");
            Console.WriteLine($"      Suma ventas reales:    ${sumRealSales:N2}");
            Console.WriteLine($"      Suma ventas predichas: ${sumPredictedSales:N2}");
            Console.WriteLine($"      Diferencia total:      ${Math.Abs(sumRealSales - sumPredictedSales):N2}");
            if (processed > 0)
            {
                float averageError = sumPercentageError / processed;
                float mae = sumDifference / processed;
                float rmse = (float)Math.Sqrt(sumSquaredDifference / processed);
                float meanReal = sumRealSales / processed;
                float ssTot = realSalesList.Sum(r => (r - meanReal) * (r - meanReal));
                float r2 = ssTot == 0 ? 0 : 1 - (sumSquaredDifference / ssTot);

                Console.WriteLine($"      Venta real promedio:     ${meanReal:F2}");
                Console.WriteLine($"      Venta predicha promedio: ${(sumPredictedSales / processed):F2}");
                Console.WriteLine($"      Venta real mínima:       ${minRealSales:F2}");
                Console.WriteLine($"      Venta real máxima:       ${maxRealSales:F2}");
                Console.WriteLine($"      Venta predicha mínima:   ${minPredictedSales:F2}");
                Console.WriteLine($"      Venta predicha máxima:   ${maxPredictedSales:F2}");
                Console.WriteLine();
                Console.WriteLine($"      MAE (Error Absoluto Medio): ${mae:F2}");
                Console.WriteLine($"      RMSE (Raíz Error Cuadrático Medio): ${rmse:F2}");
                Console.WriteLine($"      R² (Coeficiente de determinación): {r2:F4}");
                Console.WriteLine();
                Console.WriteLine($"      Error porcentual mínimo: {minPercentageError:F2}%");
                Console.WriteLine($"      Error porcentual promedio: {averageError:F2}%");
                Console.WriteLine($"      Error porcentual máximo:   {maxPercentageError:F2}%");
                Console.WriteLine();
                Console.WriteLine($"      Distribución de errores porcentuales:");
                Console.WriteLine($"        - Menor a 5%:   {countErrorUnder5:N0} registros ({(countErrorUnder5 * 100f / processed):F1}%)");
                Console.WriteLine($"        - Menor a 10%:  {countErrorUnder10:N0} registros ({(countErrorUnder10 * 100f / processed):F1}%)");
                Console.WriteLine($"        - Menor a 20%:  {countErrorUnder20:N0} registros ({(countErrorUnder20 * 100f / processed):F1}%)");
                Console.WriteLine($"        - Menor a 30%:  {countErrorUnder30:N0} registros ({(countErrorUnder30 * 100f / processed):F1}%)");
            }
            Console.WriteLine("      ─────────────────────────────────────────");
            Console.WriteLine();

            // ── 7. Conclusión sobre la calidad de la predicción ──────────────
            Console.WriteLine("[7/8] Conclusión sobre la predicción");
            Console.WriteLine("      ─────────────────────────────────────────");

            string conclusion;
            ConsoleColor conclusionColor;
            string explanation;

            if (processed > 0)
            {
                float averageError = sumPercentageError / processed;
                float totalDifferencePercent = sumRealSales == 0 ? 0 : Math.Abs(sumRealSales - sumPredictedSales) / sumRealSales * 100;
                float meanReal = sumRealSales / processed;
                float ssTot = realSalesList.Sum(r => (r - meanReal) * (r - meanReal));
                float r2 = ssTot == 0 ? 0 : 1 - (sumSquaredDifference / ssTot);

                // Evaluación combinada: R² mide la calidad general del ajuste;
                // el error porcentual promedio puede verse distorsionado por ventas muy pequeñas.
                if (r2 >= 0.8 && totalDifferencePercent < 15 && averageError < 80)
                {
                    conclusion = "POSITIVA";
                    conclusionColor = ConsoleColor.Green;
                    explanation = "El modelo captura bien la variabilidad de las ventas (R² alto) y el total predicho es cercano al real. Es confiable para estimar el comportamiento general.";
                }
                else if (r2 >= 0.5 && totalDifferencePercent < 40 && averageError < 150)
                {
                    conclusion = "REGULAR";
                    conclusionColor = ConsoleColor.Yellow;
                    explanation = "El modelo acierta la tendencia general y el total global, pero algunas predicciones individuales se desvían. Útil como referencia, no como cifra exacta.";
                }
                else
                {
                    conclusion = "NEGATIVA";
                    conclusionColor = ConsoleColor.Red;
                    explanation = "El modelo no logra ajustarse bien a los datos. No es confiable para este escenario; se recomienda reentrenar con datos más representativos.";
                }

                Console.WriteLine($"      R² del modelo:         {r2:F4}");
                Console.WriteLine($"      Error promedio:        {averageError:F2}%");
                Console.WriteLine($"      Diferencia total:      {totalDifferencePercent:F2}%");
                Console.Write("      Veredicto:             ");
                Console.ForegroundColor = conclusionColor;
                Console.WriteLine(conclusion);
                Console.ResetColor();
                Console.WriteLine($"      Explicación:           {explanation}");
            }
            else
            {
                Console.WriteLine("      No se procesaron registros válidos, por lo tanto no se puede emitir una conclusión.");
            }

            Console.WriteLine("      ─────────────────────────────────────────");
            Console.WriteLine();

            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine($"🎉 ¡Listo! Se generaron los datos y las predicciones para el año {targetYear}.");
            Console.ResetColor();
            Console.WriteLine();

            // ── 8. Generar reporte HTML automáticamente ───────────────────────
            GenerateHtmlReport(targetYear);

            Console.WriteLine();
            Console.WriteLine("Presiona ENTER para cerrar esta ventana...");
            Console.ReadLine();
        }

        static void GenerateHtmlReport(int year)
        {
            Console.WriteLine("[8/8] Generando reporte HTML automáticamente...");

            string scriptName = "generate_html_report.py";
            string scriptPath = Path.Combine(Directory.GetCurrentDirectory(), scriptName);

            if (!File.Exists(scriptPath))
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine($"      ⚠ No se encontró el script '{scriptName}'. Reporte HTML no generado.");
                Console.ResetColor();
                return;
            }

            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"\"{scriptName}\" {year}",
                    WorkingDirectory = Directory.GetCurrentDirectory(),
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using (var process = Process.Start(psi))
                {
                    if (process == null)
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine("      ⚠ No se pudo iniciar el proceso de Python.");
                        Console.ResetColor();
                        return;
                    }

                    string output = process.StandardOutput.ReadToEnd();
                    string error = process.StandardError.ReadToEnd();
                    process.WaitForExit();

                    if (process.ExitCode == 0)
                    {
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.WriteLine($"      ✔ Reporte HTML generado: reporte_prediccion_{year}.html");
                        Console.ResetColor();
                        if (!string.IsNullOrWhiteSpace(output))
                        {
                            Console.WriteLine($"        {output.Trim()}");
                        }

                        // Abrir el reporte en el navegador predeterminado.
                        try
                        {
                            string htmlPath = Path.Combine(Directory.GetCurrentDirectory(), $"reporte_prediccion_{year}.html");
                            Console.WriteLine("      → Abriendo reporte en el navegador...");
                            Process.Start(new ProcessStartInfo(htmlPath) { UseShellExecute = true });
                        }
                        catch (Exception openEx)
                        {
                            Console.ForegroundColor = ConsoleColor.Yellow;
                            Console.WriteLine($"      ⚠ No se pudo abrir el navegador: {openEx.Message}");
                            Console.ResetColor();
                        }
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine($"      ⚠ El script de Python terminó con código {process.ExitCode}.");
                        Console.ResetColor();
                        if (!string.IsNullOrWhiteSpace(error))
                        {
                            Console.WriteLine($"        {error.Trim()}");
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine($"      ⚠ No se pudo generar el reporte HTML: {ex.Message}");
                Console.ResetColor();
            }
        }
    }
}
