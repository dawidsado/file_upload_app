import pandas as pd
import hashlib
import sys
from pathlib import Path


def short_hash(value: str, length: int = 10) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:length].upper()


def replace_hu_prefix(value: str) -> str:
    if isinstance(value, str) and value.upper().startswith("HU"):
        return "PL" + value[2:]
    return value


def anonymize(input_path: str, output_path: str = None):
    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_anonymized.xlsx"
    else:
        output_path = Path(output_path)

    suffix = input_path.suffix.lower()
    if suffix == ".csv":
        # Wykryj separator automatycznie (przecinek lub srednik)
        with open(input_path, "r", encoding="utf-8", errors="replace") as f:
            sample = f.read(2048)
        sep = ";" if sample.count(";") > sample.count(",") else ","
        print(f"  [info] Wykryto separator CSV: '{sep}'")
        df = pd.read_csv(input_path, dtype=str, sep=sep, encoding="cp1250")
    elif suffix in (".xlsx", ".xls", ".xlsm"):
        df = pd.read_excel(input_path, dtype=str, engine="openpyxl")
    else:
        raise ValueError(f"Nieobslugiwany format pliku: '{suffix}'. Uzyj .csv, .xlsx lub .xls.")

    print(f"  [info] Wczytano {len(df)} wierszy, {len(df.columns)} kolumn.")
    print(f"  [info] Kolumny w pliku: {list(df.columns)}")

    hash_cols = ["MATERIAL", "DOC_NUMBER", "PROFITCENTER", "/BIC/ZE_MAT"]
    hu_cols = {"SALESEMPLY", "SOLD_TO"}

    mappings = {}

    for col in hu_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda v: replace_hu_prefix(v) if isinstance(v, str) else v)
            print(f"  [ok] '{col}' — podmieniono prefix HU→PL.")

    for col in hash_cols:
        if col not in df.columns:
            print(f"  [pominieto] Kolumna '{col}' nie istnieje w pliku.")
            continue

        col_mapping = {}

        def process(val, col=col):
            if pd.isna(val) or str(val).strip() == "":
                return val
            val = str(val).strip()
            if col in hu_cols:
                val = replace_hu_prefix(val)
            if val not in col_mapping:
                col_mapping[val] = short_hash(val)
            return col_mapping[val]

        df[col] = df[col].apply(process)
        mappings[col] = col_mapping
        print(f"  [ok] '{col}' — zanonimizowano {len(col_mapping)} unikalnych wartosci.")

    mapping_rows = []
    for col, mapping in mappings.items():
        for original, hashed in mapping.items():
            mapping_rows.append({
                "Kolumna": col,
                "Oryginalna wartosc": original,
                "Hash (zanonimizowana)": hashed,
            })
    df_mapping = pd.DataFrame(mapping_rows)

    df["LOC_CURRCY"] = "PLN"
    df["PROD_COUNTRY"] = "PL"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Dane", index=False)
        df_mapping.to_excel(writer, sheet_name="Mapowanie", index=False)

        for sheet_name, data in [("Dane", df), ("Mapowanie", df_mapping)]:
            ws = writer.sheets[sheet_name]
            for i, col_name in enumerate(data.columns, 1):
                max_len = max(
                    data[col_name].astype(str).fillna('').map(len).max() if len(data) > 0 else 0,
                    len(str(col_name))
                ) + 3
                ws.column_dimensions[ws.cell(1, i).column_letter].width = min(max_len, 50)

    print(f"\nGotowe! Zapisano do: {output_path}")
    print(f"Arkusz 'Dane'      — zanonimizowane dane")
    print(f"Arkusz 'Mapowanie' — {len(df_mapping)} wpisow (oryginał → hash)")



if __name__ == "__main__":
        input_file = r"C:\Users\A029834\OneDrive - All for One Group SE\Databricks Workshop\Original\BI_SALES_MAR_v1.csv"
        output_file = None  # None = zapisze obok oryginału jako dane_anonymized.xlsx
        anonymize(input_file, output_file)


