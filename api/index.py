from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INDEX_FILE = os.path.join(
    BASE_DIR,
    "public",
    "index.html"
)

CSS_FILE = os.path.join(
    BASE_DIR,
    "public",
    "style.css"
)


def crop_recommendation(soil, ph, temperature, rainfall):

    if soil == "Loamy" and 6.0 <= ph <= 7.5 and 20 <= temperature <= 32:
        return "Maize 🌽"

    if soil == "Clay" and 5.5 <= ph <= 7.0 and rainfall >= 600:
        return "Rice 🌾"

    if soil == "Sandy" and 6.0 <= ph <= 7.5 and temperature >= 25:
        return "Cotton 🌿"

    if 6.0 <= ph <= 7.5:
        return "Soybean 🌱"

    return "Please consult a local agricultural expert."


def irrigation_advice(moisture, rainfall):

    if rainfall >= 30:
        return "Irrigation is NOT recommended because sufficient rainfall is expected. 💧"

    if moisture < 30:
        return "Irrigation is REQUIRED because soil moisture is low. 💧"

    if moisture <= 60:
        return "Moderate moisture detected. Monitor the soil before irrigation. 💧"

    return "Irrigation is NOT required because soil moisture is sufficient. 💧"


def fertilizer_advice(nitrogen, phosphorus, potassium):

    advice = []

    if nitrogen < 40:
        advice.append("Nitrogen level is low.")

    if phosphorus < 30:
        advice.append("Phosphorus level is low.")

    if potassium < 30:
        advice.append("Potassium level is low.")

    if not advice:
        return "NPK values are within the selected range. Avoid unnecessary fertilizer application. 🌱"

    return " ".join(advice) + " Follow soil-test-based fertilizer recommendations."


def environmental_advice(moisture, rainfall):

    advice = []

    if moisture < 30 and rainfall < 30:
        advice.append("Use water carefully and irrigate only when required.")

    if rainfall >= 30:
        advice.append("Avoid unnecessary irrigation because rainfall is expected.")

    advice.append("Avoid excessive fertilizer application.")
    advice.append("Monitor soil moisture regularly.")
    advice.append("Follow sustainable farming practices.")

    return " ".join(advice)


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        if self.path == "/" or self.path == "/index.html":

            try:
                with open(INDEX_FILE, "r", encoding="utf-8") as file:
                    html = file.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))

            except Exception as e:

                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())

        elif self.path == "/style.css":

            try:
                with open(CSS_FILE, "r", encoding="utf-8") as file:
                    css = file.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/css")
                self.end_headers()
                self.wfile.write(css.encode("utf-8"))

            except Exception as e:

                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())

        else:

            self.send_response(404)
            self.end_headers()


    def do_POST(self):

        if self.path == "/analyze":

            length = int(self.headers.get("Content-Length", 0))

            data = self.rfile.read(length).decode("utf-8")

            form = urllib.parse.parse_qs(data)

            soil = form.get("soil_type", ["Loamy"])[0]

            ph = float(form.get("ph", [6.5])[0])

            moisture = float(form.get("moisture", [30])[0])

            temperature = float(form.get("temperature", [28])[0])

            rainfall = float(form.get("rainfall", [10])[0])

            nitrogen = float(form.get("nitrogen", [40])[0])

            phosphorus = float(form.get("phosphorus", [35])[0])

            potassium = float(form.get("potassium", [40])[0])


            result = {

                "crop": crop_recommendation(
                    soil,
                    ph,
                    temperature,
                    rainfall
                ),

                "irrigation": irrigation_advice(
                    moisture,
                    rainfall
                ),

                "fertilizer": fertilizer_advice(
                    nitrogen,
                    phosphorus,
                    potassium
                ),

                "environmental": environmental_advice(
                    moisture,
                    rainfall
                )

            }


            response = json.dumps(result)

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8"
            )

            self.end_headers()

            self.wfile.write(response.encode("utf-8"))

        else:

            self.send_response(404)
            self.end_headers()
