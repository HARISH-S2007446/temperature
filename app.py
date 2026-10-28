from flask import Flask, request, render_template_string
app = Flask(__name__)
def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32
MENU_HTML = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Temperature Converter</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f7fa; }
        .card { max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        input, select, button { width: 100%; margin-top: 10px; padding: 10px; font-size: 16px; }
        h1 { text-align: center; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Temperature Converter</h1>
        <form action="/convert" method="post">
            <label for="conversion">Select conversion:</label>
            <select id="conversion" name="conversion">
                <option value="c_to_f">Celsius to Fahrenheit</option>
            </select>
            <input type="number" step="any" name="value" placeholder="Enter temperature value" required>
            <button type="submit">Convert</button>
        </form>
    </div>
</body>
</html>
"""
@app.route("/")
def index():
    return MENU_HTML
@app.route("/convert", methods=["POST"])
def convert():
    temperature = float(request.form["value"])
    conversion = request.form["conversion"]

    if conversion == "c_to_f":
        result = celsius_to_fahrenheit(temperature)
        output = f"{temperature}°C = {result:.2f}°F"
    else:
        output = "Unsupported conversion"

    return render_template_string("""
        <!doctype html>
        <html>
            <head><title>Conversion Result</title></head>
            <body>
                <h2>Result</h2>
                <p>{{ output }}</p>
                <a href="/">Return to menu</a>
            </body>
        </html>
    """, output=output)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)