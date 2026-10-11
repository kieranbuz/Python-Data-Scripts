# Python Data Scripts

Python scripts built and deployed against live data for real business
operations.

**What this demonstrates:** turning a manual POS export into a repeatable cleaning and reconciliation step, used in production for a real business.

---

## Customer Loyalty Points Engine

**Python · Pandas · Deployed at Discover Diving (2022)**

Aggregates transaction data exported from a POS system, calculates
spend-based loyalty points at 2.5% of net sales, and reconciles balances
across the full customer database. Output is a cleaned CSV ready to import
back into the POS.

### What it does

- Ingests a receipts export and existing customer database as CSVs
- Deduplicates customers and aggregates total spend and visit count
- Calculates each customer's points balance at 2.5% of net sales for the
  export period — this replaces the existing balance rather than adding to it
- Reconciles against the existing customer file — updates known customers,
  zeros out anyone with no recent transactions
- Exports an updated customer CSV ready for POS import

### Files

| File | Description |
|------|-------------|
| `customer_points_v1.py` | Original deployed script (2022) — iterative approach |
| `customer_points_v2.py` | Refactored version — vectorised Pandas, typed functions, cleaner structure |

### Input format

**`receipts-YYYY-MM-DD-YYYY-MM-DD.csv`**

| Column | Description |
|--------|-------------|
| `Customer name` | Customer identifier |
| `Net sales` | Transaction value (£) |

**`customers-YYYY-MM-DD.csv`**

| Column | Description |
|--------|-------------|
| `Customer name` | Customer identifier |
| `Points balance` | Current points balance to be updated |

### Output

`customerUpdatedPoints.csv` — full customer database with recalculated
points balances.

### Setup

```bash
pip install pandas
python customer_points_v2.py
```

Update the file paths in `load_data()` to match your CSV exports.

---

## Tech

- Python 3
- Pandas
