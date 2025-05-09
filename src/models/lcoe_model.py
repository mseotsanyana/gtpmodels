from src.models.lng_demand_model import (
    electricity_demand_pj_mtco2e,
    electricity_output_mwh,
    feedstock_demand_mtpa,
)
from src.utils.constants import MILLION, PRESENT_YEAR, THOUSAND


class LCOEData:
    """Holds all data required to calculate net present value (NPV)"""

    def __init__(self, years, values, discount_rate=None):
        self.years = years
        self.values = values
        self.discount_rate = discount_rate

    def net_present_value(self, present_year, external_discount_rate=None):
        """
            Calculate net present value (NPV) given data which include years of
            a project lifetime, costs or revenue of the project and a discount
            rate.

            Args:
                present_year (int): Current year of the project.
                external_discount_rate (float, optional): Discount rate for
                the costs and revenue.

        Returns:
            Net present value (NPV).
        """
        discount_rate = (
            external_discount_rate
            if external_discount_rate is not None
            else self.discount_rate
        )
        if discount_rate is None:
            raise ValueError(
                "Discount rate needs to be specified, "
                "either as a member object or as an argument to this method."
            )
        npv = 0.0
        for year, value in zip(self.years, self.values):
            periods_into_future = year - present_year
            npv += value / (1 + discount_rate) ** periods_into_future
        return npv


def create_cash_flow(expense_tuple, discount_rate=None):
    """
    Create a LCOEData object.

    Args:
        expense_tuple (tuple): Tuple containing (start_year, end_year, expense_value).
        discount_rate (float, optional): Discount rate for the cas flow.

    Returns:
        LCOEData object.
    """
    start_year, end_year, expense_value = expense_tuple
    years = list(range(start_year, end_year + 1))

    return LCOEData(years, [expense_value for y in years], discount_rate)


def create_cost_item(cost_item_name, expense_tuple, discount_rate=None):
    """
    Create a cost item dictionary entry.

    Args:
        cost_item_name (str): Name of the cost item.
        expense_tuple (tuple): Tuple containing (start_year, end_year, expense_value).
        discount_rate (float, optional): Discount rate for the cost item.

    Returns:
        dict: Cost item dictionary entry with appropriate structure.
    """

    cost_item = {cost_item_name: create_cash_flow(expense_tuple, discount_rate)}

    return cost_item


def unroll_cost_item(cost_item_name, expense_data):
    """
    Body of the function below.
    """
    if isinstance(expense_data, tuple) and len(expense_data) == 3:
        # If expense_data is a tuple, assume it contains
        # (start_year, end_year, expense_value)
        cost_item = create_cost_item(cost_item_name, expense_data)
    elif isinstance(expense_data, tuple) and len(expense_data) == 4:
        # If it is 4 elements, assume it contains
        # (start_year, end_year, expense_value, discount_rate)
        cost_item = create_cost_item(
            cost_item_name, expense_data[:-1], expense_data[-1]
        )
    else:
        raise ValueError("Invalid format for expense data.")

    return cost_item


def create_cost_items(cost_items_rolled):
    """
    Create cost_items dictionary from cost_items_rolled.

    Args:
        cost_items_rolled (dict): Dictionary with cost_item_name
        as keys and expense_tuple as values, possibly including
        discount_rate.

    Returns:
        dict: Dictionary with cost_item_name as keys
              and corresponding expense tuples in the format used
              in cost_items.
    """
    cost_items = {}  # Initialize the cost_items dictionary
    for cost_item_name, expense_data in cost_items_rolled.items():
        cost_item = unroll_cost_item(cost_item_name, expense_data)
        cost_items.update(cost_item)

    return cost_items


def create_revenue_item(revenue_item_rolled):
    revenue_item = {}
    for revenue_item_name, revenue_item_rolled in revenue_item_rolled.items():
        revenue_data = create_cash_flow(revenue_item_rolled)
        revenue_item[revenue_item_name] = revenue_data

    return revenue_item


def discount_cash_flows(cost_items, default_discount_rate, present_year):
    """
    Calculate the discounted cash flows for all cost items.

    Args:
        cost_items (dict): Dictionary of cost items where keys are cost item names,
                           and values are CashFlowData objects.
        default_discount_rate (float): Default discount rate to be used
                                       if not specified for a cost item.
        present_year (int): The year against which all cash flows should be discounted.

    Returns:
        dict: Dictionary containing net present value for each cost item.
    """
    discounted_cash_flows = {}
    for cash_flow_name, cash_flow_data in cost_items.items():
        item_discount_rate = cash_flow_data.discount_rate or default_discount_rate
        discounted_cash_flows[cash_flow_name] = cash_flow_data.net_present_value(
            present_year, item_discount_rate
        )

    return discounted_cash_flows


def calculate_lcoe(
    revenue_data, cost_items, default_discount_rate, exchange_rate, present_year
):
    """
    Calculate the Levelised Cost of Energy (LCOE) for an energy infrastructure
    project.

    Args:
        cost_items (dict): Dictionary of cost items where keys are cost item
        names, and values are LCOEData objects.
        revenue_data (LCOEData): LCOEData object for revenue data.
        default_discount_rate (float): Default discount rate to be used
        if not specified for a cost item.
        present_year (int): The year against which all cash flows should be
        discounted.

        exchange_rate:

    Returns:
        float: LCOE in R/MWh.


    """
    revenue_discount_rate = revenue_data.discount_rate or default_discount_rate
    total_discounted_revenue = revenue_data.net_present_value(
        present_year, revenue_discount_rate
    )

    discounted_expenses = discount_cash_flows(
        cost_items, default_discount_rate, present_year
    )
    total_discounted_expenses = 0.0
    for _, discounted_expense in discounted_expenses.items():
        total_discounted_expenses += discounted_expense

    lcoe = round(
        ((total_discounted_expenses / total_discounted_revenue) * exchange_rate)
        / THOUSAND,
        2,
    )  # R/kWh

    return lcoe


### cost calculations


def overnight_capex_util(
    installed_capacity_mw, overnight_capex_per_kw, capex_contingency, exchange_rate
):
    # capital cost
    installed_capacity_kw = installed_capacity_mw * THOUSAND  # kW
    overnight_total_capex = overnight_capex_per_kw * installed_capacity_kw  # $
    overnight_capex_with_contingency = (
        overnight_total_capex * (1 + capex_contingency)
    ) * exchange_rate  # R

    return overnight_capex_with_contingency


def overnight_capex(
    installed_capacity_mw,
    construction_duration,
    overnight_capex_per_kw,
    capex_contingency,
    exchange_rate,
):
    """Capital costs (CAPEX)."""
    # capital cost
    capex_per_year = (
        overnight_capex_util(
            installed_capacity_mw,
            overnight_capex_per_kw,
            capex_contingency,
            exchange_rate,
        )
        / construction_duration
    )  # R/year

    return capex_per_year


def fixed_oam_cost(
    installed_capacity_mw,
    construction_duration,
    overnight_capex_per_kw,
    capex_contingency,
    exchange_rate,
    fixed_oam_cost_factor,
):
    """Fixed operational and maintenance costs (FO&M)."""
    # O&M cost
    foam_cost_per_year = (
        overnight_capex(
            installed_capacity_mw,
            construction_duration,
            overnight_capex_per_kw,
            capex_contingency,
            exchange_rate,
        )
        * fixed_oam_cost_factor  # R/year
    )

    return foam_cost_per_year


# def fixed_oam_cost(installed_capacity_mw, foam_cost):
#     # O&M cost
#     foam_cost_per_year = foam_cost * installed_capacity_mw
#
#     return foam_cost_per_year


def variable_oam_cost(
    installed_capacity_mw, voam_cost_per_mwh, capacity_factor, exchange_rate
):
    """Variable operational and maintenance cost (VO&M)."""
    voam_cost_per_year = (
        voam_cost_per_mwh  # $/MWh
        * electricity_output_mwh(installed_capacity_mw, capacity_factor)  # MWh/year
        * exchange_rate
    )  # R/year

    return voam_cost_per_year


def fuel_cost(
    installed_capacity_mw,
    fuel_cost_per_ton_lng,
    capacity_factor,
    efficiency_factor,
    exchange_rate,
):
    """Liquified natural gas (LNG) costs."""
    feedstock_MtLNG = feedstock_demand_mtpa(
        installed_capacity_mw, capacity_factor, efficiency_factor
    )  # Mt of LNG
    feedstock_ton_lng = feedstock_MtLNG * MILLION  # tonnes of LNG
    fuel_cost_per_year = (
        fuel_cost_per_ton_lng * feedstock_ton_lng * exchange_rate
    )  # R/Year

    return fuel_cost_per_year


def carbon_cost(
    installed_capacity,
    capacity_factor,
    emission_factor,
    carbon_cost_per_tco2e,
    exchange_rate,
):
    """Greenhouse gas (GHG) emission costs."""
    mtco2e = electricity_demand_pj_mtco2e(
        installed_capacity, capacity_factor, emission_factor
    )
    # carbon
    tco2e = mtco2e * MILLION
    carbon_cost_per_year = (carbon_cost_per_tco2e * tco2e) * exchange_rate  # R

    return carbon_cost_per_year


def decommissioning_cost(
    installed_capacity_mw,
    overnight_capex_per_kw,
    capex_contingency,
    decommissioning_duration,
    decommissioning_cost_factor,
    exchange_rate,
):
    """Power plant decomissioning costs."""
    decommission_cost = decommissioning_cost_factor * overnight_capex_util(
        installed_capacity_mw, overnight_capex_per_kw, capex_contingency, exchange_rate
    )
    decommissioning_cost_per_year = decommission_cost / decommissioning_duration

    return decommissioning_cost_per_year


## construction timelines
def start_of_construction_period():
    return PRESENT_YEAR


def end_of_construction_period(construction_duration):
    construction_end = start_of_construction_period() + construction_duration - 1
    return construction_end


## operation timeline
def start_of_operation_period(construction_duration):
    operation_start = end_of_construction_period(construction_duration) + 1
    return operation_start


def end_of_operation_period(construction_duration, operational_lifetime):
    operation_end = (
        start_of_operation_period(construction_duration) + operational_lifetime - 1
    )
    return operation_end


## decommissioning timeline
def start_of_decommissioning_period(construction_duration, operational_lifetime):
    decommissioning_start = (
        end_of_operation_period(construction_duration, operational_lifetime) + 1
    )
    return decommissioning_start


def end_of_decommissioning_period(
    construction_duration, operational_lifetime, decommissioning_duration
):
    decommissioning_end = (
        start_of_decommissioning_period(construction_duration, operational_lifetime)
        + decommissioning_duration
        - 1
    )
    return decommissioning_end


def roll_cost_items(
    installed_capacity_mw,
    construction_duration,
    operational_lifetime,
    decommissioning_duration,
    overnight_capex_per_kw,
    capex_contingency,
    foam_cost_factor,
    voam_cost_per_mwh,
    fuel_cost_per_tlng,
    carbon_cost_per_tco2e,
    decommissioning_cost_factor,
    capacity_factor,
    emission_factor,
    efficiency_factor,
    exchange_rate,
):
    # construction period
    construction_start = PRESENT_YEAR
    construction_end = end_of_construction_period(construction_duration)

    # operational period
    operation_start = start_of_operation_period(construction_duration)
    operation_end = end_of_operation_period(construction_duration, operational_lifetime)

    # decommissioning period
    decommissioning_start = start_of_decommissioning_period(
        construction_duration, operational_lifetime
    )
    decommissioning_end = end_of_decommissioning_period(
        construction_duration, operational_lifetime, decommissioning_duration
    )

    ## CAPEX

    capex_per_year = overnight_capex(
        installed_capacity_mw,
        construction_duration,
        overnight_capex_per_kw,
        capex_contingency,
        exchange_rate,
    )

    ## OPEX

    # FO&M costs
    foam_cost_per_year = fixed_oam_cost(
        installed_capacity_mw,
        construction_duration,
        overnight_capex_per_kw,
        capex_contingency,
        exchange_rate,
        foam_cost_factor,
    )

    # VO&M costs
    voam_cost_per_year = variable_oam_cost(
        installed_capacity_mw, voam_cost_per_mwh, capacity_factor, exchange_rate
    )

    ## FEEDSTOCK FUEL

    # fuel costs
    fuel_cost_per_year = fuel_cost(
        installed_capacity_mw,
        fuel_cost_per_tlng,
        capacity_factor,
        efficiency_factor,
        exchange_rate,
    )

    ## CARBON EMISSIONS

    # carbon costs
    carbon_cost_per_year = carbon_cost(
        installed_capacity_mw,
        capacity_factor,
        emission_factor,
        carbon_cost_per_tco2e,
        exchange_rate,
    )

    ## DECOMMISSIONING COSTS

    # decommissioning costs
    decommissioning_cost_per_year = decommissioning_cost(
        installed_capacity_mw,
        overnight_capex_per_kw,
        capex_contingency,
        decommissioning_duration,
        decommissioning_cost_factor,
        exchange_rate,
    )

    cost_items_rolled = {
        "CAPEX": (construction_start, construction_end, capex_per_year),
        "FO&M": (operation_start, operation_end, foam_cost_per_year),
        "VO&M": (operation_start, operation_end, voam_cost_per_year),
        "Fuel": (operation_start, operation_end, fuel_cost_per_year),
        "Carbon": (operation_start, operation_end, carbon_cost_per_year),
        "Decommissioning": (
            decommissioning_start,
            decommissioning_end,
            decommissioning_cost_per_year,
        ),
    }

    return cost_items_rolled
