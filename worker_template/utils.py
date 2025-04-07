###############################################################################
##
##  (C) Copyright 2025 EVERYSK TECHNOLOGIES
##
##  This is an unpublished work containing confidential and proprietary
##  information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
##  without authorization of EVERYSK TECHNOLOGIES is prohibited.
##
###############################################################################

###############################################################################
# Imports
###############################################################################


###############################################################################
# Implementation
###############################################################################
def sample_function(value: str) -> str:
    """
    Example of a external function from another file inside the worker folder.

    Args:
        value (str): Input string.

    Returns:
        str: Output string
    """
    return f"new value is: {value}!!"
