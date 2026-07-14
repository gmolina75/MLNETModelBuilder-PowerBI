<div align="center">

# 📈 MLNETModelBuilder-PowerBI

**Predicción de ventas con ML.NET Model Builder y visualización en Power BI / Excel**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![.NET](https://img.shields.io/badge/.NET-10.0-512BD4?logo=dotnet)](https://dotnet.microsoft.com/)
[![ML.NET](https://img.shields.io/badge/ML.NET-Model%20Builder-green?logo=microsoft)](https://dotnet.microsoft.com/apps/machinelearning-ai/ml-dotnet)
[![Power BI](https://img.shields.io/badge/Power%20BI-Visualización-F2C811?logo=powerbi)](https://powerbi.microsoft.com/)
[![Excel](https://img.shields.io/badge/Excel-Visualización-217346?logo=microsoftexcel)](https://www.microsoft.com/excel)

</div>

---

## 📚 Tabla de contenidos

1. [Resumen ejecutivo](#-resumen-ejecutivo)
2. [Contexto y motivación](#-contexto-y-motivación)
3. [Objetivos de aprendizaje](#-objetivos-de-aprendizaje)
4. [Escenario de negocio](#-escenario-de-negocio)
5. [Arquitectura del proyecto](#-arquitectura-del-proyecto)
6. [Tecnologías utilizadas](#-tecnologías-utilizadas)
7. [Estructura del repositorio](#-estructura-del-repositorio)
8. [Requisitos previos](#-requisitos-previos)
9. [Instalación y configuración](#-instalación-y-configuración)
10. [Generación de datos sintéticos](#-generación-de-datos-sintéticos)
11. [Análisis exploratorio recomendado](#-análisis-exploratorio-recomendado)
12. [Entrenamiento del modelo con ML.NET Model Builder](#-entrenamiento-del-modelo-con-mlnet-model-builder)
13. [Consumo del modelo y predicciones masivas](#-consumo-del-modelo-y-predicciones-masivas)
14. [Evaluación del modelo](#-evaluación-del-modelo)
15. [Visualización en Power BI / Excel](#-visualización-en-power-bi--excel)
16. [Interpretación de resultados de negocio](#-interpretación-de-resultados-de-negocio)
17. [Estado actual del proyecto](#-estado-actual-del-proyecto)
18. [Próximos pasos y mejoras futuras](#-próximos-pasos-y-mejoras-futuras)
19. [Resolución de problemas](#-resolución-de-problemas)
20. [Preguntas frecuentes](#-preguntas-frecuentes)
21. [Glosario](#-glosario)
22. [Recursos y referencias](#-recursos-y-referencias)
23. [Publicación en GitHub](#-publicación-en-github)
24. [Autor y licencia](#-autor-y-licencia)

---

## 📝 Resumen ejecutivo

Este repositorio contiene una **actividad académica completa de Inteligencia de Negocios** cuyo propósito es demostrar, paso a paso, cómo una organización puede construir un pipeline de analítica predictiva con **bajo código**.

El flujo integra cuatro etapas fundamentales:

1. **Ingeniería de datos**: generación de un dataset sintético de ventas con Python.
2. **Modelado predictivo**: entrenamiento de un modelo de regresión con ML.NET Model Builder en Visual Studio.
3. **Consumo del modelo**: generación masiva de predicciones mediante una aplicación de consola en C#.
4. **Visualización y toma de decisiones**: análisis de resultados en Excel o Power BI.

La variable objetivo a predecir es **`total_sales`**, que representa el valor total de cada transacción comercial. El dataset está diseñado para reflejar patrones reales de comportamiento de ventas, incluyendo estacionalidad, preferencias geográficas y variaciones por categoría de producto.

---

## 💡 Contexto y motivación

Las empresas modernas necesitan anticipar la demanda para optimizar inventarios, asignar recursos de ventas, planificar campañas de marketing y mejorar la experiencia del cliente. Sin embargo, muchas organizaciones no cuentan con equipos especializados en ciencia de datos o con presupuesto para contratarlos.

**ML.NET Model Builder** resuelve esta brecha al permitir que desarrolladores, analistas de negocio o estudiantes entrenen modelos de machine learning de forma visual, sin escribir código complejo. Combinado con herramientas de visualización como Excel y Power BI, se obtiene un ecosistema completo de analítica predictiva accesible.

Este proyecto nace como una actividad práctica para que los estudiantes comprendan:

- Cómo se preparan los datos para un modelo de machine learning.
- Cómo se entrena, evalúa y consume un modelo de regresión.
- Cómo se comunican los resultados técnicos en términos de negocio.

---

## 🎯 Objetivos de aprendizaje

Al finalizar esta actividad, el estudiante será capaz de:

- Generar datos sintéticos realistas usando Python y librerías estándar.
- Validar la calidad de un dataset antes de entrenar un modelo.
- Utilizar ML.NET Model Builder para crear un modelo de regresión sin programar el algoritmo manualmente.
- Interpretar métricas de evaluación como R², RMSE y MAE.
- Consumir un modelo entrenado desde una aplicación .NET para realizar predicciones masivas.
- Crear visualizaciones comparativas en Excel o Power BI.
- Formular conclusiones y recomendaciones de negocio basadas en datos.

---

## 🏢 Escenario de negocio

Se simula una empresa comercial ecuatoriana dedicada a la distribución de productos de consumo masivo. La empresa opera en cinco zonas principales del país y comercializa productos de cinco categorías diferentes.

### Dimensiones del negocio

| Dimensión | Valores | Cantidad |
|-----------|---------|----------|
| **Zonas geográficas** | Guayaquil, Quito, Cuenca, Manta, Ambato | 5 |
| **Categorías de producto** | Alimentos, Bebidas, Limpieza, Cuidado Personal, Electrodomésticos | 5 |
| **Productos** | 6 productos por categoría | 30 |
| **Clientes** | Cliente 1 a Cliente 50 | 50 |
| **Vendedores** | Vendedor 1 a Vendedor 8 | 8 |
| **Bodegas** | Bodega Principal, Bodega Norte, Bodega Sur | 3 |
| **Período analizado** | 1 de enero de 2025 al 31 de diciembre de 2025 | 365 días |

### Reglas de generación de datos

El script `generate_synthetic_sales.py` aplica las siguientes reglas para hacer los datos realistas:

- **Estacionalidad**: noviembre y diciembre concentran una mayor proporción de ventas (temporada navideña).
- **Días de la semana**: viernes, sábados y domingos tienen ligeramente mayores volúmenes de venta.
- **Zonas**: Guayaquil y Quito concentran la mayor parte de las transacciones por ser los mercados más grandes.
- **Categorías**: Alimentos y Bebidas son las categorías de mayor rotación, mientras que Electrodomésticos son menos frecuentes pero de mayor valor.
- **Descuentos**: se aplican descuentos aleatorios de 0 %, 5 %, 10 %, 15 % o 20 %.
- **Cálculo de ventas**: `total_sales = quantity × unit_price × (1 − discount_percentage / 100)`.

---

## 🏗️ Arquitectura del proyecto

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FUENTE DE DATOS                             │
│              generate_synthetic_sales.py (Python 3)                 │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DATASET: ventas_sinteticas_2025.csv              │
│              3.000 registros · 18 columnas · UTF-8                  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│              ENTRENAMIENTO: ML.NET Model Builder                    │
│                       (Visual Studio)                               │
│         Escenario: Value prediction · Algoritmo: Regresión          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 MODELO SERIALIZADO: SalesModel.mlnet                │
│         Archivos generados: .consumption.cs, .training.cs           │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│              CONSUMO: SalesPredictionApp (.NET 10)                  │
│          Predicción masiva sobre ventas_sinteticas_2025.csv         │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│              SALIDA: resultados_prediccion.csv                      │
│     real_sales | predicted_sales | difference | percentage_error    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│              VISUALIZACIÓN: Excel o Power BI                        │
│        Dashboards, KPIs y reportes de inteligencia de negocios      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tecnologías utilizadas

### Lenguajes y frameworks

| Tecnología | Versión recomendada | Propósito |
|------------|---------------------|-----------|
| Python | 3.8 o superior | Generación de datos sintéticos |
| C# | 10 o superior | Desarrollo de aplicaciones .NET |
| .NET | 10.0 | Plataforma de ejecución de SalesPredictionApp |
| .NET Framework | 4.8.1 | Plataforma de ejecución de SalesPrediction1 |
| ML.NET | Última estable | Framework de machine learning para .NET |
| ML.NET Model Builder | Última estable | Entrenamiento visual de modelos en Visual Studio |

### Herramientas de desarrollo

| Herramienta | Uso |
|-------------|-----|
| Visual Studio 2022/2026 | IDE principal para C# y ML.NET Model Builder |
| Excel | Visualización básica de datos y resultados |
| Power BI | Visualización avanzada y dashboards interactivos |
| Git | Control de versiones |
| GitHub CLI (`gh`) | Publicación del repositorio en GitHub |

### Librerías Python

Todas las librerías usadas pertenecen a la **librería estándar de Python**, por lo que no se requiere instalar dependencias adicionales:

- `csv`: lectura y escritura de archivos CSV.
- `random`: generación de valores aleatorios con pesos.
- `datetime`: manejo de fechas y cálculo de rangos temporales.

### Paquetes NuGet relevantes

| Paquete | Uso |
|---------|-----|
| `Microsoft.ML` | Núcleo de ML.NET |
| `Microsoft.ML.AutoML` | Entrenamiento automático de modelos |
| `Microsoft.ML.FastTree` | Algoritmo FastForest para regresión |
| `Plotly.NET` | Visualización de métricas (R², residuales) |

---

## 📂 Estructura del repositorio

```
MLNETModelBuilder-PowerBI/
│
├── .vscode/                              # Configuración de Visual Studio Code
│   └── settings.json                     # Preferencias de extensiones
│
├── SalesPrediction1/                     # Proyecto .NET Framework 4.8.1
│   ├── App.config                        # Configuración de la aplicación
│   ├── Program.cs                        # Ejemplo de predicción sobre un registro
│   ├── SalesPrediction1.csproj           # Archivo de proyecto clásico
│   ├── SalesPrediction1.slnx             # Archivo de solución simplificado
│   ├── SalesPrediction.mbconfig          # Configuración de Model Builder
│   ├── SalesPrediction.mlnet             # Modelo entrenado serializado
│   ├── SalesPrediction.consumption.cs    # Clases ModelInput / ModelOutput
│   ├── SalesPrediction.training.cs       # Pipeline de reentrenamiento
│   └── SalesPrediction.evaluate.cs       # Evaluación con PFI y gráficos
│
├── SalesPredictionApp/                   # Proyecto .NET 10 (plantilla activa)
│   ├── Program.cs                        # Lógica de predicciones masivas
│   ├── SalesModel.mbconfig               # Configuración para nuevo entrenamiento
│   ├── SalesPredictionApp.csproj         # Proyecto SDK-style
│   └── SalesPredictionApp.sln            # Solución de Visual Studio
│
├── generate_synthetic_sales.py           # Script de generación de datos
├── ventas_sinteticas_2025.csv            # Dataset de 3.000 registros
├── resultados_prediccion.csv             # Predicciones generadas por la app
│
├── Tarea_Prediccion_Ventas_MLNET_ModelBuilder.docx
├── Guía de instalación de Visual Studio Community 2026 y ML.NET Model Builder.docx
├── Paso a Paso_ Entrenamiento Visual en Visual Studio.docx
│
├── README.md                             # Este archivo
├── .gitignore                            # Archivos excluidos del control de versiones
├── push-to-github.ps1                    # Script de publicación para PowerShell
└── push-to-github.sh                     # Script de publicación para Bash
```

---

## ✅ Requisitos previos

### Software obligatorio

- **Sistema operativo**: Windows 10/11 (ML.NET Model Builder solo funciona en Visual Studio para Windows).
- **Visual Studio 2022 o 2026** con las siguientes cargas de trabajo:
  - Desarrollo de escritorio de .NET
  - Almacenamiento y procesamiento de datos (recomendado)
- **Extensión ML.NET Model Builder** instalada desde el Marketplace de Visual Studio.
- **.NET 10 SDK** para compilar y ejecutar `SalesPredictionApp`.
- **Python 3.8+** si deseas regenerar los datos sintéticos.

### Software recomendado

- **Power BI Desktop** para crear dashboards interactivos.
- **Microsoft Excel 2016 o superior** para visualizaciones básicas.
- **Git** para control de versiones.
- **GitHub CLI (`gh`)** para publicar el repositorio fácilmente.

### Cuentas

- Cuenta de GitHub (solo si vas a publicar el repositorio).
- Cuenta de Microsoft (opcional, para sincronización con OneDrive o Power BI Service).

---

## ⚙️ Instalación y configuración

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/tu-usuario/MLNETModelBuilder-PowerBI.git
cd MLNETModelBuilder-PowerBI
```

O bien descarga el archivo `.zip` y extráelo en tu disco local.

### 2. Verificar Python

```bash
python --version
```

Debe mostrar Python 3.8 o superior.

### 3. Verificar .NET SDK

```bash
dotnet --version
```

Debe mostrar la versión 10.0 o superior para ejecutar `SalesPredictionApp`.

### 4. Verificar Visual Studio

Abre Visual Studio y asegúrate de tener instalada la extensión **ML.NET Model Builder**:

```
Extensión → Administrar extensiones → Instalado → Buscar "ML.NET Model Builder"
```

Si no aparece, instálalo desde el Marketplace oficial de Visual Studio.

---

## 🐍 Generación de datos sintéticos

El script `generate_synthetic_sales.py` genera un archivo CSV con 3.000 registros de ventas que cumplen con las reglas del enunciado académico.

### Ejecutar el generador

Desde la raíz del repositorio:

```bash
python generate_synthetic_sales.py
```

Salida esperada:

```text
Archivo ventas_sinteticas_2025.csv generado exitosamente con 3000 registros.
```

### Características del dataset generado

| Característica | Valor |
|----------------|-------|
| Registros | 3.000 |
| Columnas | 18 |
| Período | 1 de enero de 2025 al 31 de diciembre de 2025 |
| Codificación | UTF-8 |
| Separador | Coma (`,`) |
| Separador decimal | Punto (`.`) |

### Descripción de columnas

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `sale_id` | Texto | Identificador único de la venta (SALE-00001 a SALE-03000) |
| `sale_date` | Fecha | Fecha de la transacción en formato `YYYY-MM-DD` |
| `year_number` | Entero | Año de la venta (2025) |
| `month_number` | Entero | Mes de la venta (1 a 12) |
| `day_number` | Entero | Día del mes (1 a 31) |
| `day_of_week` | Entero | Día de la semana (1 = Lunes, 7 = Domingo) |
| `customer_code` | Texto | Código del cliente (CUST-001 a CUST-050) |
| `customer_name` | Texto | Nombre descriptivo del cliente |
| `product_code` | Texto | Código del producto (PROD-001 a PROD-030) |
| `product_name` | Texto | Nombre descriptivo del producto y categoría |
| `category_name` | Texto | Categoría del producto |
| `zone_name` | Texto | Zona geográfica de la venta |
| `salesman_name` | Texto | Vendedor responsable |
| `warehouse_name` | Texto | Bodega desde donde se despachó |
| `quantity` | Entero | Cantidad de unidades vendidas |
| `unit_price` | Decimal | Precio unitario del producto |
| `discount_percentage` | Entero | Porcentaje de descuento aplicado (0, 5, 10, 15, 20) |
| `total_sales` | Decimal | Valor total de la venta después del descuento |

### Validaciones de calidad incluidas en el generador

- Identificadores únicos para cada venta.
- Fechas dentro del rango válido.
- Cálculo correcto de `total_sales`.
- Distribución ponderada de zonas, productos y categorías.
- Efecto estacional en noviembre y diciembre.
- Mayor volumen de ventas en fines de semana.

---

## 🔍 Análisis exploratorio recomendado

Antes de entrenar el modelo, se recomienda realizar un análisis exploratorio de datos (EDA) en Excel o Python. Algunas preguntas útiles:

1. ¿Cuál es el mes con mayores ventas? ¿Se confirma el pico de noviembre/diciembre?
2. ¿Qué categoría genera más ingresos totales?
3. ¿Qué zona tiene el mayor ticket promedio?
4. ¿Existen outliers en `total_sales`? ¿Corresponden a electrodomésticos?
5. ¿Cómo se distribuyen los descuentos a lo largo del año?

### Ejemplo de análisis rápido con Python

```python
import pandas as pd

df = pd.read_csv("ventas_sinteticas_2025.csv")

# Ventas por mes
print(df.groupby("month_number")["total_sales"].sum().sort_index())

# Ventas por categoría
print(df.groupby("category_name")["total_sales"].sum().sort_values(ascending=False))

# Estadísticas descriptivas
print(df["total_sales"].describe())
```

---

## 🤖 Entrenamiento del modelo con ML.NET Model Builder

ML.NET Model Builder es una extensión visual de Visual Studio que automatiza el proceso de selección de algoritmos, ajuste de hiperparámetros y evaluación de modelos.

### Pasos detallados

#### 1. Abrir la solución

Abre `SalesPredictionApp/SalesPredictionApp.sln` en Visual Studio.

#### 2. Agregar un modelo de Machine Learning

1. Haz clic derecho sobre el proyecto `SalesPredictionApp`.
2. Selecciona **Agregar → Machine Learning Model**.
3. Asigna el nombre `SalesModel` y presiona **Agregar**.

#### 3. Seleccionar el escenario

En la ventana de Model Builder, elige **Value prediction** (Predicción de valores). Esto configura el problema como una **regresión**.

#### 4. Cargar los datos

1. Selecciona **File** como origen de datos.
2. Busca y selecciona `ventas_sinteticas_2025.csv`.
3. En la lista desplegable **Column to predict (Label)**, selecciona `total_sales`.

#### 5. Configurar el entrenamiento

1. Selecciona **Train locally**.
2. Define el tiempo de entrenamiento. Se recomienda **60 segundos** para este dataset.
3. Opcionalmente, habilita la validación cruzada con 5 folds.
4. Haz clic en **Start training**.

Model Builder probará automáticamente varios algoritmos (SDCA, FastTree, LightGBM, FastForest, etc.) y seleccionará el de mejor rendimiento.

#### 6. Revisar métricas

Una vez finalizado el entrenamiento, revisa la pestaña **Evaluate**:

| Métrica | Nombre completo | Interpretación |
|---------|-----------------|----------------|
| **R²** | Coeficiente de determinación | Valor entre 0 y 1. Cuanto más cercano a 1, mejor explica el modelo la variabilidad de los datos. |
| **RMSE** | Root Mean Squared Error | Error promedio en las mismas unidades del target. Penaliza más los errores grandes. |
| **MAE** | Mean Absolute Error | Error promedio absoluto. Más robusto ante outliers que RMSE. |

En el proyecto de referencia `SalesPrediction1`, el mejor modelo fue **FastForestRegression** con R² ≈ 0.904.

#### 7. Guardar el modelo

Haz clic en **Add to solution**. Model Builder generará los siguientes archivos:

- `SalesModel.mbconfig`: configuración del entrenamiento.
- `SalesModel.mlnet`: modelo serializado.
- `SalesModel.consumption.cs`: clases `ModelInput`, `ModelOutput` y método `Predict()`.
- `SalesModel.training.cs`: pipeline y método `Train()` para reentrenar.
- `SalesModel.evaluate.cs`: funciones de evaluación avanzada.

---

## 🚀 Consumo del modelo y predicciones masivas

El proyecto `SalesPredictionApp` está preparado para consumir el modelo generado y producir un archivo CSV comparativo.

### Estado actual

Actualmente, `Program.cs` genera predicciones **simuladas** dentro de ±5 % del valor real. Esto permite probar el pipeline de lectura/escritura CSV sin necesidad de un modelo entrenado.

### Conectar el modelo real

1. Abre `SalesPredictionApp/Program.cs`.
2. Busca el bloque comentado que utiliza `SalesModel.ModelInput`.
3. Descomenta ese bloque.
4. Elimina o comenta el bloque de simulación con `Random`.

El código de consumo típico se ve así:

```csharp
var input = new SalesModel.ModelInput
{
    Month_number = month,
    Day_number = day,
    Day_of_week = dayOfWeek,
    Category_name = category,
    Zone_name = zone,
    Salesman_name = salesman,
    Warehouse_name = warehouse,
    Quantity = quantity,
    Unit_price = unitPrice,
    Discount_percentage = discount
};

var prediction = SalesModel.Predict(input);
float predictedSales = prediction.Score;
```

### Compilar

```bash
cd SalesPredictionApp
dotnet build
```

> **Nota**: Si recibes el error *"The requested operation cannot be performed on a file with a user-mapped section open"*, el ejecutable `apphost.exe` está bloqueado por otro proceso. Usa:
> ```bash
> dotnet build -p:UseAppHost=false
> ```

### Ejecutar

```bash
dotnet run -p:UseAppHost=false --no-launch-profile
```

Salida esperada:

```text
Iniciando generación de predicciones...
Predicciones generadas exitosamente en: G:\...\resultados_prediccion.csv
```

### Estructura del archivo de salida

```csv
sale_date,product_name,category_name,zone_name,salesman_name,warehouse_name,real_sales,predicted_sales,difference,percentage_error
2025-01-15,Producto Alimentos 3,Alimentos,Guayaquil,Vendedor 2,Bodega Principal,45.60,44.12,-1.48,-3.25
```

---

## 📊 Evaluación del modelo

### Métricas principales

#### R² (Coeficiente de determinación)

Mide qué proporción de la varianza de `total_sales` es explicada por el modelo.

- **R² = 1**: predicción perfecta.
- **R² = 0**: el modelo no explica nada mejor que la media.
- **R² < 0**: el modelo es peor que simplemente predecir el promedio.

En este proyecto, un R² de 0.90 indica que el modelo explica aproximadamente el 90 % de la variabilidad de las ventas.

#### RMSE (Root Mean Squared Error)

```
RMSE = √(promedio de los errores al cuadrado)
```

Representa el error típico en dólares. Es sensible a outliers porque penaliza los errores grandes.

#### MAE (Mean Absolute Error)

```
MAE = promedio(|real − predicho|)
```

Representa el error absoluto promedio. Es más interpretable que RMSE cuando hay valores atípicos.

### Consideraciones especiales de este dataset

Como `total_sales` se calcula directamente a partir de `quantity`, `unit_price` y `discount_percentage`, el modelo puede aprender la fórmula en lugar de patrones de demanda. Para evitar este **data leakage**, se recomienda una de estas estrategias:

1. **Estrategia A**: predecir `quantity` usando variables de contexto (mes, categoría, zona, etc.) y calcular `total_sales` posteriormente.
2. **Estrategia B**: entrenar para predecir `total_sales` pero excluyendo `unit_price` y `discount_percentage` como features.

---

## 📈 Visualización en Power BI / Excel

Una vez generado `resultados_prediccion.csv`, puedes crear visualizaciones para comunicar los hallazgos.

### Visualizaciones recomendadas

1. **Real vs. Predicho por mes**
   - Tipo: Gráfico de líneas o columnas agrupadas.
   - Eje X: `sale_date` agrupado por mes.
   - Eje Y: suma de `real_sales` y `predicted_sales`.

2. **Error porcentual promedio por categoría**
   - Tipo: Gráfico de barras.
   - Eje X: `category_name`.
   - Eje Y: promedio de `percentage_error`.

3. **Diferencia absoluta por zona**
   - Tipo: Mapa de árbol o barras.
   - Eje X: `zone_name`.
   - Eje Y: promedio de `difference`.

4. **Dispersión Real vs. Predicho**
   - Tipo: Gráfico de dispersión.
   - Eje X: `real_sales`.
   - Eje Y: `predicted_sales`.
   - Incluir línea de referencia y = x.

5. **Distribución del error**
   - Tipo: Histograma.
   - Campo: `percentage_error`.

### Ejemplo de KPIs

| KPI | Fórmula | Interpretación |
|-----|---------|----------------|
| MAPE | `PROMEDIO(ABS(percentage_error))` | Error porcentual medio |
| Sesgo | `PROMEDIO(predicted_sales − real_sales)` | Si es positivo, el modelo sobrestima |
| Cobertura | `% de predicciones con error < 10%` | Precisión operativa |

---

## 💼 Interpretación de resultados de negocio

Al analizar las predicciones, intenta responder preguntas como:

- ¿En qué meses el modelo tiene mayor error? ¿Coincide con campañas o festividades?
- ¿Qué categorías son más predecibles?
- ¿Existen zonas donde el modelo sistemáticamente subestima o sobrestima?
- ¿Los descuentos afectan la precisión del modelo?
- ¿Qué acciones operativas se pueden tomar con estas predicciones?

### Ejemplo de recomendaciones

1. **Inventario**: aumentar stock de alimentos y bebidas en noviembre/diciembre.
2. **Fuerza de ventas**: asignar más vendedores a Guayaquil y Quito en temporada alta.
3. **Promociones**: evaluar el impacto real de descuentos sobre el volumen de ventas.
4. **Bodegas**: optimizar distribución entre Bodega Principal, Norte y Sur según la demanda pronosticada.

---

## 🚧 Estado actual del proyecto

| Componente | Estado | Detalle |
|------------|--------|---------|
| Dataset sintético | ✅ Completo | 3.000 registros validados |
| `SalesPrediction1` | ⚠️ Referencia | Modelo entrenado, pero faltan referencias NuGet para compilar |
| `SalesPredictionApp` | ⚠️ En desarrollo | Compila, pero usa predicciones simuladas |
| `resultados_prediccion.csv` | ⚠️ Simulado | Generado con valores aleatorios ±5 % |
| Documentación académica | ✅ Completa | Archivos `.docx` incluidos |
| Dashboard Excel/Power BI | ❌ Pendiente | Debe crearlo el estudiante |
| README.md | ✅ Completo | Este archivo |

---

## 🔮 Próximos pasos y mejoras futuras

### Inmediatos

1. Entrenar el modelo desde `SalesModel.mbconfig` en Visual Studio.
2. Conectar el modelo real en `SalesPredictionApp/Program.cs`.
3. Regenerar `resultados_prediccion.csv` con predicciones reales.
4. Crear el dashboard en Excel o Power BI.

### Avanzados

- Implementar una API REST con ASP.NET Core para servir predicciones.
- Almacenar datos y predicciones en una base de datos como Supabase (PostgreSQL).
- Automatizar el reentrenamiento periódico del modelo.
- Crear pruebas unitarias para la lógica de predicción.
- Implementar logging estructurado con Serilog.
- Publicar el modelo como un servicio en la nube.

---

## 🛠️ Resolución de problemas

### El proyecto `SalesPrediction1` no compila

**Síntoma**: errores del tipo `The type or namespace name 'ML' does not exist`.

**Causa**: faltan referencias a paquetes NuGet.

**Solución**:

1. Abre `SalesPrediction1` en Visual Studio.
2. Ve a `Herramientas → Administrador de paquetes NuGet → Administrar paquetes NuGet para la solución`.
3. Instala los paquetes:
   - `Microsoft.ML`
   - `Microsoft.ML.FastTree`
   - `Plotly.NET`
4. Restaura los paquetes y recompila.

### Error "user-mapped section open" al compilar `SalesPredictionApp`

**Síntoma**: falla la tarea `CreateAppHost`.

**Causa**: el archivo `apphost.exe` está bloqueado por Visual Studio o antivirus.

**Solución**:

```bash
dotnet build -p:UseAppHost=false
```

### Las predicciones son idénticas al valor real

**Causa**: el modelo está usando `unit_price` y `discount_percentage` como features, por lo que aprende la fórmula exacta.

**Solución**: excluye esas columnas del entrenamiento o cambia el target a `quantity`.

### No se encuentra `ventas_sinteticas_2025.csv`

**Causa**: la ruta relativa en `Program.cs` no coincide con la ubicación actual.

**Solución**: ejecuta la aplicación desde la carpeta `SalesPredictionApp` o ajusta la ruta en el código.

### Error de codificación al abrir CSV en Excel

**Solución**: abre Excel, ve a `Datos → Obtener datos → Desde archivo → Desde texto/CSV` y selecciona codificación UTF-8.

---

## ❓ Preguntas frecuentes

### ¿Puedo usar este proyecto con Visual Studio Code?

ML.NET Model Builder **solo está disponible en Visual Studio para Windows**. Sin embargo, puedes editar el código C# y ejecutar `dotnet build`/`dotnet run` desde VS Code una vez generados los archivos del modelo.

### ¿Es necesario saber programar en C# para usar Model Builder?

No. Model Builder genera automáticamente el código necesario. Solo necesitas conocimientos básicos de C# para consumir el modelo en tu aplicación.

### ¿Puedo usar otro algoritmo diferente a FastForest?

Sí. Model Builder prueba varios algoritmos automáticamente, pero también puedes seleccionar manualmente el algoritmo en la configuración avanzada.

### ¿Los datos son reales?

No. Todos los datos son sintéticos y generados aleatoriamente con reglas de negocio realistas.

### ¿Puedo aumentar la cantidad de registros?

Sí. Modifica la variable `num_records` en `generate_synthetic_sales.py` y vuelve a ejecutar el script.

### ¿Por qué hay dos proyectos de C#?

- `SalesPrediction1` es una referencia con un modelo ya entrenado.
- `SalesPredictionApp` es la plantilla que debe completar el estudiante para generar predicciones masivas.

---

## 📖 Glosario

| Término | Definición |
|---------|------------|
| **Machine Learning** | Rama de la inteligencia artificial que permite a las computadoras aprender patrones a partir de datos. |
| **Regresión** | Tipo de problema de ML donde el objetivo es predecir un valor numérico continuo. |
| **Feature** | Variable de entrada utilizada por el modelo para realizar predicciones. |
| **Label** | Variable objetivo que el modelo intenta predecir. En este proyecto es `total_sales`. |
| **R²** | Métrica que indica qué tan bien el modelo explica la variabilidad de los datos. |
| **RMSE** | Raíz del error cuadrático medio. Mide el error típico del modelo. |
| **MAE** | Error absoluto medio. Mide el error promedio sin considerar la dirección. |
| **One-Hot Encoding** | Técnica para convertir variables categóricas en valores numéricos binarios. |
| **Data Leakage** | Cuando información del futuro o del target se filtra hacia las features, produciendo un modelo sobreoptimista. |
| **Validación cruzada** | Técnica para evaluar el modelo dividiendo los datos en varios subconjuntos y entrenando/validando en cada uno. |

---

## 📚 Recursos y referencias

- [Documentación oficial de ML.NET](https://docs.microsoft.com/dotnet/machine-learning/)
- [ML.NET Model Builder](https://dotnet.microsoft.com/apps/machinelearning-ai/ml-dotnet/model-builder)
- [Tutorial: Predecir precios con ML.NET](https://docs.microsoft.com/dotnet/machine-learning/tutorials/predict-prices-with-model-builder)
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/)
- [Visual Studio 2022](https://visualstudio.microsoft.com/vs/)
- [.NET 10 SDK](https://dotnet.microsoft.com/download)

---

## 🚀 Publicación en GitHub

Este repositorio incluye scripts automatizados para publicar el proyecto en GitHub.

### Requisitos

- Git instalado.
- GitHub CLI (`gh`) instalado y autenticado:
  ```bash
  gh auth login
  ```

### PowerShell

```powershell
.\push-to-github.ps1 -RepoName "MLNET-Prediccion-Ventas" -Visibility public
```

### Bash

```bash
./push-to-github.sh --repo-name MLNET-Prediccion-Ventas --visibility public
```

Ambos scripts:

- Inicializan el repositorio Git local.
- Crean el `.gitignore` adecuado.
- Eliminan archivos temporales.
- Crean el repositorio remoto en GitHub.
- Realizan el commit y push iniciales.

---

## 👨‍🏫 Autor y licencia

**Autor**: Proyecto académico desarrollado para la asignatura de **Inteligencia de Negocios** en **Ecotec**.

**Propósito**: Material educativo para el aprendizaje de machine learning aplicado a negocios con herramientas de bajo código.

> ⚠️ **Aviso legal**: Los datos de este proyecto son completamente sintéticos y no contienen información personal real. Cualquier parecido con datos reales es pura coincidencia.

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera compartirlo con tus compañeros.**

</div>
