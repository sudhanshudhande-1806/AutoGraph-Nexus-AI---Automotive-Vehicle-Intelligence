def classify_risk(score):

    if score >= 80:
        return "LOW"

    if score >= 50:
        return "MEDIUM"

    return "HIGH"


def vehicle_status(score):

    if score >= 80:
        return "HEALTHY"

    if score >= 50:
        return "ATTENTION_REQUIRED"

    return "CRITICAL"