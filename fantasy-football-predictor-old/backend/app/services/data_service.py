from __future__ import annotations

from functools import lru_cache

import nflreadpy as nfl
import pandas as pd

from ..config import FIRST_SEASON, POSITIONS


BASE_STATS = [
    "completions",
    "attempts",
    "passing_yards",
    "passing_tds",
    "interceptions",
    "carries",
    "rushing_yards",
    "rushing_tds",
    "receptions",
    "targets",
    "receiving_yards",
    "receiving_tds",
    "rushing_fumbles_lost",
    "receiving_fumbles_lost",
    "sack_fumbles_lost",
]


@lru_cache(maxsize=8)
def load_player_data(end_season: int, start_season: int = FIRST_SEASON) -> pd.DataFrame:
    seasons = list(range(start_season, end_season + 1))
    raw = nfl.load_player_stats(seasons)
    df = raw.to_pandas()

    required = ["season", "week", "player_id", "player_name", "position"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise RuntimeError(f"nflverse data is missing required columns: {missing}")

    if "season_type" in df.columns:
        df = df[df["season_type"] == "REG"]

    df = df[df["position"].isin(POSITIONS)].copy()

    for column in BASE_STATS:
        if column not in df.columns:
            df[column] = 0.0

    for column in ["season", "week", *BASE_STATS]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df[BASE_STATS] = df[BASE_STATS].fillna(0.0)
    df["player_id"] = df["player_id"].astype(str)
    df["player_name"] = df["player_name"].fillna("Unknown").astype(str)

    return df.sort_values(
        ["player_id", "season", "week"]
    ).reset_index(drop=True)


def clear_data_cache() -> None:
    load_player_data.cache_clear()
