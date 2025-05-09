import streamlit as st

from financial_model_app.src.components.plotly_charts import (
    create_bar_chart,
    create_donut_pie_chart,
    create_group_bar_and_dot_chart,
    create_horizontal_group_stack_bar_chart,
)
from financial_model_app.src.models.results_visualization import (
    compute_demand_scenario_emissions,
    compute_demand_scenario_projections,
    compute_discount_cash_flows,
    compute_scenario_lcoe,
)


# dashboard graphs
def show_dashboard_charts():
    with st.container(height=470):
        demand, emissions = st.columns(2)
        with demand:
            demand_scenarios = compute_demand_scenario_projections(
                st.session_state.plants, st.session_state.scenarios
            )
            create_group_bar_and_dot_chart(demand_scenarios)

        with emissions:
            electricity_emission = compute_demand_scenario_emissions(
                demand_scenarios, st.session_state.emission_factors
            )
            create_horizontal_group_stack_bar_chart(electricity_emission)

    with st.container(height=500):
        costs, lcoe = st.columns(2)
        with costs:
            peaking_tab, midmerit_tab, baseload_tab = st.tabs(
                ["Peaking scenario", "Mid-merit scenario", "Baseload scenario"]
            )
            with peaking_tab:
                discounted_plant_costs = compute_discount_cash_flows(
                    st.session_state.plants, st.session_state.scenarios, "Peaking"
                )
                create_donut_pie_chart(
                    discounted_plant_costs,
                    "Lifetime total discounted costs for peaking scenario.",
                )
            with midmerit_tab:
                discounted_plant_costs = compute_discount_cash_flows(
                    st.session_state.plants, st.session_state.scenarios, "Mid-merit"
                )
                create_donut_pie_chart(
                    discounted_plant_costs,
                    "Lifetime total discounted costs for mid-merit scenario.",
                )
            with baseload_tab:
                discounted_plant_costs = compute_discount_cash_flows(
                    st.session_state.plants, st.session_state.scenarios, "Baseload"
                )
                create_donut_pie_chart(
                    discounted_plant_costs,
                    "Lifetime total discounted costs for baseload scenario.",
                )
        with lcoe:
            plant_scenario_lcoe = compute_scenario_lcoe(
                st.session_state.plants, st.session_state.scenarios
            )
            create_bar_chart(discounted_plant_costs, plant_scenario_lcoe)
