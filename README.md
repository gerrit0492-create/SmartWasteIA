# SmartWasteIA — Cost AI Tool

Streamlit-app voor kostenberekening met **live Google Sheets sync** en **AI-ondersteuning**.
Lichte UI, dashboard-first, en een simpel logo met de initialen **cp** + stijgende hartslag.

## Snelstart (lokaal)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy op Streamlit Cloud
1. Push deze repo naar GitHub.
2. Koppel de repo in Streamlit Community Cloud.
3. Voeg **Secrets** toe (Settings → Secrets) op basis van `.streamlit/secrets.toml`.
4. Deploy: Streamlit redeployt automatisch bij elke push.

## Google Sheets
- Service Account JSON plakken in secrets; deel je Sheets met het SA‑e‑mailadres.
- Pas sheet IDs aan in `[sheets]` in secrets. Gebruik de pagina **BOM Upload** (tab Google Sheets) voor live‑sync.

## AI
- Voeg je OpenAI‑compatible API key toe onder `[llm]` in secrets. Gebruik de pagina **AI Assist**.

## Mappen
```
SmartWasteIA/
├─ app.py
├─ pages/
├─ data/           # voorbeelddata (CSV)
├─ utils/          # calculatie, sheets, AI, data update
├─ assets/         # logo_cp.svg
├─ .streamlit/     # config + secrets template
└─ .github/workflows/  # automations
```

## Data update (templates)
- `utils/data_update.py` bevat voorbeeld-hooks voor actuele prijsupdates (Outokumpu/supplier).
- Workflow `update_data.yml` (zie hieronder) kan dit dagelijks runnen en committen.

## GitHub Actions
De workflow **Update data** draait dagelijks (00:30 UTC) en bij push. Hij voert `utils/data_update.py` uit.
Zet indien nodig permissies op `contents: write` voor commits via de GitHub `GITHUB_TOKEN`.