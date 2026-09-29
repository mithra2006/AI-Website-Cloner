from flask import Flask, jsonify, request
from flask_cors import CORS
from urllib.parse import urlparse
import os

from analyzer import analyze_website
from generator import generate_website, modify_website
from saver import save_website

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GENERATED_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "generated_sites", "website_1", "src")
)


def error_response(message, status_code=400):
    return jsonify({
        "success": False,
        "error": message
    }), status_code


def validate_url(url):
    if not isinstance(url, str) or not url.strip():
        return None

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or "." not in parsed.hostname
    ):
        return None

    return url


def get_request_data():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return None

    return data


@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "AI Website Cloner is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "success": True,
        "message": "Backend is working"
    })


# Analyze website
@app.route("/analyze", methods=["POST"])
def analyze():
    data = get_request_data()

    if data is None:
        return error_response("Please send valid JSON data.")

    url = validate_url(data.get("url"))

    if not url:
        return error_response("Please enter a valid website URL.")

    try:
        result = analyze_website(url)

        if not isinstance(result, dict):
            return error_response(
                "The website analyzer returned an invalid response.",
                500
            )

        if not result.get("success"):
            return error_response(
                result.get("error", "Website analysis failed."),
                500
            )

        return jsonify(result)

    except Exception:
        app.logger.exception("Website analysis failed")
        return error_response(
            "Unable to analyze this website. Please check the URL and try again.",
            500
        )


# Generate website
@app.route("/generate", methods=["POST"])
def generate():
    data = get_request_data()

    if data is None:
        return error_response("Please send valid JSON data.")

    website_data = data.get("website_data")

    if not isinstance(website_data, dict):
        return error_response(
            "Website analysis data is required. Analyze a website first."
        )

    try:
        result = generate_website(website_data)

        if not isinstance(result, dict) or not result.get("success"):
            message = (
                result.get("error", "Website generation failed.")
                if isinstance(result, dict)
                else "The generator returned an invalid response."
            )

            status = 429 if "429" in message or "rate limit" in message.lower() else 500
            return error_response(message, status)

        app_tsx = result.get("app_tsx")
        app_css = result.get("app_css")

        if not isinstance(app_tsx, str) or not isinstance(app_css, str):
            return error_response(
                "The generator did not return valid React and CSS files.",
                500
            )

        saved = save_website(app_tsx, app_css)

        if isinstance(saved, dict):
            if not saved.get("success"):
                return error_response(
                    saved.get("error", "Could not save the generated website."),
                    500
                )
            path = saved.get("path")
        else:
            path = saved

        return jsonify({
            "success": True,
            "message": "Website generated successfully!",
            "path": path
        })

    except Exception:
        app.logger.exception("Website generation failed")
        return error_response(
            "An unexpected error occurred during website generation.",
            500
        )


# Modify generated website
@app.route("/modify", methods=["POST"])
def modify():
    data = get_request_data()

    if data is None:
        return error_response("Please send valid JSON data.")

    prompt = data.get("prompt")

    if not isinstance(prompt, str) or not prompt.strip():
        return error_response("Please enter a modification instruction.")

    app_tsx_path = os.path.join(GENERATED_DIR, "App.tsx")
    app_css_path = os.path.join(GENERATED_DIR, "App.css")

    if not os.path.isfile(app_tsx_path) or not os.path.isfile(app_css_path):
        return error_response(
            "Generate a website before modifying it.",
            400
        )

    try:
        with open(app_tsx_path, "r", encoding="utf-8") as file:
            current_tsx = file.read()

        with open(app_css_path, "r", encoding="utf-8") as file:
            current_css = file.read()

        result = modify_website(
            prompt.strip(),
            current_tsx,
            current_css
        )

        if not isinstance(result, dict) or not result.get("success"):
            message = (
                result.get("error", "Website modification failed.")
                if isinstance(result, dict)
                else "The modifier returned an invalid response."
            )

            status = 429 if "429" in message or "rate limit" in message.lower() else 500
            return error_response(message, status)

        app_tsx = result.get("app_tsx")
        app_css = result.get("app_css")

        if not isinstance(app_tsx, str) or not isinstance(app_css, str):
            return error_response(
                "The modifier did not return valid React and CSS files.",
                500
            )

        saved = save_website(app_tsx, app_css)

        if isinstance(saved, dict):
            if not saved.get("success"):
                return error_response(
                    saved.get("error", "Could not save the modified website."),
                    500
                )
            path = saved.get("path")
        else:
            path = saved

        return jsonify({
            "success": True,
            "message": "Website modified successfully!",
            "path": path
        })

    except Exception:
        app.logger.exception("Website modification failed")
        return error_response(
            "An unexpected error occurred during website modification.",
            500
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)