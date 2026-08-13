from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import FRONTEND_DIR, POSITIONS
from .services.data_service import clear_data_cache
from .services.model_service import backtest_week, predict_week


app = FastAPI(
    title="Fantasy Football Weekly Predictor",
    version="1.0.0",
    description="NFL weekly statistical and fantasy-point projection API.",
)

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static",
)


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/predictions")
def predictions(
    season: int = Query(..., ge=2018, le=2100),
    week: int = Query(..., ge=1, le=22),
    position: str = Query("ALL"),
    limit: int = Query(100, ge=1, le=500),
):
    position = position.upper()

    if position != "ALL" and position not in POSITIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Position must be ALL or one of {POSITIONS}",
        )

    try:
        bundle = predict_week(season, week)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    df = bundle.predictions

    if position != "ALL":
        df = df[df["position"] == position]

    df = df.head(limit)

    result = []
    for _, row in df.iterrows():
        predicted_stats = {
            key.removeprefix("pred_"): float(row[key])
            for key in df.columns
            if key.startswith("pred_")
        }

        result.append({
            "player_id": str(row["player_id"]),
            "player_name": str(row["player_name"]),
            "position": str(row["position"]),
            "season": int(row["season"]),
            "week": int(row["week"]),
            "projected_points": float(row["projected_points"]),
            "low": float(row["low"]),
            "high": float(row["high"]),
            "predicted_stats": predicted_stats,
        })

    return {
        "season": season,
        "week": week,
        "count": len(result),
        "predictions": result,
    }


@app.get("/api/backtest")
def backtest(
    season: int = Query(..., ge=2018, le=2100),
    week: int = Query(..., ge=1, le=22),
):
    try:
        return backtest_week(season, week)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/refresh")
def refresh():
    clear_data_cache()
    return {"status": "ok", "message": "In-memory NFL data cache cleared."}
