"""Shared display-formatting helpers used across pages."""


def format_percent(value: float, decimals: int = 1) -> str:
    """Format a 0-1 fraction as a percentage string, e.g. 0.635 -> '63.5%'."""
    return f"{value:.{decimals}%}"
