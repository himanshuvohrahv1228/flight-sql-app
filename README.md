# ✈️ Flight Analytics Dashboard

A web-based Flight Analytics Dashboard built using **Streamlit**, **MySQL**, **Pandas**, and **Plotly**.  
This project allows users to search flights between cities and analyze flight data using interactive charts and insights.

## 🚀 Features

### 🔍 Check Flights
- Select **Source** and **Destination** cities
- View all available flights on a route
- Highlights:
  - 💰 Cheapest Flight
  - ⚡ Fastest Flight
- Handles edge cases:
  - Same source & destination
  - No flights available

### 📊 Analytics
- ✈️ Airline-wise flight distribution (Donut Chart)
- 🏙️ Top 10 busiest cities (Bar Chart)
- 📈 Monthly flight trend analysis (Line Chart)
- 🌐 Flights between cities visualization (Heatmap)

### 🎨 UI Highlights
- Background image with dark overlay
- Custom styled cards for insights
- Clean, professional dashboard layout
- 
## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** MySQL
- **Data Handling:** Pandas
- **Visualization:** Plotly
- **Language:** Python

## 📁 Project Structure

flight-sql-app/
│── app.py
│── dbhelper.py
│── requirements.txt
│── README.md
│── bg.jpg

yaml
Copy code

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
bash
git clone <your-repo-url>
cd flight-sql-app

2️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt

3️⃣ Configure MySQL

Create a database (e.g. flights)

Import flight data into MySQL

Update database credentials in dbhelper.py

4️⃣ Run the app
bash
Copy code
streamlit run app.py

🗄️ Database Tables Used
flights

Airline

Source

Destination

Route

Dep_Time

Arrival_Time

Duration

Price

📌 Use Cases
Flight price comparison

Identifying cheapest and fastest routes

Analyzing airline traffic

Visualizing flight trends over time

👨‍💻 Author
Himanshu Vohra
AIML Department
RGPV University

📜 License
This project is for educational purposes.
