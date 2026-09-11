import streamlit as st
import pandas as pd
import joblib

# ==========================
# Load Model
# ==========================
model = joblib.load("model/passenger_satisfaction_model.pkl")

# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="Airline Passenger Satisfaction Prediction System",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================
# Custom CSS
# ==========================
st.markdown(
    """
    <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1100px;
        }
        h1 {
            font-size: 32px !important;
        }
        .app-subtitle {
            color: #6b7280;
            font-size: 16px;
            margin-top: -8px;
            margin-bottom: 1.5rem;
        }
        div[data-testid="stExpander"] {
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        div[data-testid="stMetric"] {
            background-color: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 10px 14px;
        }
        .stButton > button {
            width: 100%;
            padding: 0.6rem;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
        }
        .result-card {
            padding: 1.2rem 1.5rem;
            border-radius: 12px;
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================
# Header
# ==========================
st.markdown(
    """
    <h1>✈️ Airline Passenger Satisfaction Prediction System</h1>
    <div class="app-subtitle">Enter passenger and flight details to predict customer satisfaction.</div>
    """,
    unsafe_allow_html=True,
)

# ==========================
# Passenger Information
# ==========================
with st.expander("👤 Passenger Information", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        gender = st.selectbox("Gender", ["Female", "Male"])
        travel_type = st.selectbox("Type of Travel", ["Business Travel", "Personal Travel"])
    with col2:
        customer_type = st.selectbox("Customer Type", ["Loyal Customer", "Disloyal Customer"])
        travel_class = st.selectbox("Class", ["Business", "Eco", "Eco Plus"])
    with col3:
        age = st.number_input("Age", min_value=7, max_value=100, value=30)
        flight_distance = st.number_input("Flight Distance", min_value=0, value=1000)

# ==========================
# Service Ratings
# ==========================
with st.expander("⭐ Service Ratings (0–5)", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        wifi = st.slider("Inflight Wifi Service", 0, 5, 3)
        online_booking = st.slider("Ease of Online Booking", 0, 5, 3)
        gate_location = st.slider("Gate Location", 0, 5, 3)
        food_drink = st.slider("Food and Drink", 0, 5, 3)

    with col2:
        online_boarding = st.slider("Online Boarding", 0, 5, 3)
        seat_comfort = st.slider("Seat Comfort", 0, 5, 3)
        entertainment = st.slider("Inflight Entertainment", 0, 5, 3)
        onboard_service = st.slider("On-board Service", 0, 5, 3)

    with col3:
        legroom = st.slider("Leg Room Service", 0, 5, 3)
        baggage = st.slider("Baggage Handling", 0, 5, 3)
        checkin = st.slider("Check-in Service", 0, 5, 3)
        inflight_service = st.slider("Inflight Service", 0, 5, 3)

    cleanliness = st.slider("Cleanliness", 0, 5, 3)

# ==========================
# Flight Details
# ==========================
with st.expander("🛫 Flight Details", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        departure_arrival = st.slider("Departure/Arrival Time Convenient", 0, 5, 3)
    with col2:
        departure_delay = st.number_input("Departure Delay (Minutes)", min_value=0, value=0)
    with col3:
        arrival_delay = st.number_input("Arrival Delay (Minutes)", min_value=0, value=0)

# ==========================
# Encoding
# ==========================

gender_map = {
    "Female": 0,
    "Male": 1
}

customer_map = {
    "Loyal Customer": 0,
    "Disloyal Customer": 1
}

travel_map = {
    "Business Travel": 0,
    "Personal Travel": 1
}

class_map = {
    "Business": 0,
    "Eco": 1,
    "Eco Plus": 2
}

# ==========================
# Feature Engineering
# ==========================

total_delay = departure_delay + arrival_delay

delayed_flight = 1 if total_delay > 15 else 0

average_service_rating = (
    wifi +
    online_booking +
    food_drink +
    online_boarding +
    seat_comfort +
    entertainment +
    onboard_service +
    legroom +
    baggage +
    checkin +
    inflight_service +
    cleanliness
) / 12

long_haul = 1 if flight_distance > 3000 else 0

# ==========================
# Predict
# ==========================

st.markdown("")
predict_clicked = st.button("🔮 Predict Satisfaction")

if predict_clicked:

    input_df = pd.DataFrame([{
        'Gender': gender_map[gender],
        'Customer Type': customer_map[customer_type],
        'Age': age,
        'Type of Travel': travel_map[travel_type],
        'Class': class_map[travel_class],
        'Flight Distance': flight_distance,
        'Inflight wifi service': wifi,
        'Departure/Arrival time convenient': departure_arrival,
        'Ease of Online booking': online_booking,
        'Gate location': gate_location,
        'Food and drink': food_drink,
        'Online boarding': online_boarding,
        'Seat comfort': seat_comfort,
        'Inflight entertainment': entertainment,
        'On-board service': onboard_service,
        'Leg room service': legroom,
        'Baggage handling': baggage,
        'Checkin service': checkin,
        'Inflight service': inflight_service,
        'Cleanliness': cleanliness,
        'Departure Delay in Minutes': departure_delay,
        'Arrival Delay in Minutes': arrival_delay,
        'Total_Delay': total_delay,
        'Delayed_Flight': delayed_flight,
        'Average_Service_Rating': average_service_rating,
        'Long_Haul': long_haul
    }])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]

    st.markdown("---")
    st.subheader("Prediction Result")

    if prediction == 1:
        st.success(f"😊 **Satisfied Passenger**\n\nConfidence: {probability[1]*100:.2f}%")
    else:
        st.error(f"☹️ **Dissatisfied Passenger**\n\nConfidence: {probability[0]*100:.2f}%")
