import pandas as pd
from pathlib import Path

def quick_dict(df: pd.DataFrame, name: str):
    rows = []
    for col in df.columns:
        s = df[col]
        dtype = str(s.dtype)
        n_missing = int(s.isna().sum())
        n_unique = int(s.nunique(dropna=True))
        example = s.dropna().iloc[0] if s.dropna().size else ""
        rows.append({
            "dataset": name,
            "field": col,
            "dtype_inferred": dtype,
            "n_missing": n_missing,
            "n_unique": n_unique,
            "example_value": example
        })
    return pd.DataFrame(rows)


base = Path(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean")
crime = pd.read_csv(base / "CrimeClean_LGA_CrimeCounts.csv")
liquor = pd.read_csv(base / "LiquorLicenseClean_LGA_Counts.csv")
hosp  = pd.read_csv(base / "HospitalisationsClean.csv")
combo = pd.read_csv(base / "Combined_Crime_Liquor_Hosp.csv")

out = pd.concat([
    quick_dict(crime, "Crime"),
    quick_dict(liquor, "Liquor"),
    quick_dict(hosp,  "Hospitalisations"),
    quick_dict(combo, "Combined")
], ignore_index=True)

out = out[["dataset","field","dtype_inferred","n_missing","n_unique","example_value"]]
out.to_csv(base / "DataDictionary_Auto.csv", index=False)
print("Wrote:", base / "DataDictionary_Auto.csv")

import pandas as pd
from pathlib import Path
import re

RAW_DIR  = Path(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Raw")
OUT_DIR  = Path(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean")  # where to write the dict CSVs
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_any(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    # CSV fallbacks
    try:
        return pd.read_csv(path, low_memory=False)
    except UnicodeDecodeError:
        # if encoding issues
        return pd.read_csv(path, low_memory=False, encoding="latin-1")

MONTH_RE = re.compile(r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+20\d{2}$")

def is_month_col(colname: str) -> bool:
    return bool(MONTH_RE.match(str(colname)))

def summarize_series(s: pd.Series) -> dict:
    # Basic
    name = s.name
    dtype = str(s.dtype)
    n = int(len(s))
    n_missing = int(s.isna().sum())


    s_num = pd.to_numeric(s, errors="coerce")
    is_numeric_like = s_num.notna().sum() > 0 and (s.dtype.kind in "biufc" or s_num.notna().mean() > 0.5)


    out = {
        "field": name,
        "dtype_inferred": dtype,
        "n_rows": n,
        "n_missing": n_missing,
        "pct_missing": round((n_missing / n) * 100, 2) if n else 0.0,
        "is_month_col": is_month_col(str(name)),
    }

    if is_numeric_like:
        n_zero = int((s_num == 0).sum())
        n_negative = int((s_num < 0).sum())
        out.update({
            "n_zero": n_zero,
            "pct_zero": round((n_zero / n) * 100, 2) if n else 0.0,
            "n_negative": n_negative,
            "min": float(s_num.min()) if s_num.notna().any() else None,
            "max": float(s_num.max()) if s_num.notna().any() else None,
            "mean": float(s_num.mean()) if s_num.notna().any() else None,
            "std": float(s_num.std(ddof=1)) if s_num.notna().sum() > 1 else None,
            "example_value": s_num.dropna().iloc[0] if s_num.notna().any() else "",
        })
    else:

        vc = s.astype("string", errors="ignore").value_counts(dropna=True)
        topk = vc.head(5).to_dict()
        topk_str = "; ".join(f"{k}:{v}" for k, v in topk.items())
        out.update({
            "n_unique": int(s.nunique(dropna=True)),
            "top_values": topk_str,
            "example_value": (s.dropna().astype(str).iloc[0] if s.dropna().size else ""),
        })

    return out

def make_raw_data_dictionary(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    rows = [summarize_series(df[col]) for col in df.columns]
    dd = pd.DataFrame(rows)
    dd.insert(0, "dataset", dataset_name)
    # Friendly order
    cols_order = [
        "dataset","field","dtype_inferred","n_rows","n_missing","pct_missing",
        "is_month_col","n_unique","n_zero","pct_zero","n_negative",
        "min","max","mean","std","top_values","example_value"
    ]
    # keep only present columns + preserve order
    dd = dd[[c for c in cols_order if c in dd.columns]]
    return dd

# Scan RAW_DIR for files
raw_files = sorted([p for p in RAW_DIR.rglob("*") if p.suffix.lower() in (".csv", ".xlsx", ".xls")])

all_dd = []
for fp in raw_files:
    try:
        df_raw = load_any(fp)
        dataset_name = fp.stem  # filename without extension
        dd = make_raw_data_dictionary(df_raw, dataset_name)
        # write a per-dataset dictionary
        per_out = OUT_DIR / f"DataDictionary_Raw_{dataset_name}.csv"
        dd.to_csv(per_out, index=False)
        print(f"Wrote: {per_out}")
        all_dd.append(dd)
    except Exception as e:
        print(f"[WARN] Skipped {fp.name}: {e}")

# Combined dictionary across all raw files
if all_dd:
    combined = pd.concat(all_dd, ignore_index=True)
    combined_out = OUT_DIR / "DataDictionary_Raw_ALL.csv"
    combined.to_csv(combined_out, index=False)
    print(f"Wrote: {combined_out}")
else:
    print("No raw files found or all failed to parse.")