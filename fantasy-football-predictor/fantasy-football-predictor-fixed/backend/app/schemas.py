from pydantic import BaseModel


class Prediction(BaseModel):
    player_id: str
    player_name: str
    position: str
    season: int
    week: int
    projected_points: float
    low: float
    high: float
    predicted_stats: dict[str, float]


class PredictionResponse(BaseModel):
    season: int
    week: int
    count: int
    predictions: list[Prediction]


class BacktestResponse(BaseModel):
    season: int
    week: int
    players_tested: int
    mae: float
    rmse: float
    within_2: float
    within_4: float
    within_6: float
