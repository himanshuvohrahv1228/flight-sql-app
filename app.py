import streamlit as st
from dbhelper import DB
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://www.hajjumrahtech.com/images/flight-bg.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.65);
        z-index: -1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(
    page_title="Flight Analytics",
    layout="wide"
)


db = DB()

st.sidebar.title('Flight Analytics')
user_option = st.sidebar.selectbox('Menu',['Select One','Check Flights','Analytics'])

if user_option == 'Check Flights':

    st.markdown(
        "<h1 style='color:#60a5fa'>Check Flights</h1>",
        unsafe_allow_html=True
    )

    col1,col2 = st.columns(2)
    city = db.fetch_city_names()
    with col1:
        source = st.selectbox('Source', sorted(city))
    with col2:
        destination = st.selectbox('Destination', sorted(city))

    if st.button('Search'):

        if source == destination:
            st.markdown(
                """
                <div style="
                    background: rgba(220, 38, 38, 0.95);
                    color: white;
                    padding: 15px 20px;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: 600;
                    margin-top: 15px;
                    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
                ">
                    🚫 Source and Destination cannot be the same. Please select different cities.
                </div>
                """,
                unsafe_allow_html=True
            )
            st.stop()

        #FETCH ALL FLIGHTS
        results = db.fetch_all_flights(source, destination)

        if not results:
            st.info("ℹ️ No flights found for this route.")
            st.stop()

        #CHEAPEST FLIGHT
        cheap = db.cheapest_flight(source, destination)
        if cheap:
            airline_c, price = cheap
            st.markdown(
                f"""
                <div style="
                    background: rgba(34, 197, 94, 0.9);
                    color: white;
                    padding: 15px 20px;
                    border-radius: 12px;
                    font-size: 16px;
                    font-weight: 600;
                    margin-top: 15px;
                ">
                    💰 Cheapest Flight: <b>{airline_c}</b> – ₹{price}
                </div>
                """,
                unsafe_allow_html=True
            )

        #FLIGHTS TABLE
        df = pd.DataFrame(
            results,
            columns=["Airline", "Route", "Dep_Time", "Arrival_Time", "Duration", "Price"]
        )
        df.index = df.index + 1
        st.dataframe(df)

elif user_option == 'Analytics':

    st.markdown(
        "<h1 style='color:#60a5fa'>Analytics</h1>",
        unsafe_allow_html=True
    )

    #Pie Chart


    airline,freq = db.fetch_airline_freq()

    total_flights = sum(freq)
    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=freq,
            hole=0.45,
            textinfo="percent",
            hoverinfo="label+value+percent",
            pull=0.05
        )
    )

    fig.update_layout(
        title="Flight Distribution by Airline",
        template="plotly_dark",
        annotations=[
            dict(
                text="<b>Air Traffic</b><br>Overview",
                x=0.5,
                y=0.5,
                font_size=18,
                showarrow=False
            )
        ]
    )

    st.plotly_chart(fig, use_container_width=True)
    #BAR CHART
    col1, col2 = st.columns([1, 1.3])

    with col1:
        city, freq1 = db.busy_airport()

        df_city = pd.DataFrame({
            "City": city,
            "Flights": freq1
        })
        df_city = df_city.sort_values("Flights", ascending=False).head(10)

        fig_bar = px.bar(
            df_city,
            x="City",
            y="Flights",
            text="Flights",
            title="Top 10 Cities by Number of Flights",
            color="Flights",
            color_continuous_scale="Blues"
        )

        fig_bar.update_traces(
            textposition="outside"
        )

        fig_bar.update_layout(
            template="plotly_dark",
            height=500,
            xaxis_tickangle=-45,
            margin=dict(l=40, r=20, t=70, b=80),
            coloraxis_showscale=False
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    #Line Chart

    with col2:
        date, freq2 = db.daily_freq()
        df_date = pd.DataFrame({
            "Date": date,
            "Flights": freq2
        })

        df_date["Date"] = pd.to_datetime(df_date["Date"])
        df_monthly = (
            df_date
            .groupby(pd.Grouper(key="Date", freq="M"))
            .sum()
            .reset_index()
        )

        # Smooth line + hover
        fig = px.line(
            df_monthly,
            x="Date",
            y="Flights",
            title="Monthly Flights Trend (2019–2025)",
            markers=False
        )

        fig.update_traces(
            line=dict(width=3, shape="spline"),  # 🔥 smooth curve
            hovertemplate=
            "<b>Month:</b> %{x|%b %Y}<br>"
            "<b>Flights:</b> %{y}<extra></extra>"
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Month",
            yaxis_title="Number of Flights",
            height=500
        )
        fig.update_traces(
            mode="lines+markers",
            marker=dict(size=6),
            line=dict(width=3, shape="spline")
        )

        st.plotly_chart(fig, use_container_width=True, key="monthly_smooth_trend")

    #Heatmap

    source, destination, freq = db.flight_bw_cities()

    df_route = pd.DataFrame({
        "Source": source,
        "Destination": destination,
        "Flights": freq
    })

    fig = px.density_heatmap(
        df_route,
        x="Source",
        y="Destination",
        z="Flights",
        color_continuous_scale="Blues",
        title="Flights Between Cities (Route Intensity)"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Source City",
        yaxis_title="Destination City",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True, key="route_heatmap")
else:
    st.markdown(
        """
        <h1 style="
            text-align: center;
            font-size: 56px;
            font-weight: 800;
            margin-top: 40px;
            margin-bottom: 10px;
            color: #F9FAFB;
        ">
            ✈️ Welcome to Flight Analytics Dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            background: rgba(17, 24, 39, 0.85);
            padding: 40px 30px;
            border-radius: 18px;
            max-width: 950px;
            margin: 40px auto;
            box-shadow: 0 20px 40px rgba(0,0,0,0.45);
            backdrop-filter: blur(8px);
            text-align: center;
        ">
            <p style="
                color: #e5e7eb;
                font-size: 20px;
                line-height: 1.6;
                margin: 0;
            ">
                Explore comprehensive insights into airline operations, flight routes,
                pricing trends, and traffic patterns.
                <br><br>
                Use this dashboard to compare flights, identify the cheapest and fastest routes,
                analyze city-wise traffic, and track flight trends over time — all in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
