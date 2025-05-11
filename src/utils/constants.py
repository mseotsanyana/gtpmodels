PRESENT_YEAR = 1
HOURS_IN_YEAR = 8760
MWH_TO_PJ = pow(10, -6) * 3.6
PJ_TO_MTPA = 1 / 52

THOUSAND = 1000
MILLION = 1000000
BILLION = 1000000000


# Define data labels
def parameter_labels():
    labels = {
        "installed_capacity_mw": "Installed capacity (MW)",
        "construction_duration_years": "Construction duration (years)",
        "overnight_capex_per_kw": "Overnight cost ($/kW)",
        "operational_lifetime_years": "Operational lifetime (years)",
        "foam_cost_factor": "FO&M cost factor (%)",
        "voam_cost_per_mwh": "VO&M cost ($/MWh)",
        "fuel_cost_per_tLNG": "Fuel cost ($/ton LNG)",
        "carbon_cost_per_tCO2e": "Cost of carbon ($/t CO2e)",
        "decommissioning_duration_years": "Decommissioning duration (years)",
        "capex_contingency_factor": "Capital cost contingency factor (%)",
        "decommissioning_cost_factor": "Decommissioning cost factor (%)",
        "efficiency_rate": "Efficiency rate (%)",
        "emission_factor_mtco2e_per_pj": "Emission factor (Number)",
        "discount_rate": "Discount rate (%)",
        "exchange_rate": "Exchange rate (R/$)",
    }

    return labels


def parameter_step_values():
    # Define step values
    step_values = {
        "installed_capacity_mw": 100.0,
        "construction_duration_years": 1,
        "overnight_capex_per_kw": 100.0,
        "operational_lifetime_years": 1,
        "foam_cost_factor": 0.05,
        "voam_cost_per_mwh": 0.5,
        "fuel_cost_per_tLNG": 0.5,
        "carbon_cost_per_tCO2e": 0.5,
        "decommissioning_duration_years": 1,
        "capex_contingency_factor": 0.05,
        "decommissioning_cost_factor": 0.05,
        "efficiency_rate": 0.05,
        "emission_factor_mtco2e_per_pj": 0.05,
        "discount_rate": 0.05,
        "exchange_rate": 0.05,
    }

    return step_values
