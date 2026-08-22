# PahadSuraksha Backend

Flask API serving the landslide risk prediction app.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env` with your OpenWeather API key:
```
OPENWEATHER_API_KEY=your_key_here
```

## Running

### 1. Train the ML model (one-time)

```bash
python machine_learning/train_model.py
```

This creates a synthetic dataset and trains a Random Forest classifier, saving it to `machine_learning/landslide_model.pkl`. The model is used by the `/api/predict` endpoint.

**Note:** This model is trained on synthetic data. For production use, replace with real historical landslide data from geological surveys or USGS databases.

### 2. Initialize the database

```bash
python seed_db.py
```

Creates SQLite database at `instance/pahadsuraksha.db` with tables for users, districts, incidents, and predictions. Demo admin account:
- Email: `admin@pahadsuraksha.gov.in`
- Password: `ChangeMe123!` (change in production)

To use PostgreSQL instead of SQLite, set in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/pahadsuraksha
```

### 3. Start the server

```bash
python run.py
```

Server runs on **http://localhost:8000**

## API Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register` | — | Create account |
| POST | `/api/auth/login` | — | Login, returns JWT |
| GET | `/api/auth/me` | Bearer token | Current user info |
| GET | `/api/districts` | — | List all districts (for map) |
| GET | `/api/districts/stats` | — | Overall stats (incidents, users, etc.) |
| GET | `/api/districts/historical` | — | Monthly/yearly incident trends |
| POST | `/api/predict` | optional | Estimate landslide risk (rainfall, elevation, slope, etc.) |
| GET | `/api/weather?lat=X&lng=Y` | — | Current weather + 7-day forecast (cached) |
| GET | `/api/incidents` | — | List public incident reports |
| POST | `/api/incidents` | optional | Submit incident report (multipart) |
| PATCH | `/api/incidents/:id/approve` | admin | Approve report |
| PATCH | `/api/incidents/:id/reject` | admin | Reject report |
| GET | `/api/admin/users` | admin | List all users |
| GET | `/api/admin/analytics/districts` | admin | Risk summary by district |
| GET | `/api/admin/export.csv` | admin | Export incidents as CSV |
| GET | `/api/health` | — | Server health check |

## Code Organization

```
app/
  __init__.py        # Flask app factory, CORS setup
  config.py          # Config from environment
  extensions.py      # SQLAlchemy, JWT, etc.
  models/            # User, District, Incident, Prediction, etc.
  routes/            # Auth, Weather, Predict, Admin routes
  services/          # ML predictions, weather API calls
  utils/             # Decorators, helpers
machine_learning/
  train_model.py     # Generates synthetic data, trains Random Forest
  landslide_model.pkl # Saved trained model
```

## Development Notes

- **Weather caching:** OpenWeather API responses are cached in the database to avoid rate limits
- **JWT tokens:** Issued on login, checked on protected endpoints
- **Admin features:** Only users with `role='admin'` can approve incidents or access analytics
- **Multipart uploads:** Incident photos are temporarily stored in `backend/uploads/`

## Known Limitations

- Model trained on synthetic data (high confidence predictions are not guaranteed)
- Elevation API integration not yet complete
- No push notifications for saved locations
- Reports can't be filtered by user's own submissions
- No email alerts when incidents are approved/rejected
