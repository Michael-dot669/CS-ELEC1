import tkinter as tk

from fuzzy_logic import check_eye_condition
from presets import set_blur, set_strain

def create_gui():

    root = tk.Tk()

    root.title("Simple Fuzzy Eye Test")
    root.geometry("520x700")
    root.resizable(False, False)

    title = tk.Label(
        root,
        text="FUZZY LOGIC EYE TEST",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=(20, 5))

    subtitle = tk.Label(
        root,
        text="Simple eye condition assessment",
        font=("Arial", 10)
    )
    subtitle.pack(pady=(0, 15))

    tk.Label(
        root,
        text="1. Vision / Blur Level",
        font=("Arial", 11, "bold")
    ).pack()

    blur_status = tk.Label(
        root,
        text="Vision: Clear vision",
        font=("Arial", 9)
    )
    blur_status.pack()

    def update_blur(value):

        value = int(float(value))

        if value <= 30:
            text = "Clear vision"
        elif value <= 65:
            text = "Slightly blurry"
        else:
            text = "Very blurry"

        blur_status.config(
            text="Vision: " + text
        )

    blur_slider = tk.Scale(
        root,
        from_=0,
        to=100,
        orient="horizontal",
        length=380,
        command=update_blur
    )

    blur_slider.set(10)
    blur_slider.pack()

    blur_buttons = tk.Frame(root)
    blur_buttons.pack(pady=5)

    tk.Button(
        blur_buttons,
        text="Clear",
        width=10,
        command=lambda: set_blur("clear", blur_slider)
    ).pack(side="left", padx=3)

    tk.Button(
        blur_buttons,
        text="Medium",
        width=10,
        command=lambda: set_blur("medium", blur_slider)
    ).pack(side="left", padx=3)

    tk.Button(
        blur_buttons,
        text="Blurry",
        width=10,
        command=lambda: set_blur("blurry", blur_slider)
    ).pack(side="left", padx=3)

    tk.Label(
        root,
        text="2. Eye Strain",
        font=("Arial", 11, "bold")
    ).pack(pady=(20, 0))

    strain_status = tk.Label(
        root,
        text="Condition: Eyes feel relaxed",
        font=("Arial", 9)
    )
    strain_status.pack()

    def update_strain(value):

        value = int(float(value))

        if value <= 30:
            text = "Eyes feel relaxed"
        elif value <= 65:
            text = "Some eye fatigue"
        else:
            text = "High eye strain"

        strain_status.config(
            text="Condition: " + text
        )

    strain_slider = tk.Scale(
        root,
        from_=0,
        to=100,
        orient="horizontal",
        length=380,
        command=update_strain
    )

    strain_slider.set(10)
    strain_slider.pack()

    strain_buttons = tk.Frame(root)
    strain_buttons.pack(pady=5)

    tk.Button(
        strain_buttons,
        text="Relaxed",
        width=10,
        command=lambda: set_strain("relaxed", strain_slider)
    ).pack(side="left", padx=3)

    tk.Button(
        strain_buttons,
        text="Medium",
        width=10,
        command=lambda: set_strain("medium", strain_slider)
    ).pack(side="left", padx=3)

    tk.Button(
        strain_buttons,
        text="Tired",
        width=10,
        command=lambda: set_strain("tired", strain_slider)
    ).pack(side="left", padx=3)


    tk.Label(
        root,
        text="3. Distance From Screen",
        font=("Arial", 11, "bold")
    ).pack(pady=(20, 0))

    distance_status = tk.Label(
        root,
        text="Distance: Normal distance",
        font=("Arial", 9)
    )
    distance_status.pack()

    def update_distance(value):

        value = int(float(value))

        if value <= 30:
            text = "Too close"
        elif value <= 65:
            text = "Normal distance"
        else:
            text = "Quite far"

        distance_status.config(
            text="Distance: " + text
        )

    distance_slider = tk.Scale(
        root,
        from_=0,
        to=100,
        orient="horizontal",
        length=380,
        command=update_distance
    )

    distance_slider.set(50)
    distance_slider.pack()


    result_label = tk.Label(
        root,
        text="FUZZY TEST RESULT\n\n"
             "Move the sliders and click\n"
             "CHECK EYE CONDITION",
        font=("Arial", 11, "bold"),
        justify="center"
    )

    result_label.pack(pady=5)


    def evaluate_test():

        blur = blur_slider.get()
        strain = strain_slider.get()
        distance = distance_slider.get()

        result = check_eye_condition(
            blur,
            strain,
            distance
        )

        result_label.config(
            text=
            "FUZZY TEST RESULT\n\n"
            "Blur Level: " + str(blur) + "%\n"
            "Eye Strain: " + str(strain) + "%\n"
            "Screen Distance: " + str(distance) + " cm\n\n"
            "Overall Condition: " + result
        )

    tk.Button(
        root,
        text="CHECK EYE CONDITION",
        command=evaluate_test,
        font=("Arial", 11, "bold"),
        padx=20,
        pady=8
    ).pack(pady=25)

    return root