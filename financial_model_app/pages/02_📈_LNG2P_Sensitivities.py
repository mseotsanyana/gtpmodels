import streamlit as st

from financial_model_app.src.components.sensitivity_analysis import (
    show_sensitivity_analysis_chart,
)
from financial_model_app.src.components.sidebars import (
    show_sensitivity_analysis_sidebar,
)

for k, v in st.session_state.items():
    st.session_state[k] = v

scenario_options = ["Peaking", "Mid-merit", "Baseload"]

# parameter section
parameter_options = [
    "Select All",
    "Discount rate",
    "Load factor",
    "Lifetime",
    "Fuel costs",
    "Carbon costs",
    "Efficiency rate",
    "Exchange rate",
]

# Initialize selected scenarios for sensitivity analysis.
if "selected_scenarios" not in st.session_state:
    st.session_state["selected_scenarios"] = []


# show the sensitivity analysis sidebar
show_sensitivity_analysis_sidebar(scenario_options, parameter_options)

# st.write(st.session_state)

# show the sensitivity analysis plotly charts
show_sensitivity_analysis_chart(parameter_options)
