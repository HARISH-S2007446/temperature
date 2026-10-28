from flask import Flask, render_template_string, request
import os

app = Flask(__name__)


def c_to_f(celsius):
    return (celsius * 9 / 5) + 32


@app.route("/")
def index():
    return render_template_string("""
    <html>
      <body>
        <h1>Temperature Converter</h1>
        <ul>
          <li><a href="/celsius-to-fahrenheit">Celsius to Fahrenheit</a></li>
        </ul>
      </body>
    </html>
    """)


@app.route("/celsius-to-fahrenheit", methods=["GET", "POST"])
def celsius_to_fahrenheit():
    result = None
    if request.method == "POST":
        celsius = float(request.form["celsius"])
        result = c_to_f(celsius)

    return render_template_string("""
    <html>
      <body>
        <h1>Celsius to Fahrenheit</h1>
        <form method="post">
          <label>Temperature in Celsius:
            <input type="number" step="any" name="celsius" required>
          </label>
          <button type="submit">Convert</button>
        </form>
        {% if result is not none %}
          <p><strong>Result:</strong> {{ result }}°F</p>
        {% endif %}
        <p><a href="/">Back to menu</a></p>
      </body>
    </html>
    """, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
