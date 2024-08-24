import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  
    WHITE = 4  


def latest_financial_index(data: dict):
    
    financials = data.get("data", {}).get("financials", [])
    for index, financial in enumerate(financials):
        nature_value = financial.get("nature", "").strip().upper()
        print(f"Index: {index}, Nature: '{nature_value}'")

        if nature_value == "STANDALONE":
            print(f"Found 'STANDALONE' at index {index}")
            return index

    print("No 'STANDALONE' entry found.")
    return -1



def total_revenue(data: dict, index: int) -> float:

    financials = data.get("data", {}).get("financials", [])
    
    if 0 <= index < len(financials):
    
        pnl = financials[index].get("pnl", {})
        revenue_breakup = pnl.get("revenue_breakup", {})
        
    
        total_revenue = (
            revenue_breakup.get("sale_or_supply_of_services_domestic", 0) +
            revenue_breakup.get("sale_or_supply_of_services_export", 0)
        )
        
        return float(total_revenue)
    
    return 0.0





def total_borrowing(data: dict, index: int) -> float:
    
    financials = data.get("data", {}).get("financials", [])
    
    if 0 <= index < len(financials):
    
        bs = financials[index].get("bs", {})
        liabilities = bs.get("liabilities", {})
        
        long_term_borrowings = liabilities.get("long_term_borrowings", 0)
        short_term_borrowings = liabilities.get("short_term_borrowings", 0)
        
        total_borrowings = long_term_borrowings + short_term_borrowings
        
        
        return float(total_borrowings)
    
    return 0.0


def iscr(data: dict, financial_index: int) -> float:
    """
    Calculate the Interest Service Coverage Ratio (ISCR) for the financial data at the given index.

    ISCR is a ratio that measures how well a company can cover its interest payments on outstanding debt.
    It is calculated as the sum of profit before interest and tax, and depreciation, increased by 1,
    divided by the sum of interest expenses increased by 1. The addition of 1 is to avoid division by zero.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - float: The ISCR value.
    """
    financials = data.get("data", {}).get("financials", [])
    
    if 0 <= financial_index < len(financials):
        pnl = financials[financial_index].get("pnl", {})
        line_items = pnl.get("lineItems", {})
        
        profit_before_interest_and_tax = line_items.get("profit_before_interest_and_tax", 0)
        depreciation = line_items.get("depreciation", 0)
        interest_expense = line_items.get("interest", 0)
        
        
        numerator = profit_before_interest_and_tax + depreciation + 1
        denominator = interest_expense + 1
        
        if denominator != 0:
            return numerator / denominator
    
    return 0.0

def iscr_flag(data: dict, financial_index: int) -> str:
    """
    Determine the flag color based on the Interest Service Coverage Ratio (ISCR) value.

    This function calculates the ISCR value by calling the `iscr` function and then assigns a flag color
    based on the ISCR value. If the ISCR value is greater than or equal to 2, it assigns a GREEN flag,
    otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - str: The flag color based on the ISCR value. ("GREEN" or "RED")
    """
    isc_value = iscr(data, financial_index)
    
    if isc_value >= 2:
        return "GREEN"
    else:
        return "RED"

def total_revenue_5cr_flag(data: dict, financial_index: int) -> str:
    """
    Determine the flag color based on whether the total revenue exceeds 50 million.

    This function calculates the total revenue by calling the `total_revenue` function and then assigns
    a flag color based on the revenue amount. If the total revenue is greater than or equal to 50 million,
    it assigns a GREEN flag, otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the revenue calculation.

    Returns:
    - str: The flag color based on the total revenue. ("GREEN" or "RED")
    """
    total_revenue_value = total_revenue(data, financial_index)
    
    if total_revenue_value >= 50000000:
        return "GREEN"
    else:
        return "RED"

def borrowing_to_revenue_flag(data: dict, financial_index: int) -> str:
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.

    This function calculates the ratio of total borrowings to total revenue by calling the `total_borrowing`
    function and then assigns a flag color based on the calculated ratio. If the ratio is less than or equal
    to 0.25, it assigns a GREEN flag, otherwise, it assigns an AMBER flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ratio calculation.

    Returns:
    - str: The flag color based on the borrowing to revenue ratio. ("GREEN" or "AMBER")
    """
    
    ratio = total_borrowing(data, financial_index)
    
    if ratio <= 0.25:
        return "GREEN"
    else:
        return "AMBER"

