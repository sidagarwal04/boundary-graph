# Boundary Graph - IPL Analytics Dashboard

A professional, high-performance cricket analytics platform for the Indian Premier League (IPL). This project uses a **Neo4j Graph Database** to store complex ball-by-ball relationships and a **Nuxt 3** frontend for stunning data visualization.

## 🔗 Live Demo
- **Frontend**: [boundary-graph.netlify.app](https://boundary-graph.netlify.app/)
- **Backend API**: [boundary-graph.onrender.com](https://boundary-graph.onrender.com/health)

## 🏗 Architecture
This project follows a modern distributed architecture:
- **Frontend**: Nuxt 3 (Vue.js) hosted on **Netlify**.
- **Backend**: FastAPI (Python) hosted on **Render**.
- **Database**: Neo4j Graph Database hosted on **Neo4j Aura Cloud**.

## 📊 Graph Data Model
The power of this dashboard comes from the underlying graph structure. Unlike traditional SQL databases, we can traverse relationships (like a bowler dismissing a specific batsman across multiple seasons) in milliseconds.

![Neo4j Graph Schema](visualisation.png)

### Model Explanation
- **Nodes**: Represent the entities (Players, Teams, Matches, Venues).
- **Relationships**: Connect entities (e.g., a `Player` `FACED` a `Delivery` in a `Match`).
- **Aggregated Stats**: We pre-calculate and store `BATTING_STATS` and `BOWLING_STATS` relationships directly between Players and Matches to ensure the dashboard loads instantly.

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- Node.js 20+
- Neo4j Instance (Local or Cloud)

### 1. Backend (FastAPI)
```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend
python -m uvicorn backend_api:app --reload --port 8000
```

### 2. Frontend (Nuxt 3)
```bash
cd frontend
npm install
npm run dev
```

## ⚙️ Configuration
Create a `.env` file in the root and another in the `frontend` folder based on the provided `example.env`.

**Backend Variables:**
- `NEO4J_URI`: Connection string (bolt/neo4j+s).
- `NEO4J_USERNAME`: Database user.
- `NEO4J_PASSWORD`: Database password.

**Frontend Variables:**
- `NUXT_PUBLIC_API_BASE`: URL of your running backend.

## 🛠 Features
- **Player Search**: Deep dive into individual career trajectories.
- **Head-to-Head**: Compare historical performance between any two franchises.
- **Team Insights**: Track rebranding history (e.g., Delhi Daredevils ➔ Delhi Capitals).
- **Trends**: Visualizing runs and wickets scored across all IPL seasons.

## 📄 License
This project is licensed under the [MIT License](LICENSE).

---
*Built with ❤️ for cricket fans and data enthusiasts.*
