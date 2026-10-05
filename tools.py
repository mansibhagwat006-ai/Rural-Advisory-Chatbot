from langchain_core.tools import tool

@tool 
def calculate_emi(principal: float , annual_rate: float , months: int ) -> dict:
    """Calculate monthly EMI, total interest and total repayment for a loan.
    principal in rupees, annual_rate in percent per year, months = loan tenure in months."""
    if months <= 0:
        return {"ERROR":"Tenure must be atleast 1 month"} 
    r = annual_rate/12/100
    if r == 0:
        emi = principal / months 
    else:
        emi = principal * r* (1+r)** months/((1+r)**months - 1)
    total = emi*months
    return {
        "emi": round(emi),
        "total_interest":round(total - principal),
        "total_repayment": round(total)
    }

@tool
def monthly_profit(revenue: float, cost: float, other_expenses: float = 0) -> dict:
    """Calculate monthly profit and profit margin percentage from monthly
    revenue, cost of goods, and other expenses (rent, wages, electricity)."""
    profit = revenue - cost - other_expenses
    margin = round(profit / revenue * 100, 1) if revenue else 0
    return {"profit": round(profit), "margin_pct": margin}


@tool
def break_even(fixed_costs: float, price_per_unit: float, cost_per_unit: float) -> dict:
    """Calculate how many units must be sold to break even."""
    margin = price_per_unit - cost_per_unit
    if margin <= 0:
        return {"error": "Selling price must be higher than cost per unit"}
    return {"break_even_units": round(fixed_costs / margin)}


@tool
def loan_affordability(monthly_profit_amount: float, emi: float) -> dict:
    """Check whether a loan EMI is affordable. A common safe rule is that
    EMI should be at most 40 percent of monthly profit."""
    if monthly_profit_amount <= 0:
        return {"affordable": False, "reason": "No monthly profit"}
    ratio = emi / monthly_profit_amount * 100
    return {"emi_to_profit_pct": round(ratio, 1), "affordable": ratio <= 40}
