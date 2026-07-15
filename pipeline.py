import pandas as pd
import json
from config import EXCEL_NAME

# Function to clean and format the data in the DataFrame
def clean_data(dataFrame, price_historic):

    df = pd.DataFrame(dataFrame)
    price_historic = pd.DataFrame(price_historic)
    
    df["price"] = (
        df["price"]
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.extract(r"(\d+)")
    )
    # Limpeza e formatação dos dados, incluindo remoção de símbolos, extração de números e tratamento de valores nulos
    
    df.to_excel(EXCEL_NAME, index=False) #Exportação dos dados para um arquivo Excel
    
    price_historic.to_json('price_historic/best_values_historic.json', orient='records', indent=4) #Exportação do histórico de preços para um arquivo JSON

    return df