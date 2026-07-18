# =====================================================
# PASSWORD CRACK TIME ESTIMATOR
# Version 5.0 Professional
# =====================================================

from typing import Dict

# =====================================================
# CRACK TIME ESTIMATION
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
        Human-readable crack time estimate.
    """

    if entropy < 28:
        return "Instant"

    elif entropy < 36:
        return "A Few Seconds"

    elif entropy < 45:
        return "Several Minutes"

    elif entropy < 52:
        return "Several Hours"

    elif entropy < 60:
        return "Several Days"

    elif entropy < 68:
        return "Several Months"

    elif entropy < 80:
        return "Several Years"

    elif entropy < 96:
        return "Centuries"

    elif entropy < 112:
        return "Thousands of Years"

    elif entropy < 128:
        return "Millions of Years"

    else:
        return "Practically Unbreakable"


# =====================================================
# SECURITY LEVEL
# =====================================================

def security_level(entropy: float) -> str:
    """
    Return security level based on entropy.
    """

    if entropy < 28:
        return "Very Weak"

    elif entropy < 45:
        return "Weak"

    elif entropy < 60:
        return "Moderate"

    elif entropy < 80:
        return "Strong"

    elif entropy < 100:
        return "Very Strong"

    else:
        return "Excellent"


# =====================================================
# SECURITY COLOR
# =====================================================

def security_color(entropy: float) -> str:
    """
    Return UI color based on entropy.
    """

    if entropy < 28:
        return "#DC2626"      # Red

    elif entropy < 45:
        return "#EA580C"      # Orange

    elif entropy < 60:
        return "#D97706"      # Amber

    elif entropy < 80:
        return "#16A34A"      # Green

    elif entropy < 100:
        return "#2563EB"      # Blue

    return "#7C3AED"          # Purple


# =====================================================
# COMPLETE REPORT
# =====================================================

def crack_report(entropy: float) -> Dict[str, str]:
    """
    Return complete crack-time report.
    """

    return {
        "entropy": f"{entropy:.2f} bits",
        "crack_time": crack_time(entropy),
        "security_level": security_level(entropy),
        "color": security_color(entropy),
    }


# =====================================================
# SECURITY SCORE
# =====================================================

def security_score(entropy: float) -> int:
    """
    Return security score (0-100).
    """

    score = int(min(entropy / 128 * 100, 100))
    return max(score, 0)