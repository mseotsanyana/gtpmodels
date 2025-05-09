import pandas as pd
import streamlit as st

from financial_model_app.src.components.plotly_charts import (
    create_sensitivity_subplots_chart,
)
from financial_model_app.src.models.results_visualization import (
    compute_lcoe_sensitivities,
)

# st.write(st.session_state)


def show_sensitivity_analysis_chart(parameter_options):
    sensitivity_df = compute_lcoe_sensitivities(
        st.session_state.plants,
        st.session_state.selected_scenarios,
        st.session_state.sensitivities,
    )

    selected_params = (
        parameter_options[1:]
        if st.session_state["max_selections"] == 1
        else st.session_state["selected_parameters"]
    )

    params = []
    selected_sensitivities = pd.DataFrame(
        {"Power Plant": [], "Scenario": [], "Parameter": [], "Value": [], "LCOE": []}
    )
    for param in selected_params:
        params.append(sensitivity_df[sensitivity_df.Parameter == param])
    if len(params) != 0:
        selected_sensitivities = pd.concat(params).reindex()

    # st.write(st.session_state)
    # st.write(selected_params)
    # st.write(selected_sensitivities)
    create_sensitivity_subplots_chart(selected_params, selected_sensitivities)
