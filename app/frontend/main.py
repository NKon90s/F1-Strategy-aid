import streamlit as st
import pandas as pd
import requests 


 
st.set_page_config(
    page_title="F1 Strategy Aid",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(220, 0, 0, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 90%,
                rgba(220, 0, 0, 0.12),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #080808 0%,
                #111111 45%,
                #050505 100%
            );

        color: #ffffff;
    }

    /* Carbon-fiber style overlay */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;

        background-image:
            linear-gradient(
                45deg,
                rgba(255,255,255,0.015) 25%,
                transparent 25%
            ),
            linear-gradient(
                -45deg,
                rgba(255,255,255,0.015) 25%,
                transparent 25%
            );

        background-size: 8px 8px;
        pointer-events: none;
        z-index: 0;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
        position: relative;
        z-index: 1;
    }


    /* ---------- HEADER ---------- */

    .f1-header {
    position: relative;

    background:
        linear-gradient(
            135deg,
            #111111,
            #090909
        );

    border: 1px solid #292929;

    border-left: 5px solid #e10600;

    border-radius: 14px;

    padding: 28px 32px;

    margin-bottom: 25px;

    box-shadow:
        0 15px 45px rgba(0,0,0,0.45);
}


.f1-header::after {
    content: "";

    position: absolute;

    right: 0;
    top: 0;

    width: 35%;

    height: 100%;

    background:
        linear-gradient(
            135deg,
            transparent 0%,
            rgba(225,6,0,0.06) 100%
        );

    pointer-events: none;
    }

    .f1-title {
    font-size: 44px;

    font-weight: 900;

    letter-spacing: -2px;

    line-height: 1;

    color: #ffffff;
}

.f1-title span {
    color: #e10600;
}

.f1-subtitle {
    margin-top: 10px;

    color: #999999;

    font-size: 14px;

    letter-spacing: 0.5px;
}


    /* ---------- SECTION CARDS ---------- */

    .section-card {
        background: rgba(20, 20, 20, 0.92);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow:
            0 10px 35px rgba(0,0,0,0.35);
    }

    .section-title {
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 15px;
        color: #ffffff;
    }

    .section-title::before {
        content: "";
        display: inline-block;
        width: 4px;
        height: 18px;
        background: #e10600;
        margin-right: 10px;
        vertical-align: -2px;
        border-radius: 2px;
    }


    /* ---------- STREAMLIT LABELS ---------- */

    label {
        color: #d0d0d0 !important;
        font-weight: 600 !important;
    }


    /* ---------- SELECT BOX ---------- */

    div[data-baseweb="select"] > div {
        background-color: #1b1b1b !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        color: white !important;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #e10600 !important;
    }


    /* ---------- SLIDERS ---------- */

    div[data-testid="stSlider"] {
        padding-top: 10px;
    }


    /* ---------- BUTTON ---------- */

    .stButton > button {
        width: 100%;

        background: linear-gradient(
            90deg,
            #e10600,
            #b00000
        );

        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 800;
        font-size: 16px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(
            90deg,
            #ff1b12,
            #d00000
        );

        transform: translateY(-2px);

        box-shadow:
            0 8px 20px rgba(225,6,0,0.25);
    }


    /* ---------- STRATEGY RESULT ---------- */

    .strategy-result {
        background:
            linear-gradient(
                135deg,
                rgba(225,6,0,0.18),
                rgba(25,25,25,0.95)
            );

        border: 1px solid rgba(225,6,0,0.35);
        border-radius: 14px;
        padding: 25px;
        margin-top: 10px;
    }

    .strategy-label {
        color: #a8a8a8;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 1.5px;
        font-weight: 700;
    }

    .strategy-main {
        font-size: 30px;
        font-weight: 900;
        margin: 5px 0 15px;
        color: white;
    }

    .strategy-main span {
        color: #e10600;
    }


    /* ---------- METRICS ---------- */

    .metric-card {
        background: #151515;
        border: 1px solid #292929;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }

    .metric-label {
        font-size: 11px;
        text-transform: uppercase;
        color: #888;
        letter-spacing: 1px;
    }

    .metric-value {
        font-size: 22px;
        font-weight: 800;
        margin-top: 5px;
        color: white;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #666;
        font-size: 12px;
        margin-top: 35px;
        padding-top: 20px;
        border-top: 1px solid #222;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA
# ============================================================

drivers = [
    "Max Verstappen",
    "Lando Norris",
    "Charles Leclerc",
    "Lewis Hamilton",
    "Oscar Piastri",
    "George Russell",
    "Fernando Alonso",
    "Carlos Sainz",
    "Sergio Perez",
    "Lance Stroll"
]

grand_prix = [
    "Bahrain Grand Prix",
    "Saudi Arabian Grand Prix",
    "Australian Grand Prix",
    "Japanese Grand Prix",
    "Emilia-Romagna Grand Prix",
    "Monaco Grand Prix",
    "Spanish Grand Prix",
    "Canadian Grand Prix",
    "Austrian Grand Prix",
    "British Grand Prix",
    "Belgian Grand Prix",
    "Hungarian Grand Prix",
    "Dutch Grand Prix",
    "Italian Grand Prix",
    "Azerbaijan Grand Prix",
    "Singapore Grand Prix",
    "United States Grand Prix",
    "Mexico City Grand Prix",
    "São Paulo Grand Prix",
    "Las Vegas Grand Prix",
    "Qatar Grand Prix",
    "Abu Dhabi Grand Prix"
]

weather_options = [
    "No rain",
    "Light rain",
    "Heavy rain"
]


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="f1-header">

    <div class="f1-title">
        F1 <span>STRATEGY AID</span>
    </div>

    <div class="f1-subtitle">
        Race strategy decision support system
        • Tyres • Weather • Track Conditions • Race Position
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown("""
<div class="section-card">

<div class="section-title">
    Race Configuration
</div>

</div>
""", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)


with col1:

    driver = st.selectbox(
        "Driver",
        drivers
    )

    grid_position = st.selectbox(
        "Starting Grid Position",
        list(range(1, 21))
    )


with col2:

    selected_gp = st.selectbox(
        "Grand Prix",
        grand_prix
    )

    weather = st.selectbox(
        "Rain Expectation",
        weather_options
    )

 
with col3:

    asphalt_temperature = st.slider(
        "Asphalt Temperature (°C)",
        min_value=15,
        max_value=65,
        value=35,
        step=1
    )

    air_temperature = st.slider(
        "Air Temperature (°C)",
        min_value=5,
        max_value=50,
        value=25,
        step=1
    )



# ============================================================
# STRATEGY CALCULATION
# ============================================================


def calculate_strategy(
    weather,
    asphalt_temperature,
    air_temperature,
    grid_position,
    tyre_degradation,
    safety_car_probability
):

    # Wet conditions
    if weather == "Heavy rain":

        return (
            "INTERMEDIATE / WET",
            "Prioritize wet-weather tyre management. "
            "Avoid aggressive early stints and monitor the crossover point."
        )

    if weather == "Light rain":

        return (
            "INTERMEDIATE",
            "Track conditions may evolve rapidly. "
            "Monitor rainfall intensity and be ready for a crossover."
        )

    # Dry conditions
    if asphalt_temperature >= 45:

        strategy = "HARD → MEDIUM"

        explanation = (
            "High track temperature increases tyre degradation. "
            "A longer first stint on the Hard compound can reduce "
            "thermal degradation."
        )

    elif tyre_degradation == "High":

        strategy = "MEDIUM → HARD"

        explanation = (
            "High degradation favors protecting the tyres and "
            "extending the first stint."
        )

    elif grid_position <= 5:

        strategy = "MEDIUM → HARD"

        explanation = (
            "Starting near the front allows a conservative "
            "one-stop strategy while protecting track position."
        )

    else:

        strategy = "SOFT → MEDIUM → HARD"

        explanation = (
            "A more aggressive opening stint can provide opportunities "
            "to gain positions before settling into a longer strategy."
        )

    # Safety car adjustment
    if safety_car_probability == "High":

        explanation += (
            " High Safety Car probability increases the value of "
            "keeping strategic flexibility for a cheap pit stop."
        )

    return strategy, explanation


# ============================================================
# CALCULATE BUTTON
# ============================================================

st.markdown("")

if st.button("🏎️  GENERATE STRATEGY"):

    strategy, explanation = calculate_strategy(
        weather,
        asphalt_temperature,
        air_temperature,
        grid_position
    )

    st.markdown(f"""
    <div class="strategy-result">

        <div class="strategy-label">
            Recommended Strategy
        </div>

        <div class="strategy-main">
            {strategy}
        </div>

        <div style="
            color:#c0c0c0;
            line-height:1.6;
            font-size:15px;
        ">
            {explanation}
        </div>

    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # SUMMARY METRICS
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Driver</div>
            <div class="metric-value">{driver.split()[-1]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Grid</div>
            <div class="metric-value">P{grid_position}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Track Temp</div>
            <div class="metric-value">{asphalt_temperature}°C</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Rain Expectation</div>
            <div class="metric-value">{weather}</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    F1 Strategy Aid • Decision support prototype •
    Strategy recommendations are illustrative
</div>
""", unsafe_allow_html=True)

