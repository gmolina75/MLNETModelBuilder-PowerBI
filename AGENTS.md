# Guía para agentes de código - MLNETModelBuilder-PowerBI

> Este archivo está escrito en español porque toda la documentación, comentarios y nomenclatura del proyecto usan el español como idioma principal.

## 1. Visión general del proyecto

Este repositorio contiene una **actividad académica de Inteligencia de Negocios** cuyo objetivo es construir un flujo completo de analítica predictiva con bajo código:

1. Generar una base de datos sintética de ventas con Python.
2. Entrenar visualmente un modelo de regresión con **ML.NET Model Builder** dentro de Visual Studio.
3. Generar un archivo `resultados_prediccion.csv` que compare ventas reales vs. predichas.
4. Construir un dashboard en Excel o Power BI con los hallazgos de negocio.

El escenario simula una empresa comercial de productos de consumo masivo en Ecuador (zonas: Guayaquil, Quito, Cuenca, Manta, Ambato). La variable objetivo a predecir es `total_sales`.

Archivos principales en la raíz:

| Archivo / Carpeta | Propósito |
|-------------------|-----------|
| `generate_synthetic_sales.py` | Script Python que genera `ventas_sinteticas_2025.csv`. |
| `ventas_sinteticas_2025.csv` | Datos sintéticos de 3.000 registros usados para entrenar el modelo. |
| `resultados_prediccion.csv` | CSV de salida generado por `SalesPredictionApp` (ventas reales, predichas, diferencia y % de error). |
| `Tarea_Prediccion_Ventas_MLNET_ModelBuilder.docx` | Enunciado/detalle de la tarea. |
| `Guía de instalación de Visual Studio Community 2026 y ML.NET Model Builder.docx` | Instrucciones de instalación. |
| `Paso a Paso_ Entrenamiento Visual en Visual Studio.docx` | Guía paso a paso del entrenamiento en Model Builder. |
| `extracted_text_utf8.txt` | Texto plano extraído del enunciado de la tarea. |
| `temp_docx/` | Extracción XML del contenido de un documento Word. |
| `SalesPrediction1/` | Proyecto de consola **.NET Framework 4.8.1** generado por ML.NET Model Builder (contiene un modelo ya entrenado). |
| `SalesPredictionApp/` | Proyecto de consola **.NET 10** en formato SDK, plantilla para generar predicciones masivas. |
| `dashboard_prediccion.py` | Script Python que genera un dashboard HTML interactivo a partir de `resultados_prediccion.csv`. |
| `dashboard_prediccion.html` | Dashboard web con KPIs, gráficos por mes/categoría/zona y conclusiones comerciales. |

## 2. Stack tecnológico

- **Python 3** (solo librería estándar: `csv`, `random`, `datetime`) para la generación de datos sintéticos.
- **C# / .NET**:
  - `SalesPrediction1`: proyecto clásico `.csproj` para **.NET Framework 4.8.1`, generado por ML.NET Model Builder.
  - `SalesPredictionApp`: proyecto moderno **SDK-style** que apunta a **.NET 10.0** (`net10.0`).
- **ML.NET / ML.NET AutoML** para el entrenamiento y consumo del modelo de regresión.
- **Plotly.NET** (aparece en `SalesPrediction.evaluate.cs`) para graficar predicciones vs. valores reales.
- **CSV/Excel/Power BI** como formato de datos y visualización final.
- **Chart.js** para los gráficos del dashboard HTML (`dashboard_prediccion.html`).
- **Visual Studio 2026** (versión 18.x) es el IDE recomendado; Model Builder solo funciona en Visual Studio para Windows.

## 3. Estructura y organización del código

```
MLNETModelBuilder-PowerBI/
├── .vscode/
│   └── settings.json                 # Prefiere la extensión de C# en VS Code.
├── SalesPrediction1/                 # Proyecto .NET Framework 4.8.1 (Model Builder)
│   ├── App.config
│   ├── Program.cs                    # Ejemplo de predicción sobre un único registro.
│   ├── SalesPrediction1.csproj
│   ├── SalesPrediction1.slnx
│   ├── SalesPrediction.mbconfig      # Configuración de entrenamiento de Model Builder.
│   ├── SalesPrediction.mlnet         # Modelo serializado entrenado.
│   ├── SalesPrediction.consumption.cs# Clases ModelInput/ModelOutput + Predict().
│   ├── SalesPrediction.training.cs   # Pipeline y método Train() para reentrenar.
│   └── SalesPrediction.evaluate.cs   # Cálculo de PFI y gráfico de R².
├── SalesPredictionApp/               # Proyecto .NET 10 (plantilla para el estudiante)
│   ├── Program.cs                    # Lee CSV, genera resultados_prediccion.csv.
│   ├── SalesModel.mbconfig           # Configuración de Model Builder SIN entrenar.
│   ├── SalesPredictionApp.csproj
│   └── SalesPredictionApp.sln
├── generate_synthetic_sales.py
├── ventas_sinteticas_2025.csv
├── resultados_prediccion.csv
├── dashboard_prediccion.py
└── dashboard_prediccion.html
```

### 3.1. `SalesPrediction1`

- Fue creado automáticamente por ML.NET Model Builder.
- Contiene un modelo entrenado (`SalesPrediction.mlnet`) cuyo mejor trial fue **FastForestRegression** con **R² ≈ 0.904**.
- El archivo `.mbconfig` guarda rutas absolutas locales (`G:\My Drive\...`), por lo que **no es portable**.
- Los archivos `*.consumption.cs`, `*.training.cs` y `*.evaluate.cs` son de solo lectura para el agente: fueron generados por la herramienta y se regeneran si se vuelve a entrenar el modelo.
- **Estado actual**: el proyecto no referencia los paquetes NuGet necesarios (`Microsoft.ML`, `Microsoft.ML.FastTree`, `Plotly.NET`, etc.), por lo que **no compila tal como está**. Faltan las referencias de paquetes que normalmente agrega Model Builder.

### 3.2. `SalesPredictionApp`

- Es el proyecto que debe usar el estudiante para producir el archivo de predicciones masivas.
- Incluye `Microsoft.ML.AutoML` y `Microsoft.CodeAnalysis.CSharp` como paquetes NuGet.
- El modelo aún **no ha sido generado**: solo existe `SalesModel.mbconfig`.
- `Program.cs` tiene el código de consumo del modelo **comentado** y, como simulación temporal, genera predicciones aleatorias dentro de ±5 % del valor real.
- Cuando se genere el modelo con Model Builder, se deben descomentar las líneas que usan `SalesModel.ModelInput` / `SalesModel.Predict` y eliminar el bloque de simulación.

## 4. Cómo compilar y ejecutar

### 4.1. Generar / regenerar los datos sintéticos

```bash
python generate_synthetic_sales.py
```

Esto sobrescribe `ventas_sinteticas_2025.csv` con 3.000 registros.

Validaciones manuales recomendadas sobre el CSV:

- No debe haber filas vacías.
- `total_sales` debe ser mayor o igual a cero.
- El separador decimal es punto (`.`).
- Las fechas usan formato `YYYY-MM-DD`.
- Codificación UTF-8.

### 4.2. Compilar `SalesPredictionApp`

Desde la raíz del repositorio:

```bash
cd SalesPredictionApp
dotnet build
```

> **Nota observada en este entorno**: en algunas máquinas Windows el paso `CreateAppHost` falla con *"The requested operation cannot be performed on a file with a user-mapped section open"* (archivo `.exe` en uso o bloqueado por antivirus). Si ocurre, compilar sin ejecutable nativo:
>
> ```bash
> dotnet build -p:UseAppHost=false
> ```

### 4.3. Ejecutar `SalesPredictionApp`

```bash
cd SalesPredictionApp
dotnet run -p:UseAppHost=false --no-launch-profile
```

Salida esperada:

```text
Iniciando generación de predicciones...
Predicciones generadas exitosamente en: ...\resultados_prediccion.csv
```

El archivo se crea en la raíz del repositorio con las columnas:

```csv
sale_date,product_name,category_name,zone_name,salesman_name,warehouse_name,real_sales,predicted_sales,difference,percentage_error
```

### 4.4. Generar el dashboard HTML

Una vez exista `resultados_prediccion.csv`:

```bash
python dashboard_prediccion.py
```

Esto genera `dashboard_prediccion.html` con:

- KPIs generales (ventas reales vs. predichas, error promedio, R², MAE, RMSE).
- Gráficos de ventas reales vs. predichas por mes.
- Error promedio por mes.
- Predicción por categoría y por zona.
- Top 10 productos con mayor venta estimada.
- Top 10 productos con mayor diferencia entre real y predicho.
- Conclusiones automáticas sobre oportunidades, riesgos y recomendaciones comerciales.

### 4.4. Compilar `SalesPrediction1`

- Requiere Visual Studio con la carga de trabajo de **.NET Framework** y los paquetes NuGet que Model Builder debería haber agregado.
- Antes de compilar, restaurar paquetes NuGet (`Restore NuGet Packages`) y verificar que aparezcan referencias a `Microsoft.ML`, `Microsoft.ML.FastTree` y `Plotly.NET`.
- Como el proyecto utiliza rutas absolutas en `SalesPrediction.training.cs` y `SalesPrediction.mbconfig`, es probable que sea necesario actualizar esas rutas al mover el repositorio a otra máquina.

## 5. Convenciones de estilo

- **Idioma**: comentarios, nombres de columnas y documentación están en español.
- **C#**:
  - `SalesPrediction1` usa estilo clásico: `namespace`, `class Program`, `static void Main(string[] args)`.
  - `SalesPredictionApp` usa **top-level statements** (C# 9+), `ImplicitUsings` habilitado y `Nullable` habilitado.
  - Nombres de clases y métodos en PascalCase.
  - Campos del modelo en `ModelInput` usan PascalCase con prefijos mayúsculas (`Sale_id`, `Total_sales`, etc.).
- **Python**:
  - Comentarios y variables en español.
  - Uso de `f-strings` para formatear códigos.
  - Números formateados con `round(..., 2)`.
- **CSV**:
  - Separador: coma `,`.
  - Decimal: punto `.`.
  - Codificación: UTF-8.
  - En C# se usa `CultureInfo.InvariantCulture` para parsear y formatear valores numéricos.

## 6. Estrategia de pruebas

No hay proyectos de pruebas unitarias. Las validaciones son manuales:

1. **Datos**: abrir `ventas_sinteticas_2025.csv` en Excel y verificar que cumple las reglas del enunciado (estacionalidad, zonas, categorías, sin valores vacíos/negativos).
2. **Compilación**: `dotnet build` debe terminar sin errores (posiblemente usando `-p:UseAppHost=false`).
3. **Ejecución**: `dotnet run` debe crear `resultados_prediccion.csv` con 3.000 filas + encabezado.
4. **Métricas del modelo**: en ML.NET Model Builder revisar R², RMSE y MAE en la pestaña **Evaluar**.
5. **Dashboard HTML**: ejecutar `python dashboard_prediccion.py` debe generar `dashboard_prediccion.html` con todos los KPIs, gráficos y conclusiones solicitadas.
6. **Dashboard Excel/Power BI**: el archivo `.xlsx` o `.pbix` debe comparar real vs. predicho por mes, categoría y zona.

## 7. Consideraciones de seguridad

- **Rutas absolutas**: los archivos `.mbconfig` y `SalesPrediction.training.cs` contienen rutas locales del autor (`G:\My Drive\...`). Esto rompe la portabilidad y expone la estructura de carpetas del usuario original. Deben actualizarse al clonar el proyecto en otro equipo.
- **Datos sintéticos**: no contienen información personal real, por lo que no hay riesgo de PII.
- **Dependencias vulnerables**: `SalesPredictionApp` arrastra transitivamente `Microsoft.Bcl.Memory` versión `9.0.4`, que tiene una vulnerabilidad de severidad alta reportada (`GHSA-73j8-2gch-69rq`). Actualizar los paquetes NuGet cuando haya versiones corregidas.
- **Modelo binario**: `SalesPrediction.mlnet` es un archivo binario serializado. Trátalo como un artefacto de build, no lo edites manualmente.
- **Sin secretos**: no se encontraron credenciales, tokens ni cadenas de conexión en el código.

## 8. Despliegue / entrega

No hay pipelines de CI/CD. La entrega es manual y debe seguir el formato del enunciado:

- Prompt usado para generar la data sintética.
- `ventas_sinteticas_2025.csv`.
- Capturas del proceso de entrenamiento y métricas del modelo.
- `resultados_prediccion.csv` (real vs. predicho).
- Dashboard en `.xlsx` o `.pbix`.
- Documento de conclusiones y recomendaciones.
- Todo comprimido en un `.zip` con el nombre sugerido por el docente.

Opcionalmente, el flujo avanzado propone usar **Supabase** (PostgreSQL en la nube) para almacenar datos y predicciones antes de visualizarlas en Power BI.

## 9. Estado actual y próximos pasos recomendados

- `SalesPredictionApp` compila y ejecuta, pero sus predicciones son **simuladas**. El siguiente paso es entrenar el modelo desde `SalesModel.mbconfig` en Visual Studio, lo que generará `SalesModel.consumption.cs`, `SalesModel.training.cs`, `SalesModel.evaluate.cs` y `SalesModel.mlnet`. Luego se descomenta el bloque de consumo en `Program.cs`.
- `SalesPrediction1` tiene un modelo entrenado pero el proyecto **no compila** por falta de referencias NuGet. Puede servir como referencia del pipeline que generó Model Builder, pero no es la plantilla activa de trabajo.
- El archivo `resultados_prediccion.csv` en la raíz fue generado con la simulación actual; actualízalo después de conectar el modelo real.
