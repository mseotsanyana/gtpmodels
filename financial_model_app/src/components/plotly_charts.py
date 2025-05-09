import math

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from financial_model_app.src.utils.constants import BILLION


## creating plots to visualize results
def create_group_bar_and_dot_chart(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    plants = df["Power Plant"].unique().tolist()
    index = 1
    for plant in plants:
        pj_df = df[df["Power Plant"] == plant].groupby("Scenario")["PJ"].sum()
        mtpa_df = df[df["Power Plant"] == plant].groupby("Scenario")["MTPA"].sum()

        fig.add_trace(
            go.Bar(
                name=plant,
                x=pj_df.index,
                y=pj_df,
                offsetgroup=index,
                hovertemplate="%{y:.2f} PJ",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                name=plant,
                x=mtpa_df.index,
                y=mtpa_df,
                mode="markers",
                marker=dict(
                    size=12, symbol="diamond", line=dict(width=2, color="DarkSlateGrey")
                ),
                offsetgroup=index,
                hovertemplate="%{y:.2f} MTPA",
            ),
            secondary_y=True,
        )

        index = index + 1

    fig.update_layout(
        title=dict(
            text="Electricity generation and LNG volumes by scenario and power plant.",
            y=1.0,  # -0.98
            x=0,
            xanchor="left",
            yanchor="top",
            font=dict(family="Helvetica Neue", size=18),
        ),
        barmode="group",
        scattermode="group",
        legend=dict(orientation="h"),
        margin=dict(t=50, b=30, l=10, r=10),
        height=430,
    )
    # fig.update_layout()

    fig.update_yaxes(
        title_text="LNG Feedstock (MTPA)", rangemode="tozero", secondary_y=True
    )
    fig.update_yaxes(
        title_text="Generated Electricity (PJ/Year)",
        rangemode="tozero",
        secondary_y=False,
    )
    st.plotly_chart(fig)


def create_horizontal_group_stack_bar_chart(df):
    fig = go.Figure()
    fuels = df["Fuel Type"].unique()
    colors = ["darkred", "indianred", "rosybrown"]
    for fuel, colour in zip(fuels, colors):
        fuel_df = df[df["Fuel Type"] == fuel]
        fig.add_trace(
            go.Bar(
                x=fuel_df["MtCO2e"],
                y=[fuel_df["Scenario"], fuel_df["Power Plant"]],
                orientation="h",
                name=fuel,
                marker=dict(
                    color=colour,
                ),
                hovertemplate="%{x:.2f} MtCO2e",
            )
        )

    fig.update_layout(
        title=dict(
            text="Greenhouse gas emissions in MtCO2e by scenario and power plant.",
            y=1.0,  # -0.98
            x=0,
            xanchor="left",
            yanchor="top",
            font=dict(family="Helvetica Neue", size=18),
        ),
        # template="simple_white",
        barmode="stack",
        hovermode="y unified",
        legend=dict(yanchor="top", y=0.4, xanchor="left", x=0.75),
        margin=dict(t=50, b=30, l=10, r=10),
        height=430,
        # legend=dict(orientation='h')
    )

    st.plotly_chart(fig)


def create_donut_pie_chart(discounted_plant_costs, title):
    num_plants = 3  # len(discounted_plant_costs)

    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(
        rows=2,
        cols=num_plants,
        subplot_titles=tuple([t for t in discounted_plant_costs.keys()]),
        specs=[
            [{"type": "pie"} for i in range(0, num_plants)],
            [{"type": "pie"} for i in range(0, num_plants)],
        ],
        vertical_spacing=0.11,
    )
    col_index = 0
    row_index = 1
    plant_total_cost = []
    for plant, costs in discounted_plant_costs.items():
        total = sum(discounted_plant_costs[plant].values())
        labels = list(discounted_plant_costs[plant].keys())
        values = [v / total * 100 for v in discounted_plant_costs[plant].values()]
        plant_total_cost.append(round(total / BILLION, 2))
        col_index = col_index + 1
        if col_index > 3:
            row_index = 2
            col_index = 1

        fig.add_trace(
            go.Pie(
                labels=labels,
                values=values,
                name=plant,
                hole=0.6,
                hoverinfo="label+percent+name",
            ),
            row_index,
            col_index,
        )

    annotations = [a.to_plotly_json() for a in fig["layout"]["annotations"]]
    annotations.extend(
        [
            dict(
                text="R" + str(plant_total_cost[0]) + "B",
                x=sum(fig.get_subplot(1, 1).x) / 2,
                y=0.82,
                font_size=16,
                showarrow=False,
                xanchor="center",
            ),
            dict(
                text="R" + str(plant_total_cost[1]) + "B",
                x=sum(fig.get_subplot(1, 2).x) / 2,
                y=0.82,
                font_size=16,
                showarrow=False,
                xanchor="center",
            ),
            dict(
                text="R" + str(plant_total_cost[2]) + "B",
                x=sum(fig.get_subplot(1, 3).x) / 2,
                y=0.82,
                font_size=16,
                showarrow=False,
                xanchor="center",
            ),
            dict(
                text="R" + str(plant_total_cost[3]) + "B",
                x=sum(fig.get_subplot(2, 1).x) / 2,
                y=0.2,
                font_size=16,
                showarrow=False,
                xanchor="center",
            ),
            dict(
                text="R" + str(plant_total_cost[4]) + "B",
                x=sum(fig.get_subplot(2, 2).x) / 2,
                y=0.2,
                font_size=16,
                showarrow=False,
                xanchor="center",
            ),
        ]
    )

    fig["layout"]["annotations"] = annotations

    fig.update_layout(
        title=dict(
            text=title,
            y=1.0,  # -0.98
            x=0.0,
            xanchor="left",
            yanchor="top",
            # font=dict(family="Helvetica Neue", size=18),
        ),
        legend=dict(yanchor="top", y=0.45, xanchor="left", x=0.80),
        margin=dict(t=50, b=30, l=10, r=10),
        height=410,
    )  # paper_bgcolor='rgb(233,233,233)', set the background colour
    # fig.print_grid()
    st.plotly_chart(fig)


def create_bar_chart(discounted_plant_costs, plant_scenario_lcoe):
    num_plants = math.ceil(len(plant_scenario_lcoe["Power Plant"].unique()) / 2)

    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(
        rows=2,
        cols=num_plants,
        # subplot_titles=tuple([t for t in discounted_plant_costs.keys()]),
        specs=[
            [{"type": "bar"} for i in range(0, num_plants)],
            [{"type": "bar"} for i in range(0, num_plants)],
        ],
        horizontal_spacing=0.13,
    )

    row_index = 1
    col_index = 0
    for plant, costs in discounted_plant_costs.items():
        col_index = col_index + 1
        if col_index > 3:
            row_index = 2
            col_index = 1
        scenario_df = plant_scenario_lcoe[plant_scenario_lcoe["Power Plant"] == plant]
        fig.add_trace(
            go.Bar(
                x=scenario_df["Scenario"],
                y=scenario_df["LCOE"],
                hovertemplate="R%{y:.2f}/kWh",
                name=plant,
            ),
            row_index,
            col_index,
        )
    fig.update_layout(
        title=dict(
            text="Localized cost of electricity (LCOE) by scenario.",
            y=1.0,  # -0.98
            x=0,
            xanchor="left",
            yanchor="top",
            # font=dict(family="Helvetica Neue", size=18),
        ),
        # showlegend=False,
        legend=dict(yanchor="top", y=0.3, xanchor="left", x=0.75),
        margin=dict(t=40, b=10, l=10, r=10),
        # legend=dict(orientation='h'),
        height=430,
    )  # paper_bgcolor='rgb(233,233,233)', set the background colour
    fig.update_yaxes(title_text="LCOE (R/kWh)")
    # st.write(fig.layout)
    st.plotly_chart(fig)


# sensitivity section
def create_sensitivity_subplots_chart(marked_parameters, sensitivities):
    marked_scenarios = sensitivities["Scenario"].unique().tolist()
    marked_plants = sensitivities["Power Plant"].unique().tolist()
    num_scenarios = len(marked_scenarios)
    num_parameters = len(marked_parameters)
    num_plants = len(marked_plants)

    if (num_scenarios * num_parameters) > 0:
        # create a list of selected subplots titles
        subtitles = []
        for marked_scenario in marked_scenarios:
            for marked_parameter in marked_parameters:
                if (
                    "All Scenarios" == marked_scenario
                    and "Load factor" == marked_parameter
                ):
                    subtitles.append("Range of load factors")
                elif (
                    "All Scenarios" != marked_scenario
                    and "Load factor" != marked_parameter
                ):
                    subtitles.append(
                        str(marked_parameter) + " - " + str(marked_scenario)
                    )

        # st.write(subtitles)

        # number of subplots to be generated.
        num_subplots = len(subtitles)

        # adjust the vertical spacing and subplot height
        # depending on the number of subplots selected.
        current_vertical_spacing = 0.10
        current_subplot_height = 500
        if num_subplots <= 3:
            current_vertical_spacing = 0.10
            current_subplot_height = 500
        elif 3 < num_subplots <= 6:
            current_vertical_spacing = 0.10
            current_subplot_height = 800
        elif 6 < num_subplots <= 9:
            current_vertical_spacing = 0.08
            current_subplot_height = 1100
        elif 9 < num_subplots <= 12:
            current_vertical_spacing = 0.06
            current_subplot_height = 1400
        elif 12 < num_subplots <= 15:
            current_vertical_spacing = 0.04
            current_subplot_height = 1700
        elif 15 < num_subplots <= 18:
            current_vertical_spacing = 0.04
            current_subplot_height = 2000
        elif num_subplots > 18:
            current_vertical_spacing = 0.04
            current_subplot_height = 2300

        # print(subtitles)
        # st.write((num_scenarios, num_parameters, num_subplots, ceil(num_subplots / 3)))
        fig = make_subplots(
            rows=1 if num_subplots <= 3 else math.ceil(num_subplots / 3),
            cols=num_subplots if num_subplots < 3 else 3,
            subplot_titles=subtitles,
            shared_yaxes=False,
            specs=[
                [
                    {"type": "scatter"}
                    for num_cols in range(0, (num_subplots if num_subplots < 3 else 3))
                ]
                for num_rows in range(0, math.ceil(num_subplots / 3))
            ],
            vertical_spacing=current_vertical_spacing,
            # 1 / (ceil(num_subplots / 3) - 1) if (ceil(num_subplots / 3) - 1) > 0 else 0.020
        )

        isLegend = True
        isLoadFactorProcessed = False

        colors = px.colors.qualitative.Plotly[:num_plants]

        # print(colors)
        # fig.print_grid()

        col_index = 0
        row_index = 1  # 1 if num_subplots <= 3 else ceil(num_subplots / 3)

        for marked_scenario in marked_scenarios:
            for marked_parameter in marked_parameters:
                if (
                    "All Scenarios" == marked_scenario
                    and "Load factor" == marked_parameter
                ):
                    col_index = col_index + 1
                    if col_index > 3:
                        row_index = row_index + 1
                        col_index = 1
                    # print(f"ROW = {row_index} COL = {col_index}")

                    for plant, color in zip(marked_plants, colors):
                        param_df = sensitivities[
                            sensitivities.Parameter == marked_parameter
                        ]
                        scenario_df = param_df[param_df.Scenario == marked_scenario]
                        plant_df = scenario_df[
                            scenario_df["Power Plant"] == plant
                        ].reindex()
                        fig.add_trace(
                            go.Scatter(
                                x=plant_df["Value"],
                                y=plant_df["LCOE"],
                                mode="lines+markers",
                                line_color=color,
                                hovertemplate="R%{y:.2f}/kWh",
                                name=plant,
                                showlegend=isLegend,
                            ),
                            row_index,
                            col_index,
                        )
                    isLegend = False

                elif (
                    "All Scenarios" != marked_scenario
                    and "Load factor" != marked_parameter
                ):
                    col_index = col_index + 1
                    if col_index > 3:
                        row_index = row_index + 1
                        col_index = 1
                    # print(f"ROW = {row_index} COL = {col_index}")

                    for plant, color in zip(marked_plants, colors):
                        param_df = sensitivities[
                            sensitivities.Parameter == marked_parameter
                        ]
                        scenario_df = param_df[param_df.Scenario == marked_scenario]
                        plant_df = scenario_df[
                            scenario_df["Power Plant"] == plant
                        ].reindex()
                        fig.add_trace(
                            go.Scatter(
                                x=plant_df["Value"],
                                y=plant_df["LCOE"],
                                mode="lines+markers",
                                line_color=color,
                                hovertemplate="R%{y:.2f}/kWh",
                                name=plant,
                                showlegend=isLegend,
                            ),
                            row_index,
                            col_index,
                        )
                    isLegend = False

        fig.update_layout(
            title=dict(
                text="Sensitivity analysis of localized cost of electricity (LCOE) "
                "with respect to its parameters (drivers) by scenario.",
                y=1.0,  # -0.98
                x=0,
                xanchor="left",
                yanchor="top",
                # font=dict(family="Helvetica Neue", size=18),
            ),
            hovermode="x unified",
            # margin=dict(t=0, b=0, l=0, r=0),
            height=current_subplot_height,
            width=500,
        )
        fig.update_yaxes(title_text="LCOE (R/kWh)")
        st.plotly_chart(fig)
