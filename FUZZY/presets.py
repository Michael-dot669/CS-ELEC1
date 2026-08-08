def set_blur(level, slider):

    if level == "clear":
        slider.set(10)

    elif level == "medium":
        slider.set(50)

    elif level == "blurry":
        slider.set(85)


def set_strain(level, slider):

    if level == "relaxed":
        slider.set(10)

    elif level == "medium":
        slider.set(50)

    elif level == "tired":
        slider.set(85)