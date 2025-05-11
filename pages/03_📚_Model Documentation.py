import streamlit as st

from src.components.app_logo import show_app_logo

for k, v in st.session_state.items():
    st.session_state[k] = v

show_app_logo()

app_header = "Financial Modelling Tool for LNG-to-Power Projects"
app_body = """
    The Financial Modelling Tool (LNG2P-FM App) for LNG-to-Power Projects  is a web-based financial 
    modelling application designed to project electricity production from liquefied natural gas (LNG) 
    and financial viability of LNG-to-Power projects. It facilitates informed discussions and 
    decision-making among key stakeholders across the LNG-to-Power value chain, including:
    - Project developers – to model financial outcomes and assess project feasibility.
    - Financiers (investors) – to evaluate financial risks and potential returns.
    - Regulatory bodies – to analyze the impacts of regulations on project viability and sustainability."""

features_header = """Key Features"""
features_body = """
    - User-Friendly Interface: Allows stakeholders to quickly input data and generate financial models.
    - Customizable Scenarios: Users can simulate various project conditions and strategies by adjusting key assumptions.
    - Real-Time Collaboration: Enables stakeholders to share insights and feedback live, improving the decision-making process.
    - Comprehensive Reporting: Generates detailed reports on key financial metrics, aiding in quick assessment of project viability.
"""

casestudy_header = """Case Study Overview: LNG-to-Power Generation"""
casestudy_body = """The App is illustrated using a case study aligned with IRP2019 and NERSA determinations, 
    focusing on electricity generation from LNG."""

plant_utalization_header = """Plant Untalization Rate"""

plant_utalization_body = """
The study models three common types of power plant operations:
- Baseload: High, consistent output (high load factor).
- Mid-merit: Moderate, variable output (medium load factor).
- Peaking: Short bursts of output during peak demand (low load factor).

Each mode reflects a different capacity (load) factor, influencing LNG consumption and conversion efficiency. 
The App's dashboard includes a sidebar with sliders to adjust these load factors for scenario planning, 
and an edit panel to add and\or modify plant-specific technological parameters."""

visualization_header = """Visualization and Outputs"""
visualization_body = r"""On the 'LNG2P Dashboard' page, the App presents four key bar charts, generated from provided input parameters and assumptions:
1. Electricity Generation vs LNG Demand Projections
    - Left Y-Axis: Show electricity generated (Petajoules)
    - Right Y-Axis: Show required LNG imports (Million Tonnes Per Annum - MTPA)
    - Bottom X-Axis: Both Y-Axes are categorized into baseload, mid-merit, and peaking gas demand scenarios.
2. Greenhouse Gas Emissions ($$\text{CO}_2 $$ Equivalent)
    - Assesses emission reductions by replacing coal- and diesel-fired power plants with gas-fired power plants.
3. Lifetime Total Discounted Costs
    - Calculates the total present value of costs over the operational lifetime of a power plant.
4. Average Electricity Price (Break-Even Analysis)
    - Shows the average electricity price required for project to break-even over the plant’s lifetime.

These charts enable modern, fast-track evaluation of LNG-to-Power investment proposals.
"""
sensitivity_header = """Sensitivity Analysis"""
sensitivity_body = """On the 'LNG2P Sensitivities' page, the App allows stakeholders to test how variations 
in critical parameters affect project viability. Analyzed parameters include:
1. Discount rate
2. Load factor
3. Efficiency rate
4. Fuel costs
5. Carbon costs
6. Exchange rate
7. Plant operational lifetime

The resulting charts offer valuable insights into financial risks and levers for optimization.
"""


model_header = """The Financial Model: Levelised Cost of Electricity (LCOE)"""
model_body = """The financial model implemented in the LNG2P-FM App is based on the Levelised Cost of Electricity (LCOE). 
This is a standard metric used to evaluate the average cost of generating electricity over the lifetime of a power plant."""
lcoe_header = """Two Perspectives on LCOE"""
lcoe_body = """1. Revenue-Cost Equivalence: 
    - LCOE can be viewed as the price per unit of electricity that equates the present value of all 
revenues to the present value of all costs.
2. Cost Averaging: 
    - Alternatively, it represents the average total cost (capital, O&M, fuel, carbon, and decommissioning) 
per unit of electricity produced over the plant’s life."""

general_model_header = """ Equation 1: General LCOE Definition """
general_model_equation = r"""
    \begin{align}
    \underbrace{ {\sum_{s,t,y} \frac{\text{P}_{MWh} * \text{E}_{s,t,y}}{(1 + r_{t})^y}} }_{\text{Discounted Benefits}} = 
    \underbrace{{\sum_{s,t,y} \frac{(\text{CAPEX}_{s,t,y} + \text{FO\&M}_{s,t,y} + \text{VO\&M}_{s,t,y} + \text{Fuel}_{s,t,y} + 
    \text{Carbon}_{s,t,y} + \text{D}_{s,t,y})} {(1 + r_{t})^y}}}_{\text{Discounted Costs}}
    \end{align}"""


general_model_variables = r"""
Where:
- $ \text{P}_{MWh} : $ Constant unit price of electricity
- $ \text{E}_{s,t,y} : $ Electricity produced under scenario $s$, technology $t$, year $y$
- $ r : $ Discount rate
- $ \text{CAPEX}_{s,t,y},~\text{FO\&M}_{s,t,y},~\text{VO\&M}_{s,t,y},~\text{Fuel}_{s,t,y},~ 
    \text{Carbon}_{s,t,y},~\text{D}_{s,t,y} : $ Cost components
"""

solving_loc_header = """ Equation 2: Solving for LCOE """
solving_loc_body = r""" Assuming $\text{P}_{MWh}$ is constant over time:"""
solving_loc_equation = r"""
    \begin{align}
    \text{LCOE} = \text{P}_{MWh} = \frac{{\sum_{s,t,y} \frac{(\text{CAPEX}_{s,t,y} + \text{FO\&M}_{s,t,y} + \text{VO\&M}_{s,t,y} + 
    \text{Fuel}_{s,t,y} + \text{Carbon}_{s,t,y} + \text{D}_{s,t,y})} {(1 + r)^y}}}{\sum_{s,t,y} \frac{\text{E}_{s,t,y}} {(1 + r)^{y}}}
    \end{align}
    """
model_indices = r"""
$\textbf{Indices}$:
- $ s \in S : $ Load factor scenarios (e.g., baseload, mid-merit, peaking),
- $ t \in T : $ Power plants
- $ y \in Y : $ Operational years
"""
parameters_header = """Key Components of the Financial Model"""

parameters_body = r"""
1. $\textbf{Electricity Production and LNG Conversion} 
\newline$ Electricity output is calculated from:
$\newline~~~~~\text{E}_{s,t,y} = \text{Installed Capacity}_{t} \times \text{Load Factor} \times 8760 $
$\newline$ LNG volume is derived via:
$\newline~~~~~\text{Tonnes LNG} = \left(\frac{\text{E}_{s,t,y}} {\text{Efficiency Rate}} 
\times \text{LNG Conversion Factor} \right) $

2. $\textbf{Capital Expenditure (CAPEX)} \newline$ Includes:
    - Equipment and construction
    - Land acquisition
    - Grid interconnection
    - Regulatory compliance
    - etc. 

    Calculated as:
    $\newline~~~~~\text{CAPEX}_{s,t,y} = \text{Installed Capacity}_{t} \times \text{Unit Cost} $ 

3. $\textbf{Fixed Operating and Maintenance (FO\&M)} \newline$
Annual costs unrelated to energy output, including:
    - Routine maintenance
    - Administration and insurance 
    $\newline$ 

    Modeled as a percentage of total overnight costs.

4. $\textbf{Variable Operating and Maintenance (VO\&M)} \newline$ Costs that vary with output:
    - Lubricants
    - Unplanned repairs
    - etc. 

    Calculated as:
    $\newline~~~~~\text{VO\&M}_{s,t,y} = \text{E}_{s,t,y} \times \text{Cost per MWh} $ 

5. $\textbf{Fuel Costs} \newline $ Based on LNG consumption: 
$\newline~~~~~\text{Fuel Costs} = \text{Tonnes LNG} \times \text{LNG Unit Price} $

6. $\textbf{Carbon Costs} \newline$ Costs from $\text{CO}_{2}$ emissions:
$\newline~~~~~\text{Carbon Costs} = \left(\text{Tonnes LNG} \times \text{Emission Factor} 
 \right) \times \text{Carbon Price} $

 7. $\textbf{Decommissioning Costs} \newline$ 
 Reserves for end-of-life dismantling and site restoration, ensuring environmental and 
 financial closure.

"""

future_work_header = """ Future Development """
future_work_body = r""" The primary objective of financial modeling in the energy sector is to 
assess the financial viability of proposed energy projects. However, this process is 
often challenged by the energy trilemma—the need to balance three competing priorities: 
economic viability (e.g., revenue generation), environmental sustainability 
(e.g., emissions reduction), and social development (e.g., employment creation).
Currently, the LNG2P-FM App addresses environmental externalities solely through 
carbon tax policies, which serve as a proxy for $\text{CO}_2$ emissions regulation. While this 
is a critical step toward modeling environmental impact, it does not fully capture 
the broader range of externalities and incentives that influence project feasibility. """

planned_work_header = """Planned Enhancements"""
planned_work_body = r"""Future development of the App will focus on:$\newline$
- Enhancing the cost structure of the financial model to incorporate additional regulatory and fiscal externalities.
- Accounting for government incentives, such as tax credits or feed-in tariffs.
- Including social costs and benefits, such as employment generation and local economic development impacts.
- Adapting to jurisdiction-specific policies that may affect project financing, cost recovery, or environmental compliance.

These improvements aim to create a more comprehensive tool for stakeholders to evaluate 
LNG-to-Power projects within the complex policy and economic landscapes in which they operate.
"""

st.header(app_header)
st.write(app_body)
st.subheader(features_header)
st.write(features_body)
st.header(casestudy_header)
st.write(casestudy_body)
st.subheader(plant_utalization_header)
st.write(plant_utalization_body)
st.subheader(visualization_header)
st.write(visualization_body)
st.subheader(sensitivity_header)
st.write(sensitivity_body)
st.header(model_header)
st.write(model_body)
st.subheader(lcoe_header)
st.write(lcoe_body)
st.subheader(general_model_header)
st.latex(general_model_equation)
st.write(general_model_variables)
st.subheader(solving_loc_header)
st.write(solving_loc_body)
st.latex(solving_loc_equation)
st.write(model_indices)
st.subheader(parameters_header)
st.write(parameters_body)
st.header(future_work_header)
st.write(future_work_body)
st.subheader(planned_work_header)
st.write(planned_work_body)
