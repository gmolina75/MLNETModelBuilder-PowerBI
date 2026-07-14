using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SalesPredict
{
    internal class Program
    {
        static void Main(string[] args)
        {
            //Load sample data
            var sampleData = new SalesPredict.ModelInput()
            {
                Sale_id = @"SALE-00534",
                Sale_date = @"2025-01-01",
                Year_number = 2025F,
                Month_number = 1F,
                Day_number = 1F,
                Day_of_week = 3F,
                Customer_code = @"CUST-031",
                Customer_name = @"Cliente 31",
                Product_code = @"PROD-023",
                Product_name = @"Producto Cuidado Personal 5",
                Category_name = @"Cuidado Personal",
                Zone_name = @"Guayaquil",
                Salesman_name = @"Vendedor 6",
                Warehouse_name = @"Bodega Sur",
                Quantity = 18F,
                Unit_price = 11.25F,
                Discount_percentage = 0F,
            };

            //Load model and predict output
            var result = SalesPredict.Predict(sampleData);

        }
    }
}
