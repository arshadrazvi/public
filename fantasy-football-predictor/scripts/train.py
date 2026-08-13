from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.config import EXPORT_DIR
from backend.app.services.model_service import backtest_week, predict_week


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--season", type=int, required=True)
    parser.add_argument("--week", type=int, required=True)
    parser.add_argument("--backtest", action="store_true")
    args = parser.parse_args()

    bundle = predict_week(args.season, args.week)

    columns = [
        "player_name",
        "position",
        "projected_points",
        "low",
        "high",
    ]

    print()
    print(f"PROJECTIONS — {args.season} WEEK {args.week}")
    print("=" * 70)
    print(bundle.predictions[columns].head(50).to_string(index=False))

    export_path = EXPORT_DIR / f"predictions_{args.season}_week_{args.week}.csv"
    bundle.predictions.to_csv(export_path, index=False)
    print(f"\nSaved {export_path}")

    if args.backtest:
        metrics = backtest_week(args.season, args.week)
        print("\nBACKTEST")
        print("=" * 70)
        for key, value in metrics.items():
            print(f"{key:>15}: {value}")


if __name__ == "__main__":
    main()
