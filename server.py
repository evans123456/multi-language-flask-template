from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import json
import os
import requests
import logging

app = Flask(__name__, static_folder=None)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

with open("config.json") as f:
    CONFIG = json.load(f)

THEME = CONFIG["theme"]
CLASS = CONFIG["default_class"]

SUPPORTED_LOCALES = ["en", "fr", "es", "de"]
API_BASE = "http://django_api:8000"

def load_translations(locale):
    path = f"templates/{THEME}/{CLASS}/translations/translations.json"
    with open(path) as f:
        data = json.load(f)
    return data.get(locale, data.get("en"))

@app.route("/")
def index():
    # Redirect to /landing with preferred locale
    locale = request.accept_languages.best_match(SUPPORTED_LOCALES) or "en"
    return redirect(url_for("landing", locale=locale))

@app.route('/static/<path:filename>')
def static_files(filename):
    logger.debug(f"Looking for: templates/{THEME}/static/{filename}")
    return send_from_directory(f'templates/{THEME}/static', filename)



@app.route("/landing/<locale>/")
def landing(locale):
    if locale not in SUPPORTED_LOCALES:
        return "Locale not supported", 404

    translations = load_translations(locale)
    try:
        res = requests.get(f"{API_BASE}/api/portal/landing-data/")
        api_data = res.json()
    except Exception as e:
        api_data = {"error": str(e)}

    return render_template(
        f"{THEME}/{CLASS}/landing.html",
        t=translations,
        locale=locale,
        api_data=api_data
    )

@app.route("/registered/<locale>/")
def registered(locale):
    if locale not in SUPPORTED_LOCALES:
        return "Locale not supported", 404

    translations = load_translations(locale)
    try:
        res = requests.get(f"{API_BASE}/api/user/verify-registration/")
        api_data = res.json()
    except Exception as e:
        api_data = {"error": str(e)}

    return render_template(
        f"{THEME}/{CLASS}/registered.html",
        t=translations,
        locale=locale,
        api_data=api_data
    )

@app.route("/logout/<locale>/")
def logout(locale):
    if locale not in SUPPORTED_LOCALES:
        return "Locale not supported", 404

    translations = load_translations(locale)
    try:
        res = requests.post(f"{API_BASE}/api/session/end/", json={"user": "guest"})
        api_data = res.json()
    except Exception as e:
        api_data = {"error": str(e)}

    return render_template(
        f"{THEME}/{CLASS}/logout.html",
        t=translations,
        locale=locale,
        api_data=api_data
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5009, debug=True)
