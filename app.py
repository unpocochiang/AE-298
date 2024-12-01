from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    # Get inputs from the form
    wing_area = float(request.form["wing_area"])
    drag_coefficient_0 = float(request.form["drag_coefficient_0"])
    aspect_ratio = float(request.form["aspect_ratio"])
    efficiency_factor = float(request.form["efficiency_factor"])

    # Calculate drag coefficient over a range of Mach numbers
    mach_numbers = np.linspace(0.1, 1.0, 100)
    drag_coefficients = drag_coefficient_0 + (1 / (np.pi * aspect_ratio * efficiency_factor)) * mach_numbers ** 2

    # Generate an interactive plot
    fig, ax = plt.subplots()
    ax.plot(mach_numbers, drag_coefficients)
    ax.set_title("Drag Coefficient vs. Mach Number")
    ax.set_xlabel("Mach Number")
    ax.set_ylabel("Drag Coefficient")
    ax.grid()

    # Save the plot to a string
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()

    return render_template("result.html", plot_url=f"data:image/png;base64,{plot_data}")

if __name__ == "__main__":
    app.run(debug=True)
