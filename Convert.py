import csv
import re
import sys

MONTH_MAP = {
    'sty': 1, 'lut': 2, 'mar': 3, 'kwi': 4,
    'maj': 5, 'cze': 6, 'lip': 7, 'sie': 8,
    'wrz': 9, 'paź': 10, 'paz': 10, 'lis': 11, 'gru': 12
}

def fix_date_to_number(val):
    """Convert Polish date like '01.maj' back to decimal like '1.5'"""
    val = val.strip()
    m = re.match(r'^(\d{1,2})[.\-/](\w+)$', val)
    if m:
        day = m.group(1)
        month_str = m.group(2).lower()
        if month_str in MONTH_MAP:
            return f"{int(day)}.{MONTH_MAP[month_str]}"
    return val

def zero_pad(val):
    """Pad single digits to two digits: 1 -> 01, 2 -> 02"""
    val = val.strip()
    if re.match(r'^\d{1,2}$', val):
        return val.zfill(2)
    return val

# === KONFIGURACJA ===
# Wpisz ścieżkę do pliku wejściowego i wyjściowego
input_file = r'C:\EnerSys Files\Intake as file 1.csv'
output_file = r'C:\EnerSys Files\Intake as file 1.csv'

with open(input_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=';')
    rows = list(reader)

header = rows[0]
pad_cols = {'DISTRIBUTIONCHAN', 'DIVISION'}
quantity_col = 'ORDERQUANTITY'

pad_indices = [i for i, h in enumerate(header) if h in pad_cols]
qty_index = next((i for i, h in enumerate(header) if h == quantity_col), None)

for row in rows[1:]:
    for idx in pad_indices:
        row[idx] = zero_pad(row[idx])
    if qty_index is not None:
        row[qty_index] = fix_date_to_number(row[qty_index])

with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerows(rows)

print("Done. Fixed rows:", len(rows) - 1)