import streamlit as st
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
    "Max VERSTAPPEN",
    "Lando NORRIS",
    "Charles LECLERC",
    "Lewis HAMILTON",
    "Oscar PIASTRI",
    "George RUSSEL",
    "Fernando ALONSO",
    "Carlos SAINZ",
    "Sergio PEREZ",
    "Lance STROLL"
]

grand_prix = [
    'Bahrain Grand Prix', 
    'Saudi Arabian Grand Prix',
    'Australian Grand Prix', 
    'Azerbaijan Grand Prix',
    'Miami Grand Prix', 
    'Monaco Grand Prix', 
    'Spanish Grand Prix',
    'Canadian Grand Prix', 
    'Austrian Grand Prix', 
    'British Grand Prix',
    'Hungarian Grand Prix', 
    'Belgian Grand Prix', 
    'Dutch Grand Prix',
    'Italian Grand Prix', 
    'Singapore Grand Prix',
    'Japanese Grand Prix', 
    'Qatar Grand Prix',
    'United States Grand Prix', 
    'Mexico City Grand Prix',
    'São Paulo Grand Prix', 
    'Las Vegas Grand Prix',
    'Abu Dhabi Grand Prix', 
    'Chinese Grand Prix',
    'Emilia Romagna Grand Prix'
    
]


weather_options = [
    "No rain",
    "Light rain",
    "Heavy rain"
]


safety_car_options = [
    "Low",
    "Medium",
    "High"
]



# ============================================================
# HEADER
# ============================================================

f1_header_html=f"""
<div class="f1-header">
    <div class="f1-title">
        F1 <span>STRATEGY AID</span>
    </div>
    <div class="f1-subtitle">
        Race strategy decision support system
        • Tyres • Weather • Track Conditions • Race Position
    </div>
</div>
"""
st.markdown(f1_header_html, unsafe_allow_html=True)

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

    tyre_age_at_start = st.selectbox(
        "Tyre Degradation",
        list(range(0,6))
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

    safety_car_probability = st.selectbox(
        "Safety Car Probability",
        safety_car_options
    )

 
with col3:

    asphalt_temperature = st.slider(
        "Asphalt Temperature (°C)",
        min_value=15.0,
        max_value=65.0,
        value=35.0,
        step=0.1
    )

    air_temperature = st.slider(
        "Air Temperature (°C)",
        min_value=5.0,
        max_value=50.0,
        value=25.0,
        step=0.1
    )

#======================================================
# PREDICTION API AND ITS ENDPOINTS
#======================================================

# URL of the API
API_URL = "http://api:8000"
# endpoints of the API
predict_compound = f"/predict-compound"
predict_stint = f"/predict-stint"
fetch_compound_data = f"/fetch-compound-data"
fetch_stint_data = f"/fetch-stint-data"
simulate_race = f"/simulate-race"


# ============================================================
# STRATEGY CALCULATION
# ============================================================

def second_best_compound(compounds: dict):
    """
    This function selects the second best compound for alternative strategy

    :param compounds: It recieves a dictionary as an input that contains probailities of HARD, MEDIUM and SOFT compounds
    """
    data = {
        "prob_hard":compounds['prob_hard'],
        "prob_med":compounds['prob_med'],
        "prob_soft":compounds['prob_soft']
    }

    comp = {
        "prob_hard": "HARD",
        "prob_med": "MEDIUM",
        "prob_soft": "SOFT"
    }

    probs = [compounds['prob_hard'], compounds['prob_med'], compounds['prob_soft']]
    probs_sorted = sorted(probs)
    for key, value in data.items():
        if value == probs_sorted[1]:
            return comp[key]

    return compounds['predicted_compound']


def fetch_compounds(driver, selected_gp, asphalt_temperature, grid_position):
    """
    This function helps to fetch the compounds for the driver
    
    :param driver: The name of the driver
    :param selected_gp: The name of the selected Grand Prix
    :param asphalt_temperature: the temp of the tarmac in celsius
    :param grid_position: the starting position of the driver
    """

    data = {
        "driver": driver,
        "grid_position": grid_position,
        "asphalt_temperature": asphalt_temperature,
        "selected_gp": selected_gp
    }

    try:
        compound_data_response = requests.post(API_URL + fetch_compound_data, json = data)
        compound_data_response.raise_for_status()
        compound_data = compound_data_response.json()
        compound_response = requests.post(API_URL + predict_compound, json = compound_data)
        compound_response.raise_for_status()
        compound_prediction = compound_response.json()

    except requests.exceptions.RequestException as e:
        print(f"Failed pulling {predict_compound} data: {e}")

    starting_compound = compound_prediction['starting_compound']
    alt_starting_compound = second_best_compound(compound_prediction)

    return starting_compound, alt_starting_compound
 

def determine_first_stints(driver, selected_gp, asphalt_temperature, grid_position):
    """
    This function calculates the first stint on a given compound with the help of linear regression
        
    :param driver: The name of the driver
    :param selected_gp: The name of the selected Grand Prix
    :param asphalt_temperature: the temp of the tarmac in celsius
    :param grid_position: the starting position of the driver
    """

    starting_compound, alt_starting_compound = fetch_compounds(driver, selected_gp, asphalt_temperature, grid_position)

    stint_data = {
        "driver": driver,
        "grid_position": grid_position,
        "asphalt_temperature": asphalt_temperature,
        "selected_gp": selected_gp,
        "starting_compound": starting_compound
        }

    alt_stint_data = {
        "driver": driver,
        "grid_position": grid_position,
        "asphalt_temperature": asphalt_temperature,
        "selected_gp": selected_gp,
        "starting_compound": alt_starting_compound
        }
    try:
        stint_data_response = requests.post(API_URL + fetch_stint_data, json = stint_data)
        stint_data_response.raise_for_status()
        stint_features = stint_data_response.json()
        stint_response = requests.post(API_URL + predict_stint, json = stint_features)
        stint_response.raise_for_status()
        stint_prediction = stint_response.json()

    except requests.exceptions.RequestException as e:
        print(f"Failed pulling {predict_stint} data: {e}")

    first_stint = stint_prediction['first_stint_length']

    try:
        alt_stint_data_response = requests.post(API_URL + fetch_stint_data, json = alt_stint_data)
        alt_stint_data_response.raise_for_status()
        alt_stint_features = alt_stint_data_response.json()
        alt_stint_response = requests.post(API_URL + predict_stint, json = alt_stint_features)
        alt_stint_response.raise_for_status()
        alt_stint_prediction = alt_stint_response.json()

    except requests.exceptions.RequestException as e:
        print(f"Failed pulling alternative {predict_stint} data: {e}")

    alt_first_stint = alt_stint_prediction['first_stint_length']

    return first_stint, alt_first_stint

 
def top_two_strategies(strat: dict, alt_strat: dict):

    """
    This function return the two fastet strategies from recommended and alterntive strategy
                
    :param strat: The dict that contains the recommended strategy
    :param alt_strat: the dict that contain an alternative strategy

    """
 
    strat1 = strat['recommended_strategy']
    strat2 = strat['alternative_strategy']
    strat3 = alt_strat['recommended_strategy']
    strat4 = alt_strat['alternative_strategy']

    strats_idx = ['strat1', 'strat2', 'strat3', 'strat4']
    strats = [strat1, strat2, strat3, strat4]
    t_strats = [strat1['race_time'], strat2['race_time'], strat3['race_time'], strat4['race_time']]
    hash_map = {}
    strat_map = {}
 
    for i, s in enumerate(strats_idx):
        hash_map[s] = t_strats[i]

    for i, s in enumerate(strats_idx):
        strat_map[s] = strats[i]
    
    t_strats.sort()

    for _, s in enumerate(strats_idx):
        if t_strats[0] == hash_map[s]:
            main_strategy = strat_map[s]
        if t_strats[1] == hash_map[s]:
            alt_strategy = strat_map[s]

    return main_strategy, alt_strategy
 

def simulate_strategy(driver, selected_gp, asphalt_temperature, grid_position):
    """
    This function simulates the recommended and the alternative tyre strategies.
            
    :param driver: The name of the driver
    :param selected_gp: The name of the selected Grand Prix
    :param asphalt_temperature: the temp of the tarmac in celsius
    :param grid_position: the starting position of the driver
    """

    starting_compound, alt_starting_compound = fetch_compounds(driver, selected_gp, asphalt_temperature, grid_position)
    first_stint, alt_first_stint = determine_first_stints(driver, selected_gp, asphalt_temperature, grid_position)

    simulation_data = {
        "driver": driver,
        "selected_gp": selected_gp,
        "starting_compound": starting_compound,
        "first_stint": first_stint
        }

    alt_simulation_data = {
        "driver": driver,
        "selected_gp": selected_gp,
        "starting_compound": alt_starting_compound,
        "first_stint": alt_first_stint
        }

    strategy = None
    alt_strategy = None
    
    try: 
        simulation_response = requests.post(API_URL + simulate_race, json = simulation_data)
        simulation_response.raise_for_status()
        strategy = simulation_response.json()

    except requests.exceptions.RequestException as e:
        print(f"Failed calculating race strategy: {e}")

    try:
        alt_simulation_response = requests.post(API_URL + simulate_race, json = alt_simulation_data)
        alt_simulation_response.raise_for_status()
        alt_strategy = alt_simulation_response.json()

    except requests.exceptions.RequestException as e:
            print(f"Failed calculating alternative race strategy: {e}")

    if strategy is None or alt_strategy is None:
        raise RuntimeError(
            "Race strategy calculation failed. "
            "Check that the API is running and both requests succeed."
        )

    return strategy, alt_strategy

  
def no_rain_strategy(driver, selected_gp, asphalt_temperature, grid_position):

    strat, alt_strat = simulate_strategy(driver, selected_gp, asphalt_temperature, grid_position)
    recom_strat, alternative_strat = top_two_strategies(strat, alt_strat)

    if len(recom_strat) == 6:
        pit_window = f"{recom_strat['first_stint']-2}-{recom_strat['first_stint']+2}"
        main_strategy = (f"{recom_strat['starting_compound']} --> {recom_strat['second_compound']}<br>"
                    f"Pit window: {pit_window}")

    if len(alternative_strat) == 6:
        pit_window = f"{alternative_strat['pit_lap']-2}-{alternative_strat['pit_lap']+2}"
        alt_strategy = (f"{alternative_strat['starting_compound']} --> {alternative_strat['second_compound']}<br>"
                    f"Pit window: {pit_window}")

    if len(recom_strat) == 9:
        first_pit_window = f"{recom_strat['pit1_lap']-2}-{recom_strat['pit1_lap']+2}"
        second_pit_window = f"{recom_strat['pit2_lap']-2}-{recom_strat['pit2_lap']+2}"
        main_strategy = (f"{recom_strat['starting_compound']} --> {recom_strat['second_compound']} --> {recom_strat['third_compound']}<br>"
                        f"1st Pit Window: {first_pit_window}<br>"
                        f"2nd Pit Window: {second_pit_window}")

    if len(alternative_strat) == 9:
        first_pit_window = f"{alternative_strat['pit1_lap']-2}-{alternative_strat['pit1_lap']+2}"
        second_pit_window = f"{alternative_strat['pit2_lap']-2}-{alternative_strat['pit2_lap']+2}"
        alt_strategy = (f"{alternative_strat['starting_compound']} --> {alternative_strat['second_compound']} --> {alternative_strat['third_compound']}<br>"
                         f"1st Pit Window: {first_pit_window}<br>"
                         f"2nd Pit Window: {second_pit_window}")
    
    return main_strategy, alt_strategy


def calculate_strategy(driver, selected_gp, weather, asphalt_temperature, air_temperature, grid_position, safety_car_probability):

    # Wet conditions
    if weather == "Heavy rain":

        strategy = "WET"
        alt_strategy = "-"
        explanation = (
            "Prioritize wet-weather tyre management. "
            "Avoid aggressive early stints and monitor the crossover point."
        )
    
    elif weather == "Light rain":

        strategy = "INTERMEDIATE"
        alt_strategy = "-"
        explanation = (
            "Track conditions may evolve rapidly. "
            "Monitor rainfall intensity and be ready for switching to slicks."
        )
    
    
    elif weather == "No rain":
        strategy, alt_strategy = no_rain_strategy(driver, selected_gp, asphalt_temperature, grid_position)
        explanation = (
                    "..."
                )
    else:
        raise ValueError(f"Unknown Weather condition: {weather}")

    # Safety car adjustment
    if safety_car_probability == "High":

        explanation += (
            "<br>High Safety Car probability increases the value of "
            "keeping strategic flexibility for a cheap pit stop."
        )
    
    if safety_car_probability == "Medium":
    
        explanation += (
            "<br>Safety Car probability is slightly increased"  
        )

    if air_temperature > 30:
        explanation += (
            "<br>The heat can be physically demanding for drivers."
            "Ensure proper hydration and cooling."
        )

    return strategy, alt_strategy, explanation


# ============================================================
# CALCULATE BUTTON
# ============================================================

st.markdown("")

if st.button("🏎️  GENERATE STRATEGY"):

    strategy, alt_strategy, explanation = calculate_strategy(
        driver = driver,
        selected_gp = selected_gp,
        weather=weather,
        asphalt_temperature=asphalt_temperature,
        air_temperature=air_temperature,
        grid_position=grid_position,
        safety_car_probability=safety_car_probability
    )

    strategy_html=f"""
    <div class="strategy-result">
        <div class="strategy-label">
            Recommended Strategy
        </div>
        <div class="strategy-main">
            {strategy}
        </div>
        <div class="strategy-label">
            Alternative Strategy
        </div>
        <div class="strategy-main">
            {alt_strategy}
        </div>
        <div style="
            color:#c0c0c0;
            line-height:1.6;
            font-size:15px;
            ">
            {explanation}
        </div>
    </div>
    """
    st.markdown(strategy_html, unsafe_allow_html=True)

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

