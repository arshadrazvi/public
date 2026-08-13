# Fantasy Football Weekly Predictor

A full-stack machine-learning application that downloads historical NFL player statistics, analyzes player performance and usage trends, and predicts fantasy-football production for NFL weeks.

The project uses **nflverse** data through `nflreadpy`, **scikit-learn** machine learning, a **FastAPI** backend, and a lightweight **HTML/CSS/JavaScript** frontend.

## Features

- Downloads NFL weekly player statistics using `nflreadpy`
- Supports QB, RB, WR, and TE
- Calculates full-PPR fantasy points
- Creates lagged and rolling player-performance features
- Uses 3-game, 5-game, and season-to-date averages
- Tracks targets, carries, receptions, and efficiency trends
- Trains position-specific machine-learning models
- Predicts individual football statistics before calculating fantasy points
- Provides projected low/high ranges
- Filters projections by position
- Searches players by name
- Provides historical backtesting
- Calculates MAE, RMSE, and percentage within ±2/±4/±6 fantasy points
- Provides REST API endpoints and FastAPI Swagger documentation
- Exports predictions to CSV

## Architecture

```text
NFLVERSE
    |
    v
nflreadpy
    |
    v
Data Service
    |
    v
Feature Engineering
    |
    +-- Lag-1 statistics
    +-- 3-game averages
    +-- 5-game averages
    +-- Season averages
    +-- Usage trends
    +-- Efficiency metrics
    |
    v
Position-Specific ML Models
    |
    v
Statistical Predictions
    |
    v
Fantasy Scoring
    |
    v
FastAPI REST API
    |
    v
HTML / CSS / JavaScript Frontend
```

## Technology Stack

### Backend

- Python 3
- FastAPI
- Uvicorn
- Pandas
- NumPy
- scikit-learn
- PyArrow
- nflreadpy

### Machine Learning

The initial prediction engine uses `HistGradientBoostingRegressor`.

Separate models are trained for different player positions and individual statistics.

### Frontend

- HTML
- CSS
- JavaScript
- Fetch API

No Node.js build system is required.

## Project Directory Structure

```text
fantasy-football-predictor/
|
+-- backend/
|   +-- __init__.py
|   +-- app/
|       +-- __init__.py
|       +-- main.py
|       +-- config.py
|       +-- schemas.py
|       +-- services/
|           +-- __init__.py
|           +-- data_service.py
|           +-- feature_engineering.py
|           +-- model_service.py
|
+-- frontend/
|   +-- index.html
|   +-- app.js
|   +-- styles.css
|
+-- scripts/
|   +-- train.py
|
+-- data/
|   +-- cache/
|   +-- models/
|   +-- exports/
|
+-- requirements.txt
+-- run.py
+-- README.md
+-- .gitignore
```

## File Responsibilities

### `backend/app/main.py`

Main FastAPI application. It serves the frontend and provides the REST API.

Current endpoints:

```text
GET  /
GET  /api/health
GET  /api/predictions
GET  /api/backtest
POST /api/refresh
```

### `backend/app/config.py`

Contains project paths, data directories, supported positions, and other application configuration.

### `backend/app/schemas.py`

Contains Pydantic response models.

### `backend/app/services/data_service.py`

Downloads weekly player statistics from nflverse, converts the data to Pandas, filters relevant positions, and normalizes the statistical columns.

### `backend/app/services/feature_engineering.py`

Creates model features including:

- Previous-game statistics
- 3-game rolling averages
- 5-game rolling averages
- Season-to-date averages
- Target trend
- Carry trend
- Reception trend
- Yards per carry
- Yards per target
- Catch rate
- Passing yards per attempt

### `backend/app/services/model_service.py`

Contains the machine-learning prediction engine. It selects historical training data, trains position-specific models, predicts statistics, calculates fantasy points, generates approximate ranges, and performs historical backtests.

### `frontend/index.html`

Main browser interface.

### `frontend/app.js`

Uses the Fetch API to communicate with FastAPI and renders prediction/backtest results.

### `frontend/styles.css`

Contains responsive UI styling.

### `scripts/train.py`

Command-line interface for model testing, backtesting, and CSV generation.

## Installation

### 1. Enter the project directory

```bash
cd fantasy-football-predictor
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python run.py
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API

### Health Check

```text
GET /api/health
```

Example response:

```json
{
  "status": "ok"
}
```

### Generate Predictions

```text
GET /api/predictions
```

Parameters:

- `season`
- `week`
- `position`
- `limit`

Example:

```text
/api/predictions?season=2025&week=10&position=RB&limit=50
```

Position can be `ALL`, `QB`, `RB`, `WR`, or `TE`.

Example response:

```json
{
  "season": 2025,
  "week": 10,
  "count": 1,
  "predictions": [
    {
      "player_id": "00-1234567",
      "player_name": "Example Player",
      "position": "RB",
      "season": 2025,
      "week": 10,
      "projected_points": 18.7,
      "low": 13.2,
      "high": 24.2,
      "predicted_stats": {
        "rushing_yards": 74.5,
        "rushing_tds": 0.62,
        "receptions": 3.8,
        "receiving_yards": 31.4,
        "receiving_tds": 0.21
      }
    }
  ]
}
```

## Historical Backtesting

```text
GET /api/backtest?season=2025&week=10
```

The model trains only on information available before the requested week and compares its predictions with actual results.

Metrics include:

- MAE
- RMSE
- Within ±2 fantasy points
- Within ±4 fantasy points
- Within ±6 fantasy points

You can also run a backtest from the command line:

```bash
python scripts/train.py --season 2025 --week 10 --backtest
```

## Preventing Data Leakage

A critical requirement for sports prediction is preventing future information from entering the model.

Lagged features use `shift(1)`:

```python
df[f"{stat}_lag1"] = grouped[stat].shift(1)
```

Rolling features also use `shift(1)` before calculating averages.

Therefore, a Week 10 prediction can use Weeks 1-9 but cannot use Week 10 results.

```text
Weeks 1-9
    |
    v
Feature Engineering
    |
    v
Model
    |
    v
Predict Week 10
    |
    v
Compare with actual Week 10
```

## Fantasy Scoring

The initial application uses full-PPR scoring.

### Passing

- Passing yards: 0.04 points per yard
- Passing TD: 4 points
- Interception: -2 points

### Rushing

- Rushing yards: 0.10 points per yard
- Rushing TD: 6 points

### Receiving

- Reception: 1 point
- Receiving yards: 0.10 points per yard
- Receiving TD: 6 points

### Fumbles

- Lost fumble: -2 points

Because the model predicts football statistics before converting them to fantasy points, support can later be added for standard, half-PPR, full-PPR, and custom scoring.

## Position-Specific Predictions

### QB

- Passing yards
- Passing touchdowns
- Interceptions
- Rushing yards
- Rushing touchdowns

### RB

- Rushing yards
- Rushing touchdowns
- Receptions
- Receiving yards
- Receiving touchdowns

### WR

- Receptions
- Receiving yards
- Receiving touchdowns
- Rushing yards
- Rushing touchdowns

### TE

- Receptions
- Receiving yards
- Receiving touchdowns

## Command-Line Usage

Generate projections:

```bash
python scripts/train.py --season 2025 --week 10
```

Generate projections and run a historical backtest:

```bash
python scripts/train.py --season 2025 --week 10 --backtest
```

## CSV Exports

Command-line projections are stored in:

```text
data/exports/
```

Example:

```text
data/exports/predictions_2025_week_10.csv
```

## Development Roadmap

### Phase 1 — Baseline Model

- [x] Download historical NFL data
- [x] Calculate fantasy points
- [x] Generate lagged features
- [x] Generate rolling averages
- [x] Train position-specific models
- [x] Generate statistical predictions
- [x] Calculate projected fantasy points
- [x] Historical backtesting
- [x] FastAPI backend
- [x] Browser frontend
- [x] CSV exports

### Phase 2 — Matchup Intelligence

- [ ] NFL schedule integration
- [ ] Opponent defensive statistics
- [ ] Home/away indicator
- [ ] Team offensive strength
- [ ] Opponent fantasy points allowed
- [ ] Pass-defense strength
- [ ] Rush-defense strength
- [ ] Red-zone defense

### Phase 3 — Player Opportunity

- [ ] Snap percentage
- [ ] Target share
- [ ] Carry share
- [ ] Route participation
- [ ] Red-zone targets
- [ ] Red-zone carries
- [ ] Goal-line carries
- [ ] Depth-chart position

### Phase 4 — Availability

- [ ] Injury reports
- [ ] Player status
- [ ] Practice participation
- [ ] Returning-from-injury indicator
- [ ] Teammate injury effects

### Phase 5 — Game Context

- [ ] Weather
- [ ] Temperature
- [ ] Wind
- [ ] Precipitation
- [ ] Indoor/outdoor stadium
- [ ] Expected game total
- [ ] Expected point spread

### Phase 6 — Model Improvements

- [ ] Ridge regression baseline
- [ ] Random Forest
- [ ] Gradient Boosting comparison
- [ ] XGBoost
- [ ] Model ensembles
- [ ] Feature importance
- [ ] Hyperparameter optimization
- [ ] Time-series cross-validation
- [ ] Position-specific error models
- [ ] Calibrated prediction intervals

### Phase 7 — Fantasy League Integration

- [ ] Sleeper API
- [ ] Import fantasy league
- [ ] Import roster
- [ ] Custom league scoring
- [ ] Start/sit recommendations
- [ ] Waiver-wire recommendations
- [ ] Free-agent rankings
- [ ] Player comparisons

## Current Limitations

This version is an initial machine-learning baseline rather than a production forecasting service.

The model does not yet fully incorporate:

1. Opponent defensive strength
2. Injuries
3. Snap counts
4. Weather
5. Game-market information
6. Depth-chart changes
7. Formally calibrated prediction intervals
8. Schedule-based future rows for weeks that have not yet occurred

These are intended development steps.

## Model Evaluation Philosophy

The ML model should be compared against simple baselines such as:

- Previous week's fantasy points
- Season average
- 3-game average
- 5-game average

A more complex model is useful only if it consistently improves on those baselines.

Accuracy should also be measured independently for QB, RB, WR, and TE because each position has different week-to-week variance.

## Future Goal

The long-term application should answer questions such as:

- Who should I start this week?
- Which RB has the best matchup?
- Which waiver player has increasing usage?
- Which player is likely to outperform his season average?
- Which WR has the strongest target-share trend?
- How confident is the model in a prediction?
- Which available player gives my roster the largest projected improvement?

The eventual pipeline is:

```text
NFL Data
   |
   +-- Player Statistics
   +-- Schedule
   +-- Opponents
   +-- Injuries
   +-- Snap Counts
   +-- Depth Charts
   +-- Weather
   |
   v
Feature Engineering
   |
   v
Prediction Models
   |
   v
Player Projections
   |
   v
Fantasy League Analysis
   |
   +-- Start/Sit
   +-- Waiver Wire
   +-- Rankings
   +-- Player Comparison
```

## Disclaimer

Fantasy-football projections are probabilistic estimates. NFL performance can be affected by injuries, coaching decisions, game scripts, weather, turnovers, substitutions, and other events that cannot be reliably predicted.

Projection ranges should therefore be interpreted as estimates rather than guarantees.

## License

Add an appropriate project license before publicly distributing or commercializing the application. For an open-source project, the MIT License is a common option.
