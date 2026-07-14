using System;
using System.IO;
using System.Globalization;

Console.WriteLine("Iniciando generación de predicciones con el modelo ML.NET...");

// Rutas a los archivos. Al ejecutar desde VS suele correr en bin/Debug/net10.0/
string inputCsvPath = @"..\..\..\..\ventas_sinteticas_2025.csv";
string outputCsvPath = @"..\..\..\..\resultados_prediccion.csv";

if (!File.Exists(inputCsvPath))
{
    // Respaldo por si se ejecuta directamente en la raíz de la carpeta
    inputCsvPath = @"..\ventas_sinteticas_2025.csv";
    outputCsvPath = @"..\resultados_prediccion.csv";
}

if (!File.Exists(inputCsvPath))
{
    Console.WriteLine("Error: No se encontró el archivo 'ventas_sinteticas_2025.csv'. Verifica la ruta.");
    return;
}

var lines = File.ReadAllLines(inputCsvPath);
if (lines.Length <= 1)
{
    Console.WriteLine("El archivo CSV no contiene datos.");
    return;
}

// Asegurarse de que el directorio de salida exista
var outDir = Path.GetDirectoryName(outputCsvPath);
if (!string.IsNullOrEmpty(outDir)) Directory.CreateDirectory(outDir);

using (var writer = new StreamWriter(outputCsvPath))
{
    // Escribir el nuevo encabezado según la rúbrica
    writer.WriteLine("sale_date,product_name,category_name,zone_name,salesman_name,warehouse_name,real_sales,predicted_sales,difference,percentage_error");

    // Iterar a partir de la fila 1 para saltarse el encabezado original
    for (int i = 1; i < lines.Length; i++)
    {
        if (string.IsNullOrWhiteSpace(lines[i])) continue;

        var cols = lines[i].Split(',');
        // Validar que existan suficientes columnas para evitar excepciones en tiempo de ejecución
        if (cols.Length <= 17) continue;

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

        // Crear el input para el modelo ML.NET
        var sampleData = new SalesPredict.SalesPredict.ModelInput()
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

        // Realizar la predicción consumiendo el modelo generado
        var result = SalesPredict.SalesPredict.Predict(sampleData);
        float predictedSales = result.Score;

        // Calcular la diferencia y el porcentaje de error
        float difference = Math.Abs(realSales - predictedSales);
        float percentageError = realSales == 0 ? 0 : (difference / realSales) * 100;

        // Formatear la línea de salida asegurando que haya punto decimal y dos decimales
        string outputLine = $"{saleDate},{productName},{categoryName},{zoneName},{salesmanName},{warehouseName}," +
                            $"{Math.Round(realSales, 2).ToString(CultureInfo.InvariantCulture)}," +
                            $"{Math.Round(predictedSales, 2).ToString(CultureInfo.InvariantCulture)}," +
                            $"{Math.Round(difference, 2).ToString(CultureInfo.InvariantCulture)}," +
                            $"{Math.Round(percentageError, 2).ToString(CultureInfo.InvariantCulture)}%";

        writer.WriteLine(outputLine);
    }
}

Console.WriteLine($"Predicciones generadas exitosamente en: {Path.GetFullPath(outputCsvPath)}");
