from __future__ import annotations
import pandas as pd

def estimate_machine_minutes(row: pd.Series, machines_df: pd.DataFrame) -> float:
    """If process_time_min_machine is zero, estimate based on process and simple heuristics."""
    base = float(row.get("process_time_min_machine", 0) or 0)
    if base > 0:
        return base
    mcode = row.get("machine_code", "")
    m = machines_df.loc[machines_df["machine_code"] == mcode]
    process = m["process"].values[0] if not m.empty else ""
    # simplistic heuristics
    if process == "laser_cut":
        length = float(row.get("length_mm", 0) or 0)
        return max(0.5, 0.004 * length)  # 4 sec per 1 mm path (demo)
    if process == "bending":
        bends = max(1, int( (row.get("length_mm", 100) or 100) / 100 ))
        return 0.4 * bends + 0.6  # per bend + handling
    if process == "turning":
        length = float(row.get("length_mm", 0) or 50)
        return 0.15 * (length/10) + 8
    if process == "milling":
        length = float(row.get("length_mm", 0) or 50)
        return 0.20 * (length/10) + 10
    if process == "welding":
        # assume labor-driven, keep small machine time
        return 0.2 * float(row.get("process_time_min_labor", 10) or 10)
    if process == "additive":
        vol = (float(row.get("area_cm2", 0) or 0) * float(row.get("thickness_mm", 0) or 0)) / 10.0
        return max(30.0, vol * 1.2)  # min 30 min print time
    if process == "coating":
        return 12.0
    return 5.0
