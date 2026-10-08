from __future__ import annotations

import numpy as np
import pandas as pd

from .data_service import BASE_STATS


def fantasy_points(df: pd.DataFrame) -> pd.Series:
    fumbles = (
        df["rushing_fumbles_lost"]
        + df["receiving_fumbles_lost"]
        + df["sack_fumbles_lost"]
    )

    return (
        df["passing_yards"] * 0.04
        + df["passing_tds"] * 4
        - df["interceptions"] * 2
        + df["rushing_yards"] * 0.10
        + df["rushing_tds"] * 6
        + df["receptions"]
        + df["receiving_yards"] * 0.10
        + df["receiving_tds"] * 6
        - fumbles * 2
    )


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["fantasy_points"] = fantasy_points(df)

    grouped = df.groupby(["player_id", "season"], group_keys=False)

    for stat in [*BASE_STATS, "fantasy_points"]:
        df[f"{stat}_lag1"] = grouped[stat].shift(1)

        df[f"{stat}_avg3"] = grouped[stat].transform(
            lambda x: x.shift(1).rolling(3, min_periods=1).mean()
        )
        df[f"{stat}_avg5"] = grouped[stat].transform(
            lambda x: x.shift(1).rolling(5, min_periods=1).mean()
        )
        df[f"{stat}_season_avg"] = grouped[stat].transform(
            lambda x: x.shift(1).expanding(min_periods=1).mean()
        )

    df["games_played_before"] = grouped.cumcount()

    df["target_trend"] = df["targets_avg3"] - df["targets_avg5"]
    df["carry_trend"] = df["carries_avg3"] - df["carries_avg5"]
    df["reception_trend"] = df["receptions_avg3"] - df["receptions_avg5"]

    df["yards_per_carry_avg3"] = np.where(
        df["carries_avg3"] > 0,
        df["rushing_yards_avg3"] / df["carries_avg3"],
        0,
    )
    df["yards_per_target_avg3"] = np.where(
        df["targets_avg3"] > 0,
        df["receiving_yards_avg3"] / df["targets_avg3"],
        0,
    )
    df["catch_rate_avg3"] = np.where(
        df["targets_avg3"] > 0,
        df["receptions_avg3"] / df["targets_avg3"],
        0,
    )
    df["pass_yards_per_attempt_avg3"] = np.where(
        df["attempts_avg3"] > 0,
        df["passing_yards_avg3"] / df["attempts_avg3"],
        0,
    )

    return df.replace([np.inf, -np.inf], np.nan)


def feature_columns(df: pd.DataFrame) -> list[str]:
    columns: list[str] = []

    for stat in [*BASE_STATS, "fantasy_points"]:
        for suffix in ("_lag1", "_avg3", "_avg5", "_season_avg"):
            name = f"{stat}{suffix}"
            if name in df.columns:
                columns.append(name)

    columns.extend([
        "week",
        "games_played_before",
        "target_trend",
        "carry_trend",
        "reception_trend",
        "yards_per_carry_avg3",
        "yards_per_target_avg3",
        "catch_rate_avg3",
        "pass_yards_per_attempt_avg3",
    ])

    return [column for column in columns if column in df.columns]
