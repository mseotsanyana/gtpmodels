import os

import pandas as pd
import streamlit as st
from src.components.dashboard import show_dashboard_charts
from src.components.sidebars import show_dashboard_sidebar
from src.utils.load_data import (
    load_emission_factors_data,
    load_plant_data,
    load_scenario_data,
    load_sensitivity_data,
)

path = os.getcwd()
plant_data = pd.read_csv(path + "/financial_model_app/data/plant_parameters.csv")
scenario_data = pd.read_csv(path + "/financial_model_app/data/scenarios.csv")
emission_data = pd.read_csv(path + "/financial_model_app/data/emission_factors.csv")
sensitivity_data = pd.read_csv(
    path + "/financial_model_app/data/sensitivity_parameters.csv"
)

for k, v in st.session_state.items():
    st.session_state[k] = v


# Streamlit app
def main():
    st.set_page_config(
        page_title="LNG2P App",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # st.write(plant_data)
    # st.write(scenario_data)
    # st.write(emission_data)
    # st.write(sensitivity_data)

    # The main function of the app
    # st.write("## Gas To Power Financial Model")

    # Initialize plant data from csv file into session state.
    if "plants" not in st.session_state:
        st.session_state.plants = load_plant_data(plant_data).copy()

    # Initialize scenario data from csv file into session state.
    if "scenarios" not in st.session_state:
        st.session_state.scenarios = load_scenario_data(scenario_data).copy()

    # Initialize emission factors data from csv file into session state.
    if "emission_factors" not in st.session_state:
        st.session_state.emission_factors = load_emission_factors_data(
            emission_data
        ).copy()

    # Initialize sensitivity data from csv file into session state.
    if "sensitivities" not in st.session_state:
        st.session_state.sensitivities = load_sensitivity_data(sensitivity_data).copy()

    # # Initialize selected scenarios for sensitivity analysis.
    # if "selected_scenarios" not in st.session_state:
    #     st.session_state["selected_scenarios"] = []

    # Initialize selected parameters for sensitivity analysis.
    if "selected_parameters" not in st.session_state:
        st.session_state.selected_parameters = ["Select All"]
        st.session_state["max_selections"] = 1

    # Ensure refresh_plants_key exists in session state.
    if "refresh_plants_key" not in st.session_state:
        st.session_state.refresh_plants_key = "0"

    # Ensure refresh_scenarios_key exists in session state.
    if "refresh_scenarios_key" not in st.session_state:
        st.session_state.refresh_scenarios_key = "0"

    # Ensure refresh_scenarios_key exists in session state.
    if "key_Peaking" not in st.session_state:
        st.session_state.key_Peaking = True

    # st.write(st.session_state)

    # show the dashboard sidebar
    show_dashboard_sidebar(
        load_scenario_data(scenario_data), load_plant_data(plant_data)
    )

    # show the dashboard ployly charts
    show_dashboard_charts()


if __name__ == "__main__":
    main()
