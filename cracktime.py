# =====================================================
# PASSWORD CRACK TIME ESTIMATOR
# Version 4.0 Professional
# =====================================================

def crack_time(entropy: float) -> str:
    """
    Estimate password crack time based on entropy.

    Parameters
    ----------
    entropy : float
        Password entropy in bits.

    Returns
    -------
    str
        Human-readable estimated crack time.
    """

    if entropy < 28:
        return "Instant"

    elif entropy < 36:
        return "Seconds"

    elif entropy < 45:
        return "Minutes"

    elif entropy < 60:
        return "Hours"

    elif entropy < 72:
        return "Days"

    elif entropy < 80:
        return "Months"

    elif entropy < 96:
        return "Years"

    elif entropy < 112:
        return "Centuries"

    elif entropy < 128:
        return "Thousands of Years"

    else:
        return "Practically Unbreakable"