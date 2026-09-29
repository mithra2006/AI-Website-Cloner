import os
import json
import re
import html

from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

load_dotenv(
    os.path.join(os.path.dirname(__file__), ".env")
)

MODEL_NAME = "gemini-3.8-flash"

api_key = os.getenv("GEMINI_API_KEY")

client = None

if api_key:
    client = genai.Client(api_key=api_key)


# --------------------------------------------------
# GEMINI API
# --------------------------------------------------

def call_gemini(prompt):
    """
    Send a prompt to Gemini and return its response.
    """

    if client is None:
        raise ValueError(
            "GEMINI_API_KEY is missing from backend/.env"
        )

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt
    )

    return interaction.output_text


# --------------------------------------------------
# JSON EXTRACTION
# --------------------------------------------------

def extract_json(response):
    """
    Extract JSON from Gemini's response.
    Handles responses with or without Markdown fences.
    """

    if not isinstance(response, str) or not response.strip():
        raise ValueError("Gemini returned an empty response.")

    response = response.strip()

    # Remove Markdown code fences
    response = re.sub(
        r"^\s*```(?:json)?\s*",
        "",
        response,
        flags=re.IGNORECASE
    )

    response = re.sub(
        r"\s*```\s*$",
        "",
        response
    )

    # Find the JSON object
    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1 or end < start:
        raise ValueError(
            "Gemini did not return a valid JSON object."
        )

    json_text = response[start:end + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON returned by Gemini: {error}"
        )


# --------------------------------------------------
# FALLBACK WEBSITE GENERATOR
# --------------------------------------------------

def generate_fallback_website(website_data):
    """
    Generate a basic responsive website without Gemini.

    This allows the application to continue working
    when Gemini is unavailable or its quota is exhausted.
    """

    if not isinstance(website_data, dict):
        website_data = {}

    # Extract website information safely
    title = html.escape(
        str(website_data.get("title") or "Generated Website")
    )

    description = html.escape(
        str(
            website_data.get("description")
            or "Welcome to our website."
        )
    )

    headings = website_data.get("headings", [])

    if not isinstance(headings, list):
        headings = []

    # Generate heading elements
    heading_elements = "\n".join(
        f"<h2>{html.escape(str(heading))}</h2>"
        for heading in headings
        if isinstance(heading, str) and heading.strip()
    )

    if not heading_elements:
        heading_elements = "<p>Explore our website.</p>"

    # React component
    app_tsx = f'''import "./App.css";

function App() {{
  return (
    <main className="website">
      <header className="hero">
        <h1>{title}</h1>
        <p>{description}</p>
      </header>

      <section className="content">
        {heading_elements}
      </section>

      <footer>
        <p>Generated with AI Website Cloner</p>
      </footer>
    </main>
  );
}}

export default App;
'''

    # Responsive CSS
    app_css = """
* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
  color: #222;
  background: #f5f5f5;
}

.website {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.hero {
  padding: 80px 20px;
  text-align: center;
  background: #2563eb;
  color: white;
}

.hero h1 {
  font-size: clamp(2rem, 5vw, 3.5rem);
  margin: 0 0 20px;
  overflow-wrap: anywhere;
}

.hero p {
  max-width: 650px;
  margin: 0 auto;
  line-height: 1.6;
  overflow-wrap: anywhere;
}

.content {
  width: min(100% - 32px, 1000px);
  margin: 40px auto;
  padding: 24px;
  background: white;
  border-radius: 12px;
  flex: 1;
}

.content h2 {
  margin: 20px 0;
  overflow-wrap: anywhere;
}

footer {
  padding: 20px;
  text-align: center;
  background: #222;
  color: white;
}

@media (max-width: 600px) {
  .hero {
    padding: 50px 16px;
  }

  .content {
    width: calc(100% - 24px);
    margin: 20px auto;
    padding: 18px;
  }
}
"""

    return {
        "success": True,
        "app_tsx": app_tsx,
        "app_css": app_css,
        "fallback": True,
        "message": (
            "A basic website was generated using fallback mode. "
            "Gemini was not used."
        )
    }


# --------------------------------------------------
# AI WEBSITE GENERATION
# --------------------------------------------------

def generate_website(website_data):
    """
    Generate a website using Gemini.

    If Gemini fails, use the fallback generator.
    """

    if not isinstance(website_data, dict):
        return {
            "success": False,
            "error": "Website data must be a JSON object."
        }

    prompt = f"""
You are an expert frontend developer.

Create a complete, responsive React website using
TypeScript and CSS.

Recreate the supplied website using its layout, text,
images, colors, typography, and design information.

Website data:
{json.dumps(website_data, indent=2)}

Requirements:

- Create a complete React App.tsx file using TypeScript.
- Create a complete App.css file.
- Use reusable React components where appropriate.
- Use a mobile-first responsive design.
- Support mobile phones, tablets, laptops, and desktops.
- Use CSS Flexbox and Grid where appropriate.
- Avoid fixed widths that cause horizontal scrolling.
- Make images responsive using max-width: 100%.
- Ensure navigation works on small screens.
- Use CSS media queries for different screen sizes.
- Make buttons and links easy to tap on mobile.
- Ensure text remains readable on small screens.
- Preserve the original website's layout, colors,
  and typography as closely as possible.
- Use the provided text and image URLs where possible.
- Do not use external UI libraries.
- Do not invent unnecessary website sections.
- Use semantic HTML elements.
- Ensure the React code is valid and complete.

Return ONLY a valid JSON object with these keys:

{{
  "app_tsx": "complete App.tsx code",
  "app_css": "complete App.css code"
}}

Do not include Markdown code fences.
"""

    try:
        response = call_gemini(prompt)
        result = extract_json(response)

        app_tsx = result.get("app_tsx")
        app_css = result.get("app_css")

        if not isinstance(app_tsx, str) or not app_tsx.strip():
            raise ValueError(
                "Gemini did not return valid App.tsx code."
            )

        if not isinstance(app_css, str) or not app_css.strip():
            raise ValueError(
                "Gemini did not return valid App.css code."
            )

        return {
            "success": True,
            "app_tsx": app_tsx,
            "app_css": app_css,
            "fallback": False
        }

    except Exception as error:
        print("Website generation error:", str(error))

        # Try fallback generation
        fallback = generate_fallback_website(website_data)

        fallback["ai_error"] = str(error)

        return fallback


# --------------------------------------------------
# AI WEBSITE MODIFICATION
# --------------------------------------------------

def modify_website(prompt, app_tsx, app_css):
    """
    Modify an existing website using Gemini.

    If Gemini fails, return an error rather than
    replacing the user's existing website with a
    generic fallback.
    """

    if not isinstance(prompt, str) or not prompt.strip():
        return {
            "success": False,
            "error": "Please enter a modification instruction."
        }

    if not isinstance(app_tsx, str) or not app_tsx.strip():
        return {
            "success": False,
            "error": "Existing App.tsx code is missing."
        }

    if not isinstance(app_css, str) or not app_css.strip():
        return {
            "success": False,
            "error": "Existing App.css code is missing."
        }

    request = f"""
You are an expert React developer.

Modify the existing website according to this instruction:

{prompt}

Current App.tsx:
{app_tsx}

Current App.css:
{app_css}

Requirements:

- Preserve existing website functionality.
- Keep the design responsive on mobile, tablet,
  and desktop.
- Do not remove existing components unless requested.
- Do not remove existing content unless requested.
- Use clean and readable React and CSS.
- Avoid unnecessary changes to unrelated sections.
- Ensure images and layouts remain responsive.
- Use CSS media queries where appropriate.
- Ensure the updated React and CSS code is valid.
- Return the complete updated App.tsx and App.css files.

Return ONLY a valid JSON object with these keys:

{{
  "app_tsx": "complete updated App.tsx code",
  "app_css": "complete updated App.css code"
}}

Do not include Markdown code fences.
"""

    try:
        response = call_gemini(request)
        result = extract_json(response)

        updated_app_tsx = result.get("app_tsx")
        updated_app_css = result.get("app_css")

        if (
            not isinstance(updated_app_tsx, str)
            or not updated_app_tsx.strip()
        ):
            raise ValueError(
                "Gemini did not return valid updated App.tsx."
            )

        if (
            not isinstance(updated_app_css, str)
            or not updated_app_css.strip()
        ):
            raise ValueError(
                "Gemini did not return valid updated App.css."
            )

        return {
            "success": True,
            "app_tsx": updated_app_tsx,
            "app_css": updated_app_css,
            "fallback": False
        }

    except Exception as error:
        print("Website modification error:", str(error))

        return {
            "success": False,
            "error": str(error)
        }