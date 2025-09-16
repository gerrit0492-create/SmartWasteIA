from __future__ import annotations
import pandas as pd
import numpy as np

def _lookup(df: pd.DataFrame, key_col: str, key, value_col: str, default=None):
    m = df.loc[df[key_col] == key]
    return (m[value_col].values[0] if not m.empty else default)

def compute_material_qty(row, materials_df):
    # If material_qty provided (>0), use it; else derive naive estimate from geometry
    q = float(row.get("material_qty", 0) or 0)
    if q > 0:
        return q
    # Derive kg from area_cm2 * thickness_mm * density
    mat = row.get("material_code", "")
    density = _lookup(materials_df, "material_code", mat, "density_kg_m3", 7800)
    area_cm2 = float(row.get("area_cm2", 0) or 0)
    th_mm = float(row.get("thickness_mm", 0) or 0)
    vol_m3 = (area_cm2 * 1e-4) * (th_mm / 1000.0)  # cm^2 -> m^2, mm -> m
    kg = density * vol_m3
    return kg

def compute_costs(bom_df: pd.DataFrame, materials_df: pd.DataFrame,
                  machines_df: pd.DataFrame, labor_df: pd.DataFrame,
                  logistics_df: pd.DataFrame) -> pd.DataFrame:
    df = bom_df.copy()
    # Normalize NaNs
    for c in ["unit_price_eur","process_time_min_machine","process_time_min_labor","markup_pct"]:
        if c in df.columns:
            df[c] = df[c].fillna(0)
    # Material price lookup if not given
    df["material_qty_calc_kg"] = df.apply(lambda r: compute_material_qty(r, materials_df), axis=1)
    df["material_eur_per_kg"] = df.apply(
        lambda r: r["unit_price_eur"] if float(r.get("unit_price_eur",0) or 0) > 0
        else _lookup(materials_df, "material_code", r.get("material_code",""), "eur_per_kg", 0.0), axis=1)
    df["material_cost"] = df["qty"] * df["material_qty_calc_kg"] * df["material_eur_per_kg"]

    # Machine cost
    df["machine_rate_eur_h"] = df.apply(lambda r:
        _lookup(machines_df, "machine_code", r.get("machine_code",""), "rate_eur_per_hour", 0.0), axis=1)
    df["machine_setup_min"] = df.apply(lambda r:
        _lookup(machines_df, "machine_code", r.get("machine_code",""), "setup_min", 0.0), axis=1)
    # Per part share of setup (simple: setup divided by batch = qty)
    df["machine_time_total_min"] = df["process_time_min_machine"] + (df["machine_setup_min"] / df["qty"].replace(0,1))
    df["machine_cost"] = (df["machine_time_total_min"]/60.0) * df["machine_rate_eur_h"] * df["qty"]

    # Labor cost
    df["labor_rate_eur_h"] = df.apply(lambda r:
        _lookup(labor_df, "labor_grade", r.get("labor_grade",""), "rate_eur_per_hour", 0.0), axis=1)
    df["labor_cost"] = (df["process_time_min_labor"]/60.0) * df["labor_rate_eur_h"] * df["qty"]

    # Logistics (use flat default)
    if "default" in logistics_df.columns:
        default_row = logistics_df.loc[logistics_df["default"]==True].head(1)
        flat = float(default_row["eur_flat"].values[0]) if not default_row.empty else 0.0
    else:
        flat = 0.0
    df["logistics_cost"] = 0.0
    if len(df) > 0:
        df.loc[df.index[0],"logistics_cost"] = flat  # charge once per BOM for demo

    # Subtotals
    df["sub_total"] = df["material_cost"] + df["machine_cost"] + df["labor_cost"] + df["logistics_cost"]

    # Markup
    df["markup_pct"] = df["markup_pct"].fillna(0)
    df["markup_amount"] = df["sub_total"] * (df["markup_pct"]/100.0)
    df["total_line"] = df["sub_total"] + df["markup_amount"]

    return df

def summarize(df: pd.DataFrame) -> dict:
    out = {}
    out["lines"] = len(df)
    out["qty_total"] = float(df["qty"].sum())
    out["material_cost"] = float(df["material_cost"].sum())
    out["machine_cost"] = float(df["machine_cost"].sum())
    out["labor_cost"] = float(df["labor_cost"].sum())
    out["logistics_cost"] = float(df["logistics_cost"].sum())
    out["margin"] = float(df["markup_amount"].sum())
    out["grand_total"] = float(df["total_line"].sum())
    return out
