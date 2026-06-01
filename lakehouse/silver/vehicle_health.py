def calculate_health_score(
    battery,
    engine_temp,
    fault_code
):

    score = 100

    if battery < 20:
        score -= 30

    if battery < 10:
        score -= 20

    if engine_temp > 115:
        score -= 25

    if engine_temp > 130:
        score -= 15

    if fault_code:
        score -= 20

    return max(score, 0)