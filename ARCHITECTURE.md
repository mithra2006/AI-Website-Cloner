# AI Website Cloner - Architecture

```mermaid
flowchart TD
    A[User enters website URL] --> B[React Frontend]
    B --> C[Flask Backend]
    C --> D[Website Analyzer]
    D --> E[Extract website content and styles]
    E --> F[Gemini AI Generator]

    F -->|Generation successful| G[Generated React and CSS]
    F -->|API error or quota exceeded| H[Fallback Generator]

    H --> G
    G --> I[Website Saver]
    I --> J[Install Dependencies]
    J --> K[Build Validation]

    K -->|Build successful| L[Generated Website]
    K -->|Build failed| M[Return Error]

    L --> N[Local Website Preview]
    N --> O[User requests modification]
    O --> C
    M --> B
    
## Step 2: Save the file

Press **Ctrl + S**.

Your diagram represents the main workflow:

1. The user enters a website URL.
2. Flask analyzes the website.
3. Gemini generates the React code, or the fallback generator creates a basic website if Gemini fails.
4. The saver writes the generated files and validates the build.
5. The user previews and modifies the generated website.

**Note:** The diagram assumes your current Flask routes connect these components as described. We can adjust it if your implementation differs.

## Step 3: Check your project

Your project should now include:

```text
AI-Website-Cloner/
│
├── backend/
│   ├── app.py
│   ├── analyzer.py
│   ├── generator.py
│   ├── saver.py
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── App.tsx
│       ├── App.css
│       └── main.tsx
│
├── generated_sites/
│   └── website_1/
│
├── .gitignore
├── README.md
└── ARCHITECTURE.md