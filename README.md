# Procurement Spend & Supplier Performance Analysis

<p align="center">
  <img src="images/dashboard_preview.png" alt="Procurement performance dashboard preview" width="100%">
</p>

<p align="center">
  <b>End-to-end supply-chain analytics portfolio project</b><br>
  Python • SQL • KPI Reporting • Supplier Management • Procurement Strategy
</p>

---

## Executive summary

This project analyzes a synthetic set of 720 purchase-order records across 12 suppliers and 6 procurement categories, representing **$12.95M** in synthetic spend. The analysis converts transaction-level data into leadership-ready supplier scorecards, category summaries, and a targeted risk report.

> **Data note:** All records in this repository are synthetic and created solely for portfolio demonstration. They do not contain employer, supplier, customer, pricing, or purchase-order data from any real organization.

## Business problem

Procurement leaders need to balance continuity of supply, cost control, and supplier performance. Fragmented purchasing, unreliable delivery, and unmanaged price variation can create production disruption and unnecessary expedite costs. This project answers: **Which suppliers and categories should procurement prioritize to improve reliability and reduce spend risk?**

## Objectives

- Quantify spend by supplier and category.
- Evaluate supplier on-time delivery against a 95% performance target.
- Identify late or expedited purchase orders requiring action.
- Build a supplier scorecard combining spend, delivery, quality, and expedite exposure.
- Translate results into practical sourcing and supplier-management recommendations.

## Tools and techniques

| Area | Tools / methods |
|---|---|
| Data analysis | Python, Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Business intelligence | KPI design, supplier scorecards, risk segmentation |
| Database analysis | SQL aggregations, conditional logic, joins |
| Domain focus | Procurement spend, supplier performance, on-time delivery, expedited orders |

## Project structure

```text
procurement-spend-supplier-analysis/
├── data/                         # Synthetic purchase-order records
├── images/                       # Dashboard and README visuals
├── notebooks/                    # Exploratory notebook
├── outputs/                      # Generated KPI tables and risk report
├── sql/                          # Reusable SQL analysis queries
├── src/                          # Reproducible Python analysis
├── README.md
└── requirements.txt
```

## KPI framework

| KPI | Definition | Why it matters |
|---|---|---|
| Total spend | Sum of PO line spend | Shows sourcing concentration and negotiation leverage |
| On-time delivery | Share of POs delivered on/before required date | Measures supplier reliability and continuity-of-supply risk |
| Average days late | Mean lateness for each supplier | Separates minor variance from persistent service failures |
| Expedite count | POs flagged for acceleration | Highlights avoidable operational cost and disruption risk |
| Supplier score | Weighted delivery, quality, risk, and spend-performance measure | Prioritizes supplier actions consistently |

## Key findings

Findings below are computed directly from the dataset in `data/synthetic_procurement_data.csv` by running `src/procurement_analysis.py`.

- Total synthetic spend across all purchase orders is **$12.95M**, with **Logistics** the largest category at **$6,575K**.
- Overall on-time delivery is **89.4%**, below the 95% target, with **9 of 12 suppliers** falling short of that benchmark.
- **Summit Freight Partners** is the highest-spend supplier (**$3,505K**) but delivers on time only **80.3%** of the time, making it the top priority for a supplier-development conversation.
- **Pacific Industrial Co.** has the weakest on-time delivery rate at **79.3%**, warranting a formal corrective-action plan or backup-source evaluation.
- **69 purchase orders** required expediting, representing avoidable freight premiums and operational risk concentrated among the lowest-scoring suppliers.

## Recommended actions

1. **Protect high-spend, reliable suppliers.** Use volume forecasts and longer-term agreements where performance supports consolidation.
2. **Develop or mitigate underperforming suppliers.** Start with Summit Freight Partners and Pacific Industrial Co.; validate capacity, lead-time assumptions, and communication cadence.
3. **Monitor high-risk POs weekly.** Prioritize the 69 orders in `outputs/late_po_risk_report.csv` that are late by four or more days or required expediting.
4. **Use category-level spend reviews.** Target Logistics for competitive quotes, price-variance analysis, and demand-planning collaboration given its $6,575K spend share.
5. **Institutionalize supplier scorecards.** Review on-time delivery, quality, spend, and expedite trends in recurring supplier-business reviews using `outputs/supplier_scorecard.csv`.

## Visual analysis

### Supplier spend and delivery signal

![Top supplier spend](images/supplier_spend.png)

### On-time delivery performance

![On-time delivery](images/on_time_delivery.png)

### Category spend

![Category spend](images/category_spend.png)

> **Note:** Chart images are generated locally by running the analysis script (see below) and are not yet committed to this repository. Run the script and commit the `images/` folder to complete the visuals.

## How to run

```bash
git clone https://github.com/JonathanMCopelandJr/procurement-spend-supplier-analysis.git
cd procurement-spend-supplier-analysis
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/procurement_analysis.py
```

The script refreshes the summary files in `outputs/` and charts in `images/`.

## Author

**Jonathan M. Copeland Jr.**
Buyer Planner | Data Analytics M.S. | SQL, Python, Excel, Forecasting, Supply Chain Analytics
[LinkedIn](https://www.linkedin.com/in/jonathanmcopeland) • [GitHub](https://github.com/JonathanMCopelandJr)
