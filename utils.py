def convert_price_to_float(price_str: str) -> float:
    """Utility to convert price string to a float."""
    return float(price_str.replace("₹", "").replace(",", ""))