# SmartWasteIA — Cost AI Tool (v4 full)

Streamlit-app voor kostenberekening met **live Google Sheets sync**, **AI-ondersteuning**, lichte UI en dashboard-first ontwerp.
Inclusief workflows voor **dagelijkse data-update** en **export**.

## Snelstart
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud
- Koppel repo → Deploy
- Zet **Secrets** via `.streamlit/secrets.toml` (Service Account, Sheet IDs, LLM-key)

## Pagina's
- **Dashboard** — overzicht en metrics
- **BOM Upload** — CSV + Google Sheets live-sync
- **Data Sources** — materials/machines/labor beheren + update
- **AI Assist** — AI-advies (LLM)
- **Export Data** — Google Sheets + Power BI (CSV)
- **Settings** — handleiding & secrets

## Data model (BOM min-kolommen)
`item_code, description, qty, unit, material_code, material_qty (optioneel), unit_price_eur (optioneel), machine_code, process_time_min_machine, labor_grade, process_time_min_labor, markup_pct`

## Licentie & compliance
- Controleer leveranciersvoorwaarden bij scrapen en prijsdata.