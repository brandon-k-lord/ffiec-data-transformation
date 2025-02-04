from typing import List


def normalize_headers(headers: List[str]) -> List[str]:
    """
    Normalizes headers read from files to simplify sql statements.

    Parameters:
    - headers: list of column headers
    """
    return [header.replace("#", "").lower().strip() for header in headers]
