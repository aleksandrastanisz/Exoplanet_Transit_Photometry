import csv
from pathlib import Path
import matplotlib.pyplot as plt

from src.bls_search import find_transit_period
from src.fetch_data import download_data
from src.preprocess import clean_and_flatten
from src.transit_model import calculate_physical_parameters, fold_and_bin

def main():
    target = "TrES-2"
    quarter = 2

    figures_dir = Path("outputs/figures")
    tables_dir = Path("outputs/tables")
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    raw_lc = download_data(target, quarter)
    clean_lc, flat_lc, trend_lc = clean_and_flatten(raw_lc)
    bls, best_period, best_t0, _ = find_transit_period(flat_lc, 1.5, 4.0)
    folded_lc, binned_lc = fold_and_bin(flat_lc, best_period, best_t0)
    params = calculate_physical_parameters(binned_lc, best_period, target)

    fig, ax = plt.subplots(figsize=(10, 4))
    clean_lc.scatter(ax=ax, s=1, color="black", label="Surowe dane")
    trend_lc.plot(ax=ax, color="red", lw=1.5, label="Trend gwiazdowy")
    fig.savefig(figures_dir / "01_raw_and_trend.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    bls.plot(ax=ax, color="navy")
    ax.axvline(
        best_period.value,
        color="crimson",
        ls="--",
        label=f"P = {best_period.value:.4f} d",
    )
    fig.savefig(figures_dir / "02_bls_periodogram.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    folded_lc.scatter(ax=ax, s=1, color="silver", alpha=0.5, label="Pomiary")
    binned_lc.scatter(ax=ax, s=15, color="crimson", label="Zbindowane punkty")
    ax.set_ylim(0.980, 1.008)
    ax.set_xlim(-0.1, 0.1)
    fig.savefig(figures_dir / "03_folded_transit.png", dpi=300)
    plt.close(fig)

    csv_path = tables_dir / "parameters.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=params.keys())
        writer.writeheader()
        writer.writerow(params)

    print(f"wyniki zapisane w outputs/")


if __name__ == "__main__":
    main()