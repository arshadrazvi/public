# Fantasy Football Weekly Predictor

Full-stack NFL fantasy-football projection starter.

## Stack

- Backend: FastAPI
- ML: scikit-learn HistGradientBoostingRegressor
- NFL data: nflverse via nflreadpy
- Frontend: HTML/CSS/JavaScript
- Storage: local model/cache/export directories

## Directory layout

```text
fantasy-football-predictor/
├── backend/
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── schemas.py
│       └── services/
│           ├── __init__.py
│           ├── data_service.py
│           ├── feature_engineering.py
│           └── model_service.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── scripts/
│   └── train.py
├── data/
│   ├── cache/
│   ├── models/
│   └── exports/
├── requirements.txt
├── run.py
├── .gitignore
└── README.md
```

## Setup

```bash
cd fantasy-football-predictor

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the web app

```bash
python run.py
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Train/test from command line

Historical backtest:

```bash
python scripts/train.py --season 2025 --week 10 --backtest
```

Generate projections:

```bash
python scripts/train.py --season 2025 --week 10
```


## Frontend Sorting and Filtering

After **Load Projections** completes, the browser keeps the returned projection set in memory.

The following controls do **not** call the prediction API again:

- Position filter
- Team filter
- Player-name search
- Minimum projected points
- Sort field
- Sort direction
- Clickable table-column sorting

A new model/API request is made only when **Load Projections** is clicked for a season/week.

## API

Health:

```text
GET /api/health
```

Predictions:

```text
GET /api/predictions?season=2025&week=10&position=ALL&limit=100
```

Backtest:

```text
GET /api/backtest?season=2025&week=10
```

Refresh downloaded data:

```text
POST /api/refresh?end_season=2025
```

## Important modeling note

Historical prediction rows use lagged/rolling features with `shift(1)`, so the result from the week being predicted is not included in its own features.

This starter intentionally focuses on player history and usage. The next production improvement should add opponent strength, schedules, injuries, snap share, weather and game-market context.
