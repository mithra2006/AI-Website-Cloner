import os
import json
import subprocess
import shutil
import sys


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GENERATED_DIR = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "generated_sites",
        "website_1"
    )
)


# --------------------------------------------------
# NPM COMMAND
# --------------------------------------------------

def run_npm_command(arguments, timeout=180):
    """
    Run npm commands on Windows and other platforms.
    Windows requires special handling for npm.cmd.
    """

    if os.name == "nt":
        npm_path = shutil.which("npm.cmd")

        if not npm_path:
            npm_path = shutil.which("npm")

        if not npm_path:
            raise FileNotFoundError(
                "npm was not found. Please install Node.js "
                "and restart VS Code."
            )

        command = subprocess.list2cmdline(
            [npm_path] + arguments
        )

        return subprocess.run(
            command,
            cwd=GENERATED_DIR,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=True
        )

    npm_path = shutil.which("npm")

    if not npm_path:
        raise FileNotFoundError(
            "npm was not found. Please install Node.js."
        )

    return subprocess.run(
        [npm_path] + arguments,
        cwd=GENERATED_DIR,
        capture_output=True,
        text=True,
        timeout=timeout
    )


# --------------------------------------------------
# SAVE WEBSITE
# --------------------------------------------------

def save_website(app_tsx, app_css):
    """
    Save generated React files and validate the project
    by installing dependencies when necessary and running
    a production build.
    """

    try:
        # Validate generated code
        if not isinstance(app_tsx, str) or not app_tsx.strip():
            return {
                "success": False,
                "error": "App.tsx code is empty or invalid."
            }

        if not isinstance(app_css, str) or not app_css.strip():
            return {
                "success": False,
                "error": "App.css code is empty or invalid."
            }

        # Create project folders
        src_dir = os.path.join(GENERATED_DIR, "src")
        os.makedirs(src_dir, exist_ok=True)

        os.makedirs(GENERATED_DIR, exist_ok=True)

        # --------------------------------------------------
        # MAIN.TSX
        # --------------------------------------------------

        main_tsx = """
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

ReactDOM.createRoot(
    document.getElementById("root")!
).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
"""

        # --------------------------------------------------
        # INDEX.HTML
        # --------------------------------------------------

        index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >
    <title>Generated Website</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
</body>
</html>
"""

        # --------------------------------------------------
        # PACKAGE.JSON
        # --------------------------------------------------

        package = {
            "name": "generated-website",
            "version": "1.0.0",
            "private": True,
            "type": "module",
            "scripts": {
                "dev": "vite --host 127.0.0.1",
                "build": "tsc -b && vite build"
            },
            "dependencies": {
                "react": "^19.0.0",
                "react-dom": "^19.0.0"
            },
            "devDependencies": {
                "@types/react": "^19.0.0",
                "@types/react-dom": "^19.0.0",
                "@vitejs/plugin-react": "^4.3.0",
                "typescript": "~5.7.0",
                "vite": "^6.0.0"
            }
        }

        # --------------------------------------------------
        # VITE CONFIGURATION
        # --------------------------------------------------

        vite_config = """
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],
    server: {
        host: "127.0.0.1",
        port: 5174,
        strictPort: true
    }
});
"""

        # --------------------------------------------------
        # TYPESCRIPT CONFIGURATION
        # --------------------------------------------------

        tsconfig = {
            "compilerOptions": {
                "target": "ES2020",
                "useDefineForClassFields": True,
                "lib": [
                    "ES2020",
                    "DOM",
                    "DOM.Iterable"
                ],
                "module": "ESNext",
                "skipLibCheck": True,
                "moduleResolution": "Bundler",
                "allowImportingTsExtensions": True,
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx",
                "strict": False
            },
            "include": ["src"]
        }

        # --------------------------------------------------
        # FILES TO SAVE
        # --------------------------------------------------

        files = {
            os.path.join(src_dir, "App.tsx"): app_tsx,
            os.path.join(src_dir, "App.css"): app_css,
            os.path.join(src_dir, "main.tsx"): main_tsx,
            os.path.join(GENERATED_DIR, "index.html"): index_html,
            os.path.join(GENERATED_DIR, "package.json"):
                json.dumps(package, indent=2),
            os.path.join(GENERATED_DIR, "vite.config.ts"):
                vite_config,
            os.path.join(GENERATED_DIR, "tsconfig.json"):
                json.dumps(tsconfig, indent=2)
        }

        # --------------------------------------------------
        # WRITE FILES
        # --------------------------------------------------

        for path, content in files.items():
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)

        # --------------------------------------------------
        # INSTALL DEPENDENCIES
        # --------------------------------------------------

        node_modules = os.path.join(
            GENERATED_DIR,
            "node_modules"
        )

        if not os.path.isdir(node_modules):
            print("Installing npm dependencies...")

            install = run_npm_command(
                ["install", "--no-audit", "--no-fund"]
            )

            if install.returncode != 0:
                return {
                    "success": False,
                    "error": (
                        "Dependency installation failed:\n"
                        + install.stdout[-2000:]
                        + install.stderr[-2000:]
                    )
                }

        # --------------------------------------------------
        # BUILD VALIDATION
        # --------------------------------------------------

        print("Validating generated React website...")

        build = run_npm_command(
            ["run", "build"]
        )

        if build.returncode != 0:
            return {
                "success": False,
                "error": (
                    "Generated website has build errors:\n"
                    + build.stdout[-2000:]
                    + build.stderr[-2000:]
                )
            }

        # --------------------------------------------------
        # SUCCESS
        # --------------------------------------------------

        return {
            "success": True,
            "path": GENERATED_DIR,
            "message": (
                "Website saved and build validation passed."
            )
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": (
                "Website validation timed out. "
                "Please try again."
            )
        }

    except FileNotFoundError as error:
        return {
            "success": False,
            "error": str(error)
        }

    except Exception as error:
        print("Website saving error:", str(error))

        return {
            "success": False,
            "error": str(error)
        }