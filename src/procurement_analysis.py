from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_procurement_data.csv"
OUTPUTS = ROOT / "outputs"
IMAGES = ROOT / "images"
OUTPUTS.mkdir(exist_ok=True)
IMAGES.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")
COLORS = {"navy": "#102A43", "teal": "#00A6A6", "orange": "#F4A261", "red": "#E76F51"}


def load_data():
    df = pd.read_csv(DATA, parse_dates=["order_date", "required_delivery_date", "actual_delivery_date"])
    df["on_time_flag"] = (df["delivery_status"] == "On Time").astype(int)
    df["expedite_flag_num"] = (df["expedite_flag"] == "Yes").astype(int)
    return df


def supplier_scorecard(df):
    scorecard = df.groupby("supplier").agg(
        total_spend=("total_spend", "sum"),
        purchase_orders=("po_number", "count"),
        on_time_delivery_pct=("on_time_flag", lambda x: x.mean() * 100),
        avg_days_late=("days_late", "mean"),
        avg_quality_score=("quality_score", "mean"),
        expedited_pos=("expedite_flag_num", "sum"),
    ).reset_index()
    scorecard["supplier_score"] = (
        scorecard["on_time_delivery_pct"] * 0.45
        + scorecard["avg_quality_score"] * 0.30
        + (100 - scorecard["avg_days_late"].clip(upper=12) * 8) * 0.15
        + (100 - (scorecard["expedited_pos"] / scorecard["purchase_orders"] * 100 * 2).clip(upper=100)) * 0.10
    ).round(1)
    scorecard["priority_action"] = scorecard.apply(
        lambda x: "Develop / mitigate risk" if x.on_time_delivery_pct < 90 or x.avg_quality_score < 92 else "Maintain / grow relationship",
        axis=1,
    )
    return scorecard.sort_values("total_spend", ascending=False).round(2)


def category_summary_table(df):
    return df.groupby("category").agg(
        total_spend=("total_spend", "sum"),
        purchase_orders=("po_number", "count"),
        on_time_delivery_pct=("on_time_flag", lambda x: x.mean() * 100),
        avg_unit_price=("unit_price", "mean"),
    ).reset_index().sort_values("total_spend", ascending=False).round(2)


def risk_report_table(df):
    risk = df[(df["days_late"] >= 4) | (df["expedite_flag"] == "Yes")].copy()
    risk["risk_level"] = risk.apply(lambda x: "High" if x.days_late >= 7 or x.expedite_flag == "Yes" else "Medium", axis=1)
    return risk.sort_values(["risk_level", "days_late"], ascending=[True, False])


def create_charts(scorecard, category_summary):
    top = scorecard.head(8).sort_values("total_spend")
    plt.figure(figsize=(11, 6))
    plt.barh(top["supplier"], top["total_spend"] / 1000,
             color=[COLORS["teal"] if x >= 90 else COLORS["orange"] for x in top["on_time_delivery_pct"]])
    plt.title("Top Supplier Spend with Delivery Performance Signal", fontweight="bold", color=COLORS["navy"])
    plt.xlabel("Total Spend ($000s)")
    plt.tight_layout()
    plt.savefig(IMAGES / "supplier_spend.png", dpi=180)
    plt.close()

    ordered = scorecard.sort_values("on_time_delivery_pct")
    plt.figure(figsize=(11, 6))
    plt.barh(ordered["supplier"], ordered["on_time_delivery_pct"],
              color=[COLORS["red"] if x < 90 else COLORS["teal"] for x in ordered["on_time_delivery_pct"]])
    plt.axvline(95, color=COLORS["navy"], linestyle="--", label="95% target")
    plt.xlim(70, 100)
    plt.legend(frameon=False)
    plt.title("On-Time Delivery by Supplier", fontweight="bold", color=COLORS["navy"])
    plt.xlabel("On-Time Delivery (%)")
    plt.tight_layout()
    plt.savefig(IMAGES / "on_time_delivery.png", dpi=180)
    plt.close()

    ordered_categories = category_summary.sort_values("total_spend")
    plt.figure(figsize=(11, 6))
    plt.barh(ordered_categories["category"], ordered_categories["total_spend"] / 1000, color=COLORS["navy"])
    plt.title("Spend by Procurement Category", fontweight="bold", color=COLORS["navy"])
    plt.xlabel("Total Spend ($000s)")
    plt.tight_layout()
    plt.savefig(IMAGES / "category_spend.png", dpi=180)
    plt.close()


def create_dashboard(df, scorecard):
    fig = plt.figure(figsize=(15, 9), facecolor="#F7FAFC")
    fig.text(0.04, 0.95, "PROCUREMENT PERFORMANCE DASHBOARD", fontsize=20, fontweight="bold", color=COLORS["navy"])
    fig.text(0.04, 0.915, "Synthetic portfolio case study | Spend, supplier reliability, and risk management",
              fontsize=10, color="#486581")
    metrics = [
        ("Total Spend", f"${df.total_spend.sum() / 1e6:.2f}M", COLORS["teal"]),
        ("On-Time Delivery", f"{(df.delivery_status == 'On Time').mean() * 100:.1f}%", COLORS["navy"]),
        ("Expedited POs", str((df.expedite_flag == "Yes").sum()), COLORS["orange"]),
        ("Suppliers Below Target", str((scorecard.on_time_delivery_pct < 95).sum()), COLORS["red"]),
    ]
    for j, (lab, val, col) in enumerate(metrics):
        x = 0.04 + j * 0.235
        fig.patches.append(plt.Rectangle((x, 0.78), 0.20, 0.10, transform=fig.transFigure,
                                          facecolor="white", edgecolor="#D9E2EC", lw=1))
        fig.text(x + 0.015, 0.845, val, fontsize=20, fontweight="bold", color=col)
        fig.text(x + 0.015, 0.805, lab, fontsize=9, color="#627D98")

    ax1 = fig.add_axes([0.06, 0.18, 0.42, 0.48], facecolor="white")
    top = scorecard.head(7).sort_values("total_spend")
    ax1.barh(top["supplier"], top["total_spend"] / 1000, color=COLORS["teal"])
    ax1.set_title("Top Supplier Spend ($000s)", loc="left", fontweight="bold", color=COLORS["navy"], pad=12)
    ax1.set_xlabel("$000s")
    ax1.spines[["top", "right", "left"]].set_visible(False)
    ax1.grid(axis="x", alpha=0.25)

    ax2 = fig.add_axes([0.55, 0.18, 0.39, 0.48], facecolor="white")
    ordered = scorecard.sort_values("on_time_delivery_pct")
    ax2.barh(ordered["supplier"], ordered["on_time_delivery_pct"],
              color=[COLORS["red"] if x < 90 else COLORS["teal"] for x in ordered["on_time_delivery_pct"]])
    ax2.axvline(95, color=COLORS["navy"], linestyle="--", lw=1.2)
    ax2.set_xlim(70, 100)
    ax2.set_title("On-Time Delivery vs. 95% Target", loc="left", fontweight="bold", color=COLORS["navy"], pad=12)
    ax2.set_xlabel("OTD %")
    ax2.spines[["top", "right", "left"]].set_visible(False)
    ax2.grid(axis="x", alpha=0.25)

    fig.savefig(IMAGES / "dashboard_preview.png", dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    df = load_data()
    scorecard = supplier_scorecard(df)
    category_summary = category_summary_table(df)
    risk_report = risk_report_table(df)

    scorecard.to_csv(OUTPUTS / "supplier_scorecard.csv", index=False)
    category_summary.to_csv(OUTPUTS / "category_spend_summary.csv", index=False)
    risk_report.to_csv(OUTPUTS / "late_po_risk_report.csv", index=False)

    create_charts(scorecard, category_summary)
    create_dashboard(df, scorecard)

    print(f"Analysis complete. Processed {len(df):,} purchase orders across {df['supplier'].nunique()} suppliers.")


if __name__ == "__main__":
    main()
