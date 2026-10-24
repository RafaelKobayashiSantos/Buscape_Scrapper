
import pandas as pd


def clean_data(dataFrame):
    df = pd.DataFrame(dataFrame).copy()

    if "price" in df.columns:
        df["price"] = (
            df["price"]
            .astype(str)
            .str.replace("R$", "", regex=False)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip()
        )

        df["price"] = pd.to_numeric(df["price"], errors="coerce")

    return df
