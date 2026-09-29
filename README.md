# AI Website Cloner

An AI-powered website cloning application that analyzes existing websites and generates responsive React websites using artificial intelligence.

The application uses React and TypeScript for the frontend, Python and Flask for the backend, and Google's Gemini API for AI-powered website generation. It also includes a fallback generator for situations when the AI service is unavailable.

## Features

- **Website Analysis:** Accepts a publicly accessible website URL and extracts information such as the title, description, headings, links, images, and basic styles.
- **AI Website Generation:** Uses Google's Gemini API to generate React and CSS code based on the analyzed website.
- **Responsive Design:** Generates websites designed to work on mobile phones, tablets, and desktop screens.
- **Website Modification:** Allows users to modify generated websites using natural-language instructions.
- **Fallback Generation:** Generates a basic React website when the Gemini API is unavailable or its request fails.
- **Build Validation:** Uses TypeScript and Vite to check generated websites for build errors.
- **Local Preview:** Allows users to preview generated websites locally.

## Technologies Used

### Frontend
- React
- TypeScript
- Vite
- CSS
- HTML

### Backend
- Python
- Flask
- Flask-CORS
- Playwright

### AI
- Google Gemini API
- Google Gen AI SDK

### Development Tools
- Visual Studio Code
- Git
- GitHub
- Node.js
- npm

## Project Architecture

The application follows a frontend-backend architecture.

1. The user enters a publicly accessible website URL.
2. The React frontend sends the URL to the Flask backend.
3. The website analyzer extracts information from the original website.
4. The backend sends the extracted information to Gemini.
5. Gemini generates React and CSS code.
6. If Gemini is unavailable, the fallback generator creates a basic website.
7. The website saver writes the generated files to the project.
8. The generated project is validated using a production build.
9. The user can preview and modify the generated website.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the architecture diagram.

## Project Structure

```text
AI-Website-Cloner/
│
├── backend/
│   ├── app.py
│   ├── analyzer.py
│   ├── generator.py
│   ├── saver.py
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── generated_sites/
│   └── website_1/
│       ├── src/
│       │   ├── App.tsx
│       │   ├── App.css
│       │   └── main.tsx
│       ├── index.html
│       ├── package.json
│       ├── tsconfig.json
│       └── vite.config.ts
│
├── .gitignore
├── README.md
└── ARCHITECTURE.md
```

## Requirements

Make sure the following tools are installed:

- Python 3.10 or later
- Node.js and npm
- Git
- Visual Studio Code
- A Google Gemini API key

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Website-Cloner.git
```

Navigate to the project directory:

```bash
cd AI-Website-Cloner
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Configure the Gemini API Key

Create a file named `.env` inside the `backend` directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your actual API key.

Keep your API key private. Never upload your `.env` file to GitHub.

### 4. Start the Backend

From the `backend` directory, run:

```bash
python app.py
```

The Flask backend should start at:

```text
http://127.0.0.1:5000
```

### 5. Set Up the Frontend

Open a second terminal.

Navigate to the frontend directory:

```bash
cd E:\AI-Website-Cloner\frontend
```

Install the frontend dependencies:

```bash
npm install
```

Start the frontend development server:

```bash
npm run dev
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:5173
```

### 6. Generate a Website

1. Open the AI Website Cloner in your browser.
2. Enter a publicly accessible website URL.
3. Click **Analyze Website**.
4. Review the extracted website information.
5. Click **Generate Website**.
6. Wait for the generated website to be saved and validated.
7. Preview the generated website.
8. Enter a natural-language instruction to modify the website.

## Generated Website Preview

The generated website is saved in:

```text
generated_sites/website_1/
```

To run the generated website separately, open another terminal:

```powershell
cd E:\AI-Website-Cloner\generated_sites\website_1
```

Install dependencies if necessary:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The generated website is configured to use:

```text
http://127.0.0.1:5174
```

## Fallback Generation

The application includes a fallback generator for situations where Gemini cannot generate a website.

The fallback generator uses the analyzed website's title, description, and headings to create a basic responsive React page.

This allows the application to demonstrate basic website generation even when the AI service is unavailable.

The fallback does not reproduce the original website's complete layout, styling, or functionality.

## Error Handling and Validation

The application includes basic error handling for:

- Invalid or missing website information
- Empty or invalid AI responses
- Gemini API errors and rate limits
- Missing generated React or CSS code
- Dependency installation failures
- Generated website build errors
- Build validation timeouts

The generated website is checked using a production build before being reported as successfully validated.

## Limitations

- Website analysis depends on the accessibility and structure of the original website.
- Some websites may block automated browsing or require authentication.
- Complex websites with dynamic content may not be fully analyzed.
- AI-generated websites may differ from the original design.
- The fallback generator creates a basic website rather than a complete visual recreation.
- Gemini API usage is subject to rate limits and availability.
- Generated websites may require additional manual adjustments.
- The application currently saves the generated website to a local project folder.

## Future Improvements

- Improve website layout and visual recreation.
- Support more complex website structures.
- Improve image and asset extraction.
- Add more reusable React components.
- Improve responsive layout generation.
- Enhance error recovery and generated-code validation.
- Support multiple generated websites.
- Improve the natural-language modification workflow.

## Author

**Mithra M**

B.Sc. Information Technology  
Sri Krishna Arts and Science College  
Coimbatore, Tamil Nadu, India

## Project Purpose

This project was developed as part of an internship assignment to explore AI-assisted frontend development, website analysis, code generation, responsive design, and natural-language website modification.
