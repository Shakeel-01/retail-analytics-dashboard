# Real-Time Sales Dashboard

🔗 **Live API:** https://retail-analytics-api-wnev.onrender.com
🔗 **Live Dashboard:** https://retail-analytics-dashboard.onrender.com  
📖 **API Docs:** https://retail-analytics-api-wnev.onrender.com/docs
## Stack
- **Data:** pandas, numpy
- **ML / Forecasting:** scikit-learn (LinearRegression)
- **API:** FastAPI + Uvicorn
- **Frontend:** Streamlit + Plotly
- **Deployment:** Render / Railway

## Setup

### 1. Get the dataset
Download [Superstore Sales](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) and save as `data/superstore.csv`.

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the API
```bash
uvicorn src.api:app --reload
```
API docs auto-generated at: http://localhost:8000/docs

### 4. Run the dashboard (new terminal)
```bash
streamlit run app.py
```
Dashboard at: http://localhost:8501

## API Endpoints
| Endpoint | Description |
|---|---|
| `GET /summary` | KPIs: revenue, profit, orders, margins |
| `GET /top-products?n=10` | Top N products by revenue |
| `GET /regional-breakdown` | Sales & profit by region |
| `GET /monthly-trend` | Month-by-month trend |
| `GET /category-breakdown` | Revenue by product category |
| `GET /forecast?days=30` | 30-day sales forecast with confidence intervals |

## Deployment (Render)
1. Push to GitHub
2. New Web Service → connect repo
3. Start command: `uvicorn src.api:app --host 0.0.0.0 --port $PORT`
4. Deploy Streamlit as a second service: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
