import os

import streamlit as st

from financial_model_app.src.utils.constants import (
    parameter_labels,
    parameter_step_values,
)


def show_dashboard_sidebar(scenario_data, plant_data):

    with st.sidebar.expander(":blue[LNG-to-Power scenario formulation]"):
        # st.image(os.getcwd() + "/financial_model_app/asserts/developer.png")
        st.logo(
            image=os.getcwd() + "/financial_model_app/asserts/developer.png",
            size="large",
        )
        # select scenario variables - the selection drives the electricity generated, the LNG volumes
        # required, CO2e emissions, discounted costs, localized cost of electricity, and sensitivity
        # analysis for all parameters except load factor for peaking, mid-merit and baseload scenarios.

        default_values_scenarios_col, reset_scenarios_col = st.columns([2, 1])
        default_values_scenarios_col.write("Reset to scenarios")

        reset_scenarios_clicked = reset_scenarios_col.button(
            "Reset ",
            # key=f"reset_plant_scenarios_key_{st.session_state.refresh_scenarios_key}",
        )

        if reset_scenarios_clicked:
            st.session_state.scenarios = scenario_data.copy()
            st.session_state.scenarios_buffer = scenario_data.copy()
            # Change widget keys to force refresh of number_input
            st.session_state.refresh_scenarios_key = str(
                int(st.session_state.refresh_scenarios_key) + 1
            )
            st.rerun()

        def on_change_scenario(
            key,
        ):
            if key == "peaking_scenario_key":
                st.session_state.scenarios["Peaking"] = (
                    st.session_state.peaking_scenario_key
                )
            if key == "midmerit_scenario_key":
                st.session_state.scenarios["Mid-merit"] = (
                    st.session_state.midmerit_scenario_key
                )

            if key == "baseload_scenario_key":
                st.session_state.scenarios["Baseload"] = (
                    st.session_state.baseload_scenario_key
                )

        peaking = st.slider(
            label="Peaking load factor: ",
            min_value=1.0,
            max_value=20.0,
            value=st.session_state.scenarios["Peaking"],
            on_change=on_change_scenario,
            args=("peaking_scenario_key",),
            key="peaking_scenario_key",
            format="%d%%",
        )

        st.divider()

        midmerit = st.slider(
            label="Mid-merit load factor: ",
            min_value=21.0,
            max_value=60.0,
            value=st.session_state.scenarios["Mid-merit"],
            on_change=on_change_scenario,
            args=("midmerit_scenario_key",),
            key="midmerit_scenario_key",
            format="%d%%",
        )

        st.divider()

        baseload = st.slider(
            label="Baseload load factor: ",
            min_value=61.0,
            max_value=100.0,
            value=st.session_state.scenarios["Baseload"],
            on_change=on_change_scenario,
            args=("baseload_scenario_key",),
            key="baseload_scenario_key",
            format="%d%%",
        )

        st.session_state.scenarios["Peaking"] = peaking
        st.session_state.scenarios["Mid-merit"] = midmerit
        st.session_state.scenarios["Baseload"] = baseload

    with st.sidebar.expander(":blue[Edit power plant specific parameters]"):
        # set specific power plant technical and financial parameters

        default_values_col, reset_col = st.columns([2, 1])
        default_values_col.write("Reset parameters")

        reset_clicked = reset_col.button(
            "Reset",
            # key=f"reset_plant_parameters_key_{st.session_state.refresh_plants_key}",
        )

        selected_plant = st.selectbox(
            " ",
            (st.session_state.plants.keys()),
            index=None,
            placeholder="Select a power plant to edit...",
            key=f"select_box_key_{st.session_state.refresh_plants_key}",
        )

        if reset_clicked:
            st.session_state.plants = plant_data.copy()
            st.session_state.plants_buffer = plant_data.copy()
            # Change widget keys to force refresh of number_input
            st.session_state.refresh_plants_key = str(
                int(st.session_state.refresh_plants_key) + 1
            )
            st.rerun()

        def update_callback(
            key,
        ):
            for plant_cb, characteristics_cb in st.session_state.plants.items():
                if selected_plant == plant_cb:
                    for parameter_cb in characteristics_cb:
                        if (
                            key
                            == f"{plant_cb}_{parameter_cb}_{st.session_state.refresh_plants_key}"
                        ):
                            st.session_state.plants[plant_cb][parameter_cb] = (
                                st.session_state[key]
                            )

        for plant, characteristics in st.session_state.plants.items():

            if selected_plant == plant:
                for parameter in characteristics:
                    value_type = type(characteristics[parameter])
                    st.session_state.plants[selected_plant][parameter] = (
                        st.number_input(
                            f"{parameter_labels()[parameter]}:",
                            value=st.session_state.plants[selected_plant][parameter],
                            min_value=0 if value_type == int else 0.0,
                            # max_value=1.0 if (parameter in percentage_parameters and value_type == float) else 1.0,
                            step=parameter_step_values()[parameter],
                            on_change=update_callback,
                            args=(
                                f"{plant}_{parameter}_{st.session_state.refresh_plants_key}",
                            ),
                            key=f"{plant}_{parameter}_{st.session_state.refresh_plants_key}",
                        )
                    )


def show_sensitivity_analysis_sidebar(scenario_options, parameter_options):
    st.sidebar.write("Select scenarios:")

    selected_scenarios = {}
    for scenario in scenario_options:
        if st.sidebar.checkbox(label=scenario, key=f"key_{scenario}"):
            selected_scenarios[scenario] = st.session_state["scenarios"][scenario]

    st.session_state.selected_scenarios = selected_scenarios

    st.sidebar.divider()

    if "max_selections" not in st.session_state:
        st.session_state["max_selections"] = len(parameter_options)

    def on_update_selected_options():
        if "selected_parameters" in st.session_state:
            if "Select All" in st.session_state["selected_parameters"]:
                st.session_state["selected_parameters"] = [parameter_options[0]]
                st.session_state["max_selections"] = 1
            else:
                st.session_state["max_selections"] = len(parameter_options)

    st.sidebar.multiselect(
        label="Select parameters:",
        options=parameter_options,
        key="selected_parameters",
        max_selections=st.session_state["max_selections"],
        on_change=on_update_selected_options,
        format_func=lambda x: "All Parameters" if x == "Select All" else f"{x}",
    )
