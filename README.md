# Generic Medicine Substitute Finder

A Flask-based web application that helps users find cheaper generic substitutes for branded medicines available in the Indian pharmaceutical market. Substitutes are identified by matching **active composition** (not brand name), so users can confidently compare chemically equivalent alternatives and see potential cost savings.

Built on the [A-Z Medicine Dataset of India](https://www.kaggle.com/datasets/shudhanshusingh/az-medicine-dataset-of-india) (~250,000 records) by Shudhanshu Singh.

> ⚠️ **Disclaimer:** This tool is informational only and does not provide medical advice. Always consult a licensed doctor or pharmacist before switching medicines.

---

## Features

- **Medicine Search** — Search by name with fuzzy matching (via RapidFuzz), so typos and partial names still return relevant results.
- **Medicine Details & Substitutes** — View a medicine's price, manufacturer, type, pack size, and composition, along with all generic substitutes sharing the exact same active composition.
- **Price Comparison & Savings** — Substitutes are ranked cheapest-first, with the potential savings calculated against the originally searched medicine.
- **Insights Dashboard** — Analytical charts generated from the dataset: price distribution, price variation by medicine type, top manufacturers, and compositions with the most competing branded variants.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | MySQL |
| Data Processing | Pandas |
| Fuzzy Search | RapidFuzz |
| Data Visualization | Matplotlib, Seaborn |
| Frontend | HTML5, CSS3, Bootstrap |

---

## Project Structure

```
Generic Medicine Substitute Finder/
├── app.py                  # Flask entry point
├── config.py                # App configuration
├── db.py                    # MySQL connection helper
├── import_data.py           # One-time CSV → MySQL import script
├── main.py                  # Standalone script: generates analytics charts
├── requirements.txt
├── .env.example              # Template for environment variables
├── blueprints/
│   └── medicine_routes.py   # Search, details, substitutes, dashboard routes
├── sql/
│   └── schema.sql            # Database schema
├── static/
│   └── css/
│       └── style.css         # Custom design system
├── templates/
│   ├── medicine_search.html
│   ├── medicine_view.html
│   └── dashboard.html
├── dataset/
│   └── A_Z_medicines_dataset_of_India.csv   # (not tracked in git — see Setup)
└── Diagramatic Results/      # Generated charts (created by main.py)
```

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd "Generic Medicine Substitute Finder"
```

### 2. Create and activate a virtual environment

```bash
python -m venv myenv
myenv\Scripts\Activate.ps1      # Windows PowerShell
# source myenv/bin/activate     # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and fill in your actual values:

```bash
cp .env.example .env
```

```
SECRET_KEY=your-secret-key-here
```

> **Note:** Database credentials (`host`, `user`, `password`, `database`) are currently hardcoded directly inside `db.py`, not read from `.env`. If your MySQL setup differs from the defaults (`localhost`, user `root`, no password, database `Substitute_Finder_App`), edit the `get_connection()` function in `db.py` directly.
>
> ⚠️ Since credentials live in `db.py`, avoid committing real passwords to this file if you ever set one — either keep it out of version control at that point, or move to environment variables instead.

### 5. Set up the database

Create the MySQL database, then run the schema:

```sql
CREATE DATABASE Substitute_Finder_App;
```

```bash
mysql -u root -p Substitute_Finder_App < sql/schema.sql
```

### 6. Download the dataset

Download `A_Z_medicines_dataset_of_India.csv` from [Kaggle](https://www.kaggle.com/datasets/shudhanshusingh/az-medicine-dataset-of-india) and place it in the `dataset/` folder.

### 7. Import the data

```bash
python import_data.py
```

### 8. (Optional) Generate analytics charts

```bash
python main.py
```

### 9. Run the application

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## How Substitute Matching Works

Each medicine's `short_composition1` and `short_composition2` fields are combined into a single, sorted **composition key**. Medicines sharing the exact same composition key — regardless of brand name — are treated as substitutes for one another. Discontinued medicines are excluded from substitute results by default, and results are sorted by price, cheapest first.

---

## Notes on Scope

- This project uses a **static, pre-compiled dataset** — prices and availability are not live and do not reflect real-time pharmacy stock.
- There is **no user login, admin panel, or account system** — the application is a public, single-purpose lookup tool.
- Substitute matching is based on **exact composition string matching**, not natural-language or ML-based ingredient parsing.

---

## License

This project was built for educational purposes.
