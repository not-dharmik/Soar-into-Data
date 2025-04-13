
# 🛰️ UCI TSP Mapper

An intelligent route optimization tool built by UCI students for the **"Soar Into Data" Datathon** hosted by **Data @UCI**. This project leverages Melissa APIs and OR-Tools to help users discover the shortest path for errands around UCI, whether using a fixed list (Static) or selecting dynamically (Dynamic).

---

You can view the website [here](https://not-dharmik.github.io/Soar-into-Data/). Though for full functionality, you will have to run the backend on terminal.

## 📖 Project Summary

Our tool uses **Melissa APIs** to enrich a dataset of addresses near UCI with the following:

- 🧭 **Geolocation** (Latitude, Longitude)
- 🏠 **Residential or Business classification**
- 🆔 **Melissa Address Keys (MAK)**

Once enriched, the project applies the **Travelling Salesman Problem (TSP)** algorithm to calculate the most efficient round-trip route.

> 🚶 Ideal for students new to Irvine who depend on walking, cycling, or public transport for their errands.  
> 🌎 Reduces time, effort, and carbon footprint.  
> 🔭 Potential future: Chrome/Maps extension with Melissa-powered navigation.

---

## ⚙️ Tool Modes

### 🔵 Static Route
- Input: Pre-defined dataset (Excel file)
- Output: Optimal round-trip route starting and ending at UCI
- Use Case: Batch route analysis or delivery route visualization

### 🟢 Dynamic Route
- Input: User-selected locations from the dataset
- Output: Optimal route from user-selected starting point through selected stops
- Use Case: Personalized errands, real-time planning

---

## 🧠 Hackathon Theme Integration

This tool embraces the theme **“Soar Into Data”** by:
- Turning raw address data into valuable route intelligence
- Leveraging APIs to uncover hidden patterns in address types and geographies
- Helping users **optimize mobility through data**

---

## 🛠️ Tech Stack

| Layer        | Tech Stack                               |
|--------------|-------------------------------------------|
| Frontend     | HTML, CSS, Leaflet.js                     |
| Backend      | Python, FastAPI, Google OR-Tools, Pandas  |
| Data Enrich  | Melissa APIs                              |
| Visualization| Leaflet.js (Map & Route Plotting)         |

---

## 🔍 Features

- 🔁 Route optimization with round-trip support
- 🗺️ Beautiful route visualization with Leaflet.js
- 🧠 Smart start-point selection for dynamic routing
- ⚡ Real-time backend with FastAPI and reload support
- 📈 Displays total route distance with dynamic color-coded markers

---

## 🚀 Getting Started

### 1. Clone the repo

\`\`\`bash
git clone https://github.com/not-dharmik/Soar-into-Data
\`\`\`

### 2. Setup Python backend

\`\`\`bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
\`\`\`

Make sure you have your dataset in \`backend/data/dataset.xlsx\`.

### 3. Run Backend

\`\`\`bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
\`\`\`

### 4. Run Frontend (from root or \`frontend/\`)

\`\`\`bash
cd frontend
python3 -m http.server 3000
\`\`\`

Visit: [http://localhost:3000/static.html](http://localhost:3000/static.html)

---

## 📂 Repository Structure

\`\`\`
├── backend/
│   ├── main.py
│   ├── tsp_solver.py
│   └── data/dataset.xlsx
├── frontend/
│   ├── static.html
│   ├── dynamic.html
│   ├── team.html
│   ├── index.html
│   └── css/style.css
└── README.md
\`\`\`

---

## 👥 Team

- **Dharmik Naicker**
- **Shrushti Mehta** 
- **Yash Deole**

---
