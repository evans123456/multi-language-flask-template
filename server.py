from flask import Flask, render_template, request, redirect, url_for
import json
import os
import requests

app = Flask(__name__)

# Config
with open("config.json") as f:
    CONFIG = json.load(f)

THEME = CONFIG["theme"]
CLASS = CONFIG["default_class"]

SUPPORTED_LOCALES = ["en", "fr", "es", "de"]
VALID_PAGES = {"landing", "registered", "logout"}

API_BASE = "http://django_api:8000"

# Per-page API logic
API_CONFIG = {
    "landing": {"endpoint": "/api/portal/landing-data/", "method": "GET"},
    "registered": {"endpoint": "/api/user/verify-registration/", "method": "GET"},
    "logout": {"endpoint": "/api/session/end/", "method": "POST"}
}

def load_translations(locale):
    path = f"templates/{THEME}/{CLASS}/translations/translations.json"
    with open(path) as f:
        data = json.load(f)
    return data.get(locale, data.get("en"))

def call_api(page):
    config = API_CONFIG.get(page)
    if not config:
        return {"error": "API config missing"}

    url = f"{API_BASE}{config['endpoint']}"
    method = config["method"]

    try:
        if method == "GET":
            res = requests.get(url)
        elif method == "POST":
            res = requests.post(url, json={"user": "guest"})  # Example payload
        else:
            return {"error": f"Unsupported method: {method}"}

        return res.json() if res.status_code == 200 else {"error": f"API error: {res.status_code}"}
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    locale = request.accept_languages.best_match(SUPPORTED_LOCALES) or "en"
    return redirect(url_for("localized_page", page="landing", locale=locale))

@app.route("/<page>/")
def default_locale_page(page):
    if page not in VALID_PAGES:
        return "Page not found", 404
    locale = request.accept_languages.best_match(SUPPORTED_LOCALES) or "en"
    return redirect(url_for("localized_page", page=page, locale=locale))

@app.route("/<page>/<locale>/")
def localized_page(page, locale):
    if page not in VALID_PAGES:
        return "Page not found", 404
    if locale not in SUPPORTED_LOCALES:
        return "Locale not supported", 404

    translations = load_translations(locale)
    api_data = call_api(page)

    try:
        return render_template(
            f"{THEME}/{CLASS}/{page}.html",
            t=translations,
            locale=locale,
            api_data=api_data
        )
    except:
        return f"Template for page '{page}' not found.", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5009, debug=True)
