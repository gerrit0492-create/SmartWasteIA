from __future__ import annotations
import pandas as pd
import numpy as np
from .process_models import estimate_machine_minutes

def _lookup(df: pd.DataFrame, key_col: str, key, value_col: str, default=None):
    m = df.loc[df[key_col] == key]
    return (m[value_col].values[0] if not m.empty else default)

def compute_material_qty(row, materials_df):
    q = float(row.get("material_qty", 0) or 0)
    if q > 0:
        return q
    # Derive kg from geometry if possible
    mat = row.get("material_code", "")
    density = _lookup(materials_df, "material_code", mat, "density_kg_m3", 7800)
    area_cm2 = float(row.get("area_cm2", 0) or 0)
    th_mm = float(row.get("thickness_mm", 0) or 0)
    length_mm = float(row.get("length_mm", 0) or 0)
    diameter_mm = float(row.get("diameter_mm", 0) or 0)

    vol_m3 = 0.0
    if area_cm2 > 0 and th_mm > 0:
        vol_m3 = (area_cm2 * 1e-4) * (th_mm / 1000.0)  # plate
    elif diameter_mm > 0 and length_mm > 0:
        import math
        r = (diameter_mm / 1000.0) / 2.0
        vol_m3 = math.pi * r * r * (length_mm / 1000.0)  # round bar
    kg = density * vol_m3
    return kg

def compute_costs(bom_df: pd.DataFrame, materials_df: pd.DataFrame,
                  machines_df: pd.DataFrame, labor_df: pd.DataFrame,
                  logistics_df: pd.DataFrame) -> pd.DataFrame:
    df = bom_df.copy()
    for c in ["unit_price_eur","process_time_min_machine","process_time_min_labor","markup_pct","qty"]:
        if c in df.columns:
            df[c] = df[c].fillna(0)
    # Material price / qty
    df["material_qty_calc_kg"] = df.apply(lambda r: compute_material_qty(r, materials_df), axis=1)
    df["material_eur_per_kg"] = df.apply(
        lambda r: r["unit_price_eur"] if float(r.get("unit_price_eur",0) or 0) > 0
        else _lookup(materials_df, "material_code", r.get("material_code",""), "eur_per_kg", 0.0), axis=1)
    df["material_waste_pct"] = df.apply(
        lambda r: _lookup(materials_df, "material_code", r.get("material_code",""), "waste_pct", 0.05), axis=1)
    df["material_cost"] = df["qty"] * df["material_qty_calc_kg"] * (1+df["material_waste_pct"]) * df["material_eur_per_kg"]

    # Machine time
    df["machine_rate_eur_h"] = df.apply(lambda r:
        _lookup(machines_df, "machine_code", r.get("machine_code",""), "rate_eur_per_hour", 0.0), axis=1)
    df["machine_setup_min"] = df.apply(lambda r:
        _lookup(machines_df, "machine_code", r.get("machine_code",""), "setup_min", 0.0), axis=1)

    # If no machine time given, estimate
    df["machine_time_est_min"] = df.apply(lambda r: estimate_machine_minutes(r, machines_df), axis=1)
    df["machine_time_total_min"] = df[["process_time_min_machine","machine_time_est_min"]].max(axis=1) + (df["machine_setup_min"] / df["qty"].replace(0,1))
    df["machine_cost"] = (df["machine_time_total_min"]/60.0) * df["machine_rate_eur_h"] * df["qty"]

    # Labor
    df["labor_rate_eur_h"] = df.apply(lambda r:
        _lookup(labor_df, "labor_grade", r.get("labor_grade",""), "rate_eur_per_hour", 0.0), axis=1)
    df["labor_cost"] = (df["process_time_min_labor"]/60.0) * df["labor_rate_eur_h"] * df["qty"]

    # Welding consumables simple factor if welding process
    df["consumables_cost"] = 0.0
    df.loc[df["machine_code"].str.contains("WELD", na=False), "consumables_cost"] = 0.08 * df["labor_cost"]

    # Logistics (flat once per BOM)
    flat = 0.0
    if "default" in logistics_df.columns:
        default_row = logistics_df.loc[logistics_df["default"]==True].head(1)
        flat = float(default_row["eur_flat"].values[0]) if not default_row.empty else 0.0
    if len(df) > 0:
        df.loc[df.index[0],"logistics_cost"] = flat
    else:
        df["logistics_cost"] = 0.0

    # Subtotal + markup
    df["sub_total"] = df["material_cost"] + df["machine_cost"] + df["labor_cost"] + df["consumables_cost"] + df["logistics_cost"]
    df["markup_pct"] = df["markup_pct"].fillna(0)
    df["markup_amount"] = df["sub_total"] * (df["markup_pct"]/100.0)
    df["total_line"] = df["sub_total"] + df["markup_amount"]

    return df

def summarize(df: pd.DataFrame) -> dict:
    if df is None or len(df)==0:
        return {"lines": 0, "qty_total": 0.0, "material_cost": 0.0, "machine_cost": 0.0, "labor_cost": 0.0, "consumables_cost": 0.0, "logistics_cost": 0.0, "margin": 0.0, "grand_total": 0.0}
    out = {}
    out["lines"] = int(len(df))
    out["qty_total"] = float(df["qty"].sum()) if "qty" in df.columns else 0.0
    for col in ["material_cost","machine_cost","labor_cost","consumables_cost","logistics_cost","markup_amount","total_line"]:
        if col in df.columns:
            key = "margin" if col=="markup_amount" else ("grand_total" if col=="total_line" else col)
            out[key] = float(df[col].sum())
    return out
