from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from ..config import POSITIONS
from .data_service import load_player_data
from .feature_engineering import add_features, feature_columns


STAT_TARGETS = {
    "QB": [
        "passing_yards", "passing_tds", "interceptions",
        "rushing_yards", "rushing_tds",
    ],
    "RB": [
        "rushing_yards", "rushing_tds", "receptions",
        "receiving_yards", "receiving_tds",
    ],
    "WR": [
        "receptions", "receiving_yards", "receiving_tds",
        "rushing_yards", "rushing_tds",
    ],
    "TE": [
        "receptions", "receiving_yards", "receiving_tds",
    ],
}

OUTPUT_STATS = [
    "passing_yards", "passing_tds", "interceptions",
    "rushing_yards", "rushing_tds",
    "receptions", "receiving_yards", "receiving_tds",
]


@dataclass
class PredictionBundle:
    predictions: pd.DataFrame
    source_week: pd.DataFrame


def _new_model() -> HistGradientBoostingRegressor:
    return HistGradientBoostingRegressor(
        learning_rate=0.05,
        max_iter=200,
        max_leaf_nodes=20,
        min_samples_leaf=20,
        l2_regularization=1.0,
        random_state=42,
    )


def _before_week(df: pd.DataFrame, season: int, week: int) -> pd.DataFrame:
    return df[
        (df["season"] < season)
        | ((df["season"] == season) & (df["week"] < week))
    ].copy()


def _exact_week(df: pd.DataFrame, season: int, week: int) -> pd.DataFrame:
    return df[(df["season"] == season) & (df["week"] == week)].copy()


def _train_models(train_df: pd.DataFrame, features: list[str]):
    models: dict[str, dict[str, HistGradientBoostingRegressor]] = {}

    for position in POSITIONS:
        models[position] = {}
        pos_df = train_df[
            (train_df["position"] == position)
            & (train_df["games_played_before"] >= 2)
        ].copy()

        for target in STAT_TARGETS[position]:
            usable = pos_df.dropna(subset=[target])
            if len(usable) < 100:
                continue

            model = _new_model()
            model.fit(usable[features].fillna(0), usable[target])
            models[position][target] = model

    return models


def _predict_stats(models, rows: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    # nflverse player-stat datasets commonly expose the player's team as
    # ``recent_team``. Keep this optional so schema changes do not break the app.
    team_column = None
    for candidate in ("recent_team", "team"):
        if candidate in rows.columns:
            team_column = candidate
            break

    output_columns = [
        "player_id",
        "player_name",
        "position",
        "season",
        "week",
    ]

    if team_column:
        output_columns.append(team_column)

    out = rows[output_columns].copy()

    if team_column:
        out = out.rename(columns={team_column: "team"})
    else:
        out["team"] = ""

    for stat in OUTPUT_STATS:
        out[f"pred_{stat}"] = 0.0

    for position in POSITIONS:
        mask = rows["position"] == position
        if not mask.any():
            continue

        X = rows.loc[mask, features].fillna(0)

        for target, model in models.get(position, {}).items():
            values = np.maximum(model.predict(X), 0)
            out.loc[mask, f"pred_{target}"] = values

    return out


def _projected_points(df: pd.DataFrame) -> pd.Series:
    return (
        df["pred_passing_yards"] * 0.04
        + df["pred_passing_tds"] * 4
        - df["pred_interceptions"] * 2
        + df["pred_rushing_yards"] * 0.10
        + df["pred_rushing_tds"] * 6
        + df["pred_receptions"]
        + df["pred_receiving_yards"] * 0.10
        + df["pred_receiving_tds"] * 6
    )


def predict_week(season: int, week: int) -> PredictionBundle:
    raw = load_player_data(season)
    df = add_features(raw)
    features = feature_columns(df)

    train_df = _before_week(df, season, week)
    target_df = _exact_week(df, season, week)

    if train_df.empty:
        raise ValueError("No training data exists before the requested week.")

    if target_df.empty:
        raise ValueError(
            f"No player-stat rows exist for {season} Week {week}. "
            "This starter currently predicts weeks already represented "
            "in the nflverse player-stat dataset."
        )

    models = _train_models(train_df, features)
    predictions = _predict_stats(models, target_df, features)
    predictions["projected_points"] = _projected_points(predictions)

    # Approximate empirical range for MVP. This is not a formal prediction interval.
    position_margin = {"QB": 6.0, "RB": 5.5, "WR": 5.5, "TE": 4.5}
    predictions["margin"] = predictions["position"].map(position_margin).fillna(6.0)
    predictions["low"] = np.maximum(
        0, predictions["projected_points"] - predictions["margin"]
    )
    predictions["high"] = predictions["projected_points"] + predictions["margin"]

    numeric = [
        c for c in predictions.columns
        if c.startswith("pred_")
    ] + ["projected_points", "low", "high", "margin"]

    predictions[numeric] = predictions[numeric].round(2)
    predictions = predictions.sort_values("projected_points", ascending=False)

    return PredictionBundle(predictions=predictions, source_week=target_df)


def backtest_week(season: int, week: int) -> dict:
    bundle = predict_week(season, week)

    actual = bundle.source_week[
        ["player_id", "fantasy_points"]
    ].copy()

    comparison = bundle.predictions.merge(actual, on="player_id", how="inner")
    if comparison.empty:
        raise ValueError("No players were available for backtesting.")

    y_true = comparison["fantasy_points"]
    y_pred = comparison["projected_points"]
    error = np.abs(y_true - y_pred)

    return {
        "season": season,
        "week": week,
        "players_tested": int(len(comparison)),
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 2),
        "rmse": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 2),
        "within_2": round(float((error <= 2).mean() * 100), 1),
        "within_4": round(float((error <= 4).mean() * 100), 1),
        "within_6": round(float((error <= 6).mean() * 100), 1),
    }
