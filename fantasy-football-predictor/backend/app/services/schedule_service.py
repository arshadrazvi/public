"""Build pregame player rows using the NFL schedule and historical participation."""
from functools import lru_cache
import pandas as pd
import nflreadpy as nfl

from ..config import POSITIONS
from .data_service import BASE_STATS

@lru_cache(maxsize=8)
def load_schedule(season: int) -> pd.DataFrame:
    try:
        raw = nfl.load_schedules([season])
        df = raw.to_pandas() if hasattr(raw, "to_pandas") else pd.DataFrame(raw)
    except Exception as exc:
        raise ValueError(
            f"Could not download {season} NFL schedule. Check internet access "
            f"and nflreadpy version. Details: {exc}"
        ) from exc
    required = {"season", "week", "home_team", "away_team"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Schedule is missing columns: {sorted(missing)}")
    if "game_type" in df.columns:
        df = df[df["game_type"].astype(str).isin(["REG", "reg"])]
    elif "season_type" in df.columns:
        df = df[df["season_type"].astype(str).isin(["REG", "reg"])]
    return df

def _team_column(df):
    for name in ("recent_team", "team"):
        if name in df.columns:
            return name
    raise ValueError("Player statistics have no team column.")

def make_future_rows(history: pd.DataFrame, season: int, week: int) -> pd.DataFrame:
    games = load_schedule(season)
    games = games[(games["season"] == season) & (games["week"] == week)]
    if games.empty:
        raise ValueError(f"No regular-season schedule exists for {season} Week {week}.")
    teams = set(games["home_team"].dropna()) | set(games["away_team"].dropna())
    history = history.copy()
    history = history[(history["season"] < season) |
                      ((history["season"] == season) & (history["week"] < week))]
    if history.empty:
        raise ValueError("No historical games before the requested week.")
    team_col = _team_column(history)
    history = history.sort_values(["season", "week"])
    latest = history.drop_duplicates("player_id", keep="last")
    latest = latest[latest[team_col].isin(teams) &
                    latest["position"].isin(POSITIONS)].copy()

    # Players must have appeared recently; this is a candidate pool,
    # not a guarantee of active roster status or availability.
    current = latest[(latest["season"] == season) &
                     (latest["week"] >= max(1, week - 4))]
    if week <= 2:
        prior = latest[(latest["season"] == season - 1) &
                       (latest["week"] >= 14)]
        latest = pd.concat([current, prior]).drop_duplicates("player_id")
    else:
        latest = current

    if latest.empty:
        raise ValueError(
            "No recent players found for scheduled teams. "
            "Check whether the requested season's player stats are published."
        )

    # A synthetic, zero-stat row is appended AFTER all historical rows.
    # add_features() uses shift(1), so these zeroes never enter its inputs.
    future = latest.copy()
    future["season"] = season
    future["week"] = week
    for stat in BASE_STATS:
        future[stat] = 0.0
    return future.reset_index(drop=True)
