from __future__ import annotations
import pandas as pd

def estimate_machine_minutes(row: pd.Series, machines_df: pd.DataFrame) -> float:
    base = float(row.get("process_time_min_machine", 0) or 0)
    if base > 0:
        return base
    mcode = row.get("machine_code", "")
    m = machines_df.loc[machines_df["machine_code"] == mcode]
    process = m["process"].values[0] if not m.empty else ""
    if process == "laser_cut":
        length = float(row.get("length_mm", 0) or 0)
        return max(1.0, 0.0038 * length)  # 3.8 sec / mm path estimate
    if process == "bending":
        bends = max(1, int((row.get("length_mm", 150) or 150) / 120))
        return 0.5 * bends + 0.8
    if process == "turning":
        length = float(row.get("length_mm", 60) or 60)
        d = float(row.get("diameter_mm", 30) or 30)
        return 6 + 0.1 * (length/10) + 0.05 * (d/5)
    if process == "milling":
        return 12.0
    if process == "welding":
        return 0.25 * float(row.get("process_time_min_labor", 20) or 20)
    if process == "additive":
        vol = (float(row.get("area_cm2", 0) or 0) * float(row.get("thickness_mm", 0) or 0)) / 10.0
        return max(45.0, vol * 1.1)
    if process == "coating":
        return 8.0
    if process == "quality":
        return 6.0
    return 5.0
