## GRAPH ONE ##


import pandas as pd

from src.models.lcoe_model import (
    calculate_lcoe,
    create_cash_flow,
    create_cost_items,
    discount_cash_flows,
    end_of_operation_period,
    roll_cost_items,
    start_of_operation_period,
)
from src.models.lng_demand_model import (
    electricity_demand_pj,
    electricity_output_mwh,
    feedstock_demand_mtpa,
)
from src.utils.constants import PRESENT_YEAR


def compute_demand_scenario_projections(plants, scenarios):
    """
    Demand scenario projections.
    """

    plant_list = []
    scenario_list = []
    pj_demands = []
    mtpa_demands = []
    for plant, characteristics in plants.items():
        for scenario, capacity_factor in scenarios.items():
            cf = capacity_factor / 100.0
            pj = electricity_demand_pj(characteristics["installed_capacity_mw"], cf)
            mtpa = feedstock_demand_mtpa(
                characteristics["installed_capacity_mw"],
                cf,
                characteristics["efficiency_rate"],
            )

            plant_list.append(plant)
            scenario_list.append(scenario)
            pj_demands.append(pj)
            mtpa_demands.append(mtpa)

    demand_df = pd.DataFrame(
        {
            "Power Plant": plant_list,
            "Scenario": scenario_list,
            "PJ": pj_demands,
            "MTPA": mtpa_demands,
        }
    )

    return demand_df


## GRAPH TWO ##


def compute_demand_scenario_emissions(demands, emission_factor_mtco2e_per_pjs):
    """
    Demand scenario emissions.
    """
    scenario_list = []
    plant_list = []
    fuel_type_list = []
    mtco2e_list = []

    for pj_index, pj_row in demands.iterrows():
        for energy_carrier, mtco2e_per_pj in emission_factor_mtco2e_per_pjs.items():
            scenario_list.append(pj_row["Scenario"])
            plant_list.append(pj_row["Power Plant"])
            fuel_type_list.append(energy_carrier)

            mtco2e = float(mtco2e_per_pj) * float(pj_row["PJ"])

            mtco2e_list.append(mtco2e)

    mtco2e_df = pd.DataFrame(
        {
            "Scenario": scenario_list,
            "Power Plant": plant_list,
            "Fuel Type": fuel_type_list,
            "MtCO2e": mtco2e_list,
        }
    )

    return mtco2e_df


## GRAPH THREE ##


def compute_discount_cash_flows(plants, scenarios, scenario_name):
    """
    Compute discounted cash flows.
    """
    plant_discounted_cash_flow = {}
    for plant, characteristics in plants.items():
        installed_capacity_mw = float(plants[plant]["installed_capacity_mw"])
        construction_duration_years = int(plants[plant]["construction_duration_years"])
        overnight_capex_per_kw = float(plants[plant]["overnight_capex_per_kw"])
        operational_lifetime_years = int(plants[plant]["operational_lifetime_years"])
        foam_cost_factor = float(plants[plant]["foam_cost_factor"])
        voam_cost_per_mwh = float(plants[plant]["voam_cost_per_mwh"])
        fuel_cost_per_tLNG = float(plants[plant]["fuel_cost_per_tLNG"])
        carbon_cost_per_tCO2e = float(plants[plant]["carbon_cost_per_tCO2e"])
        decommissioning_duration_years = int(
            plants[plant]["decommissioning_duration_years"]
        )
        capex_contingency_factor = float(plants[plant]["capex_contingency_factor"])
        decommissioning_cost_factor = float(
            plants[plant]["decommissioning_cost_factor"]
        )
        efficiency_rate = float(plants[plant]["efficiency_rate"])
        emission_factor_mtco2e_per_pj = float(
            plants[plant]["emission_factor_mtco2e_per_pj"]
        )
        discount_rate = float(plants[plant]["discount_rate"])
        exchange_rate = float(plants[plant]["exchange_rate"])

        plant_cost_items = roll_cost_items(
            installed_capacity_mw,
            construction_duration_years,
            operational_lifetime_years,
            decommissioning_duration_years,
            overnight_capex_per_kw,
            capex_contingency_factor,
            foam_cost_factor,
            voam_cost_per_mwh,
            fuel_cost_per_tLNG,
            carbon_cost_per_tCO2e,
            decommissioning_cost_factor,
            scenarios[scenario_name],
            emission_factor_mtco2e_per_pj,
            efficiency_rate,
            exchange_rate,
        )

        cost_items = create_cost_items(plant_cost_items)

        plant_discounted_cash_flow[plant] = discount_cash_flows(
            cost_items, discount_rate, PRESENT_YEAR
        )

    return plant_discounted_cash_flow


## GRAPH FOUR ##


def compute_scenario_lcoe(plants, scenarios):
    """
    Compute scenario localized cost of electricity.
    """

    scenario_list = []
    plant_list = []
    lcoe_list = []

    for plant, characteristics in plants.items():
        installed_capacity_mw = float(plants[plant]["installed_capacity_mw"])
        construction_duration_years = int(plants[plant]["construction_duration_years"])
        overnight_capex_per_kw = float(plants[plant]["overnight_capex_per_kw"])
        operational_lifetime_years = int(plants[plant]["operational_lifetime_years"])
        foam_cost_factor = float(plants[plant]["foam_cost_factor"])
        voam_cost_per_mwh = float(plants[plant]["voam_cost_per_mwh"])
        fuel_cost_per_tlng = float(plants[plant]["fuel_cost_per_tLNG"])
        carbon_cost_per_tco2e = float(plants[plant]["carbon_cost_per_tCO2e"])
        decommissioning_duration_years = int(
            plants[plant]["decommissioning_duration_years"]
        )
        capex_contingency_factor = float(plants[plant]["capex_contingency_factor"])
        decommissioning_cost_factor = float(
            plants[plant]["decommissioning_cost_factor"]
        )
        efficiency_rate = float(plants[plant]["efficiency_rate"])
        emission_factor_mtco2e_per_pj = float(
            plants[plant]["emission_factor_mtco2e_per_pj"]
        )
        discount_rate = float(plants[plant]["discount_rate"])
        exchange_rate = float(plants[plant]["exchange_rate"])

        for scenario, cf in scenarios.items():
            plant_revenue_item = (
                start_of_operation_period(construction_duration_years),
                end_of_operation_period(
                    construction_duration_years, operational_lifetime_years
                ),
                electricity_output_mwh(installed_capacity_mw, cf),
            )

            plant_cost_items = roll_cost_items(
                installed_capacity_mw,
                construction_duration_years,
                operational_lifetime_years,
                decommissioning_duration_years,
                overnight_capex_per_kw,
                capex_contingency_factor,
                foam_cost_factor,
                voam_cost_per_mwh,
                fuel_cost_per_tlng,
                carbon_cost_per_tco2e,
                decommissioning_cost_factor,
                cf,
                emission_factor_mtco2e_per_pj,
                efficiency_rate,
                exchange_rate,
            )

            revenue_item = create_cash_flow(plant_revenue_item)
            cost_items = create_cost_items(plant_cost_items)

            scenario_plant_lcoe = calculate_lcoe(
                revenue_item, cost_items, discount_rate, exchange_rate, PRESENT_YEAR
            )

            scenario_list.append(scenario)
            plant_list.append(plant)
            lcoe_list.append(scenario_plant_lcoe)

    plant_lcoe = pd.DataFrame(
        {
            "Scenario": scenario_list,
            "Power Plant": plant_list,
            "LCOE": lcoe_list,
        }
    )

    return plant_lcoe


## GRAPH FIVE ##


def compute_lcoe_sensitivities(plants, scenarios, selected_parameters):
    # plants = data.plants
    # scenarios = data.selected_scenarios
    # selected_parameters = data.sensitivities

    plant_list = []
    scenario_list = []
    parameter_list = []
    value_list = []
    lcoe_list = []

    for plant, parameters in plants.items():
        installed_capacity_mw = float(plants[plant]["installed_capacity_mw"])
        construction_duration_years = int(plants[plant]["construction_duration_years"])
        overnight_capex_per_kw = float(plants[plant]["overnight_capex_per_kw"])
        operational_lifetime_years = int(plants[plant]["operational_lifetime_years"])
        foam_cost_factor = float(plants[plant]["foam_cost_factor"])
        voam_cost_per_mwh = float(plants[plant]["voam_cost_per_mwh"])
        fuel_cost_per_tlng = float(plants[plant]["fuel_cost_per_tLNG"])
        carbon_cost_per_tco2e = float(plants[plant]["carbon_cost_per_tCO2e"])
        decommissioning_duration_years = int(
            plants[plant]["decommissioning_duration_years"]
        )
        capex_contingency_factor = float(plants[plant]["capex_contingency_factor"])
        decommissioning_cost_factor = float(
            plants[plant]["decommissioning_cost_factor"]
        )
        efficiency_rate = float(plants[plant]["efficiency_rate"])
        emission_factor_mtco2e_per_pj = float(
            plants[plant]["emission_factor_mtco2e_per_pj"]
        )
        discount_rate = float(plants[plant]["discount_rate"])
        exchange_rate = float(plants[plant]["exchange_rate"])

        if "capacity_factor" in selected_parameters:
            for cf in selected_parameters["capacity_factor"]:
                plant_revenue_item = (
                    start_of_operation_period(construction_duration_years),
                    end_of_operation_period(
                        construction_duration_years, operational_lifetime_years
                    ),
                    electricity_output_mwh(installed_capacity_mw, cf),
                )

                plant_cost_items = roll_cost_items(
                    installed_capacity_mw,
                    construction_duration_years,
                    operational_lifetime_years,
                    decommissioning_duration_years,
                    overnight_capex_per_kw,
                    capex_contingency_factor,
                    foam_cost_factor,
                    voam_cost_per_mwh,
                    fuel_cost_per_tlng,
                    carbon_cost_per_tco2e,
                    decommissioning_cost_factor,
                    cf,
                    emission_factor_mtco2e_per_pj,
                    efficiency_rate,
                    exchange_rate,
                )

                revenue_item = create_cash_flow(plant_revenue_item)
                cost_items = create_cost_items(plant_cost_items)
                lcoe_per_kwh = calculate_lcoe(
                    revenue_item, cost_items, discount_rate, exchange_rate, PRESENT_YEAR
                )
                plant_list.append(plant)
                scenario_list.append("All Scenarios")
                parameter_list.append("Load factor")
                value_list.append(cf)
                lcoe_list.append(lcoe_per_kwh)

        for scenario, cf in scenarios.items():
            plant_revenue_item = (
                start_of_operation_period(construction_duration_years),
                end_of_operation_period(
                    construction_duration_years, operational_lifetime_years
                ),
                electricity_output_mwh(installed_capacity_mw, cf),
            )

            plant_cost_items = roll_cost_items(
                installed_capacity_mw,
                construction_duration_years,
                operational_lifetime_years,
                decommissioning_duration_years,
                overnight_capex_per_kw,
                capex_contingency_factor,
                foam_cost_factor,
                voam_cost_per_mwh,
                fuel_cost_per_tlng,
                carbon_cost_per_tco2e,
                decommissioning_cost_factor,
                cf,
                emission_factor_mtco2e_per_pj,
                efficiency_rate,
                exchange_rate,
            )

            revenue_item = create_cash_flow(plant_revenue_item)
            cost_items = create_cost_items(plant_cost_items)

            for parameter, parameter_values in selected_parameters.items():
                if parameter == "discount_rate":
                    for dr in range(len(parameter_values)):
                        lcoe_per_kwh = calculate_lcoe(
                            revenue_item,
                            cost_items,
                            parameter_values[dr],
                            exchange_rate,
                            PRESENT_YEAR,
                        )
                        plant_list.append(plant)
                        scenario_list.append(scenario)
                        parameter_list.append("Discount rate")
                        value_list.append(parameter_values[dr])
                        lcoe_list.append(lcoe_per_kwh)

                if parameter == "efficiency_rate":
                    for er in range(len(parameter_values)):
                        plant_cost_items = roll_cost_items(
                            installed_capacity_mw,
                            construction_duration_years,
                            operational_lifetime_years,
                            decommissioning_duration_years,
                            overnight_capex_per_kw,
                            capex_contingency_factor,
                            foam_cost_factor,
                            voam_cost_per_mwh,
                            fuel_cost_per_tlng,
                            carbon_cost_per_tco2e,
                            decommissioning_cost_factor,
                            cf,
                            emission_factor_mtco2e_per_pj,
                            parameter_values[er],
                            exchange_rate,
                        )

                        cost_items = create_cost_items(plant_cost_items)
                        lcoe_per_kwh = calculate_lcoe(
                            revenue_item,
                            cost_items,
                            discount_rate,
                            exchange_rate,
                            PRESENT_YEAR,
                        )
                        plant_list.append(plant)
                        scenario_list.append(scenario)
                        parameter_list.append("Efficiency rate")
                        value_list.append(parameter_values[er])
                        lcoe_list.append(lcoe_per_kwh)

                if parameter == "fuel_cost":
                    for fc in range(len(parameter_values)):
                        lng_cost = fuel_cost_per_tlng * parameter_values[fc]
                        plant_cost_items = roll_cost_items(
                            installed_capacity_mw,
                            construction_duration_years,
                            operational_lifetime_years,
                            decommissioning_duration_years,
                            overnight_capex_per_kw,
                            capex_contingency_factor,
                            foam_cost_factor,
                            voam_cost_per_mwh,
                            lng_cost,
                            carbon_cost_per_tco2e,
                            decommissioning_cost_factor,
                            cf,
                            emission_factor_mtco2e_per_pj,
                            efficiency_rate,
                            exchange_rate,
                        )

                        cost_items = create_cost_items(plant_cost_items)
                        lcoe_per_kwh = calculate_lcoe(
                            revenue_item,
                            cost_items,
                            discount_rate,
                            exchange_rate,
                            PRESENT_YEAR,
                        )
                        plant_list.append(plant)
                        scenario_list.append(scenario)
                        parameter_list.append("Fuel costs")
                        value_list.append(parameter_values[fc])
                        lcoe_list.append(lcoe_per_kwh)

                if parameter == "carbon_cost":
                    for cc in range(len(parameter_values)):
                        tco2e_cost = carbon_cost_per_tco2e * parameter_values[cc]
                        plant_cost_items = roll_cost_items(
                            installed_capacity_mw,
                            construction_duration_years,
                            operational_lifetime_years,
                            decommissioning_duration_years,
                            overnight_capex_per_kw,
                            capex_contingency_factor,
                            foam_cost_factor,
                            voam_cost_per_mwh,
                            fuel_cost_per_tlng,
                            tco2e_cost,
                            decommissioning_cost_factor,
                            cf,
                            emission_factor_mtco2e_per_pj,
                            efficiency_rate,
                            exchange_rate,
                        )

                        cost_items = create_cost_items(plant_cost_items)
                        lcoe_per_kwh = calculate_lcoe(
                            revenue_item,
                            cost_items,
                            discount_rate,
                            exchange_rate,
                            PRESENT_YEAR,
                        )
                        plant_list.append(plant)
                        scenario_list.append(scenario)
                        parameter_list.append("Carbon costs")
                        value_list.append(parameter_values[cc])
                        lcoe_list.append(lcoe_per_kwh)

                if parameter == "exchange_rate":
                    for er in range(len(parameter_values)):
                        ex_rate = exchange_rate * parameter_values[er]
                        plant_cost_items = roll_cost_items(
                            installed_capacity_mw,
                            construction_duration_years,
                            operational_lifetime_years,
                            decommissioning_duration_years,
                            overnight_capex_per_kw,
                            capex_contingency_factor,
                            foam_cost_factor,
                            voam_cost_per_mwh,
                            fuel_cost_per_tlng,
                            carbon_cost_per_tco2e,
                            decommissioning_cost_factor,
                            cf,
                            emission_factor_mtco2e_per_pj,
                            efficiency_rate,
                            ex_rate,
                        )

                        cost_items = create_cost_items(plant_cost_items)
                        lcoe_per_kwh = calculate_lcoe(
                            revenue_item,
                            cost_items,
                            discount_rate,
                            exchange_rate,
                            PRESENT_YEAR,
                        )
                        plant_list.append(plant)
                        scenario_list.append(scenario)
                        parameter_list.append("Exchange rate")
                        value_list.append(parameter_values[er])
                        lcoe_list.append(lcoe_per_kwh)

                if parameter == "operational_lifetime":
                    for lt in range(len(parameter_values)):
                        lifetime_years = int(
                            operational_lifetime_years * parameter_values[lt]
                        )
                        plant_cost_items = roll_cost_items(
                            installed_capacity_mw,
                            construction_duration_years,
                            lifetime_years,
                            decommissioning_duration_years,
                            overnight_capex_per_kw,
                            capex_contingency_factor,
                            foam_cost_factor,
                            voam_cost_per_mwh,
                            fuel_cost_per_tlng,
                            carbon_cost_per_tco2e,
                            decommissioning_cost_factor,
                            cf,
                            emission_factor_mtco2e_per_pj,
                            efficiency_rate,
                            exchange_rate,
                        )

                        cost_items = create_cost_items(plant_cost_items)
                        lcoe_per_kwh = calculate_lcoe(
                            revenue_item,
                            cost_items,
                            discount_rate,
                            exchange_rate,
                            PRESENT_YEAR,
                        )
                        plant_list.append(plant)
                        scenario_list.append(scenario)
                        parameter_list.append("Lifetime")
                        value_list.append(parameter_values[lt])
                        lcoe_list.append(lcoe_per_kwh)

    lcoe_sensitivities = pd.DataFrame(
        {
            "Power Plant": plant_list,
            "Scenario": scenario_list,
            "Parameter": parameter_list,
            "Value": value_list,
            "LCOE": lcoe_list,
        }
    )

    return lcoe_sensitivities
