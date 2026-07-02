import pandas as pd
from config import EXCEL_NAME

# Function to clean and format the data in the DataFrame
def clean_data(dataFrame):

    df = pd.DataFrame(dataFrame)
    
    df["price"] = (
        df["price"]
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.extract(r"(\d+)")
    )

    # Limpeza e formatação dos dados, incluindo remoção de símbolos, extração de números e tratamento de valores nulos

    df.head() #Exibição dos primeiros registros para verificação
    df.to_excel(EXCEL_NAME, index=False) #Exportação dos dados para um arquivo Excel
    return df