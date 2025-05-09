def load_plant_data(data):
    plants = {}
    for i in range(len(data)):
        plant = data.iloc[i, 0]

        plants[plant] = {}
        plants[plant]["installed_capacity_mw"] = float(data.iloc[i, 1])
        plants[plant]["construction_duration_years"] = int(data.iloc[i, 2])
        plants[plant]["overnight_capex_per_kw"] = float(data.iloc[i, 3])
        plants[plant]["operational_lifetime_years"] = int(data.iloc[i, 4])
        plants[plant]["foam_cost_factor"] = float(data.iloc[i, 5])
        plants[plant]["voam_cost_per_mwh"] = float(data.iloc[i, 6])
        plants[plant]["fuel_cost_per_tLNG"] = float(data.iloc[i, 7])
        plants[plant]["carbon_cost_per_tCO2e"] = float(data.iloc[i, 8])
        plants[plant]["decommissioning_duration_years"] = int(data.iloc[i, 9])
        plants[plant]["capex_contingency_factor"] = float(data.iloc[i, 10])
        plants[plant]["decommissioning_cost_factor"] = float(data.iloc[i, 11])
        plants[plant]["efficiency_rate"] = float(data.iloc[i, 12])
        plants[plant]["emission_factor_mtco2e_per_pj"] = float(data.iloc[i, 13])
        plants[plant]["discount_rate"] = float(data.iloc[i, 14])
        plants[plant]["exchange_rate"] = float(data.iloc[i, 15])

    return plants


# FIXME: is not currently used, since the data type problem.
def load_scenario_data(data):
    scenarios = {}
    scenarios["Peaking"] = float(data.iloc[0, 0])
    scenarios["Mid-merit"] = float(data.iloc[0, 1])
    scenarios["Baseload"] = float(data.iloc[0, 2])

    return scenarios


def load_emission_factors_data(data):
    emission_factors = {}
    for i in range(len(data)):
        emission_factors[data.iloc[i, 0]] = float(data.iloc[i, 1])

    return emission_factors


def load_sensitivity_data(data):
    sensitivities = {}
    sensitivities["discount_rate"] = data["discount_rate"].to_list()
    sensitivities["capacity_factor"] = data["capacity_factor"].to_list()
    sensitivities["efficiency_rate"] = data["efficiency_rate"].to_list()
    sensitivities["fuel_cost"] = data["fuel_cost"].to_list()
    sensitivities["carbon_cost"] = data["carbon_cost"].to_list()
    sensitivities["exchange_rate"] = data["exchange_rate"].to_list()
    sensitivities["operational_lifetime"] = data["operational_lifetime"].to_list()

    return sensitivities
