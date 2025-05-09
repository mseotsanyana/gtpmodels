import pandas as pd

from financial_model_app.src.utils.constants import HOURS_IN_YEAR, MWH_TO_PJ, PJ_TO_MTPA


def electricity_output_mwh(installed_capacity_mw, capacity_factor):
    """
    Calculate the electricity output from a power plant.

    Args:
        installed_capacity : installed capacity of a power plant in megawatts.
        capacity_factor : capacity factor of a power plant.

    Returns:
        generated electricity in megawatts hour.
    """
    output_mwh_per_year = HOURS_IN_YEAR * installed_capacity_mw * capacity_factor

    return output_mwh_per_year


def electricity_input_mwh(installed_capacity_mw, capacity_factor, efficiency_factor):
    # electricity demand (MWh/year)
    input_mwh_per_year = (
        electricity_output_mwh(installed_capacity_mw, capacity_factor)
        / efficiency_factor
    )

    return input_mwh_per_year


def electricity_demand_pj(installed_capacity_mw, capacity_factor):
    # electricity demand (PJ/year)
    mwh_per_year = electricity_output_mwh(installed_capacity_mw, capacity_factor)
    output_pj_per_year = mwh_per_year * MWH_TO_PJ

    return output_pj_per_year


def electricity_demand_pj_mtco2e(
    installed_capacity_mw, capacity_factor, emission_factor_mtco2e_per_pj
):
    # LNG CO2 equivalent  (MtCO2e/year)
    output_pj_per_year = electricity_demand_pj(installed_capacity_mw, capacity_factor)
    mtco2e_per_year = (
        output_pj_per_year * emission_factor_mtco2e_per_pj
    )  # PJ/year * MtCO2e/PJ = MtCO2e/year

    return mtco2e_per_year


def feedstock_demand_mtpa(installed_capacity_mw, capacity_factor, efficiency_factor):
    # LNG demand (MTPA/year)
    mwh_per_year = electricity_input_mwh(
        installed_capacity_mw, capacity_factor, efficiency_factor
    )
    input_mtpa_per_year = (mwh_per_year * MWH_TO_PJ) * PJ_TO_MTPA

    return input_mtpa_per_year
