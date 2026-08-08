from membership import low, medium, high

def check_eye_condition(blur, strain, distance):

    blur_low = low(blur)
    blur_medium = medium(blur)
    blur_high = high(blur)

    strain_low = low(strain)
    strain_medium = medium(strain)
    strain_high = high(strain)
    
    distance_near = low(distance)
    distance_normal = medium(distance)
    distance_far = high(distance)

    good = max(
        min(blur_low, strain_low, distance_normal),
        min(blur_low, strain_low, distance_far)
    )

    moderate = max(
        min(blur_medium, strain_medium),
        min(blur_low, strain_high),
        min(blur_high, strain_low)
    )

    bad = max(
        min(blur_high, strain_high),
        min(blur_high, distance_near),
        min(strain_high, distance_near)
    )

    total = good + moderate + bad

    if total == 0:
        return "No Result"

    score = (
        (good * 1) +
        (moderate * 2) +
        (bad * 3)
    ) / total

    if score < 1.5:
        return "GOOD"
    elif score < 2.5:
        return "MODERATE"
    else:
        return "BAD"