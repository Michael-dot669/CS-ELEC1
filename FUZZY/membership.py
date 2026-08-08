
def low(value):
    if value <= 30:
        return 1
    elif value < 50:
        return (50 - value) / 20
    else:
        return 0


def medium(value):
    if 30 < value < 50:
        return (value - 30) / 20
    elif 50 <= value < 70:
        return (70 - value) / 20
    else:
        return 0


def high(value):
    if value >= 70:
        return 1
    elif value > 50:
        return (value - 50) / 20
    else:
        return 0