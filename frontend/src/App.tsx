import { useState } from "react";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [generating, setGenerating] = useState(false);
  const [generationMessage, setGenerationMessage] = useState("");
  const [previewUrl, setPreviewUrl] = useState("");
  const [modification, setModification] = useState("");
  const [modifying, setModifying] = useState(false);

  // Analyze website
  async function analyzeWebsite() {
    if (!url.trim()) {
      setError("Please enter a website URL.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setGenerationMessage("");
    setPreviewUrl("");

    try {
      const response = await fetch("http://localhost:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || "Analysis failed");
      }

      setResult(data.data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  }

  // Generate website
  async function generateWebsite() {
    if (!result) {
      setGenerationMessage("Analyze a website first.");
      return;
    }

    setGenerating(true);
    setGenerationMessage("");
    setError("");
    setPreviewUrl("");

    try {
      const response = await fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          website_data: result,
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || "Website generation failed");
      }

      setGenerationMessage(
        data.message || "Website generated successfully!"
      );

      setPreviewUrl("http://localhost:5174/");
    } catch (err) {
      setGenerationMessage(
        err instanceof Error ? err.message : "Generation failed"
      );
    } finally {
      setGenerating(false);
    }
  }

  // Modify website using Gemini
  async function modifyWebsite() {
    if (!modification.trim()) {
      setGenerationMessage("Please enter a modification instruction.");
      return;
    }

    if (!previewUrl) {
      setGenerationMessage("Generate a website before modifying it.");
      return;
    }

    setModifying(true);
    setGenerationMessage("");

    try {
      const response = await fetch("http://localhost:5000/modify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: modification,
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || "Modification failed");
      }

      setGenerationMessage(
        data.message || "Website modified successfully!"
      );

      // Refresh the preview after modification
      setPreviewUrl(
        `http://localhost:5174/?refresh=${Date.now()}`
      );

      setModification("");
    } catch (err) {
      setGenerationMessage(
        err instanceof Error ? err.message : "Modification failed"
      );
    } finally {
      setModifying(false);
    }
  }

  return (
    <div className="container">
      <h1>AI Website Cloner</h1>

      <p>
        Analyze a publicly accessible website and generate
        a React version of its design.
      </p>

      {/* Website URL input */}
      <div className="input-area">
        <input
          type="url"
          placeholder="Enter website URL (e.g. https://example.com)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button
          onClick={analyzeWebsite}
          disabled={!url.trim() || loading || generating}
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {/* Analysis error */}
      {error && <p className="error">{error}</p>}

      {/* Analysis results */}
      {result && (
        <div className="results">
          <h2>{result.title || "Website Analysis"}</h2>

          <p>
            <strong>Description:</strong>{" "}
            {result.description || "Not available"}
          </p>

          {/* Generate button */}
          <div className="generate-area">
            <button
              onClick={generateWebsite}
              disabled={generating || loading || modifying}
            >
              {generating ? "Generating Website..." : "Generate Website"}
            </button>

            {generationMessage && (
              <p className="generation-message">
                {generationMessage}
              </p>
            )}
          </div>

          {/* Website preview */}
          {previewUrl && (
            <div className="preview-area">
              <h2>Generated Website Preview</h2>

              <iframe
                src={previewUrl}
                title="Generated Website Preview"
                className="preview-frame"
              />
            </div>
          )}

          {/* Website modification */}
          {previewUrl && (
            <div className="modification-area">
              <h2>Modify Your Website</h2>

              <p>
                Describe the changes you want Gemini to make.
              </p>

              <textarea
                placeholder="Example: Change the background to light blue..."
                value={modification}
                onChange={(e) => setModification(e.target.value)}
                rows={4}
                disabled={modifying}
              />

              <button
                onClick={modifyWebsite}
                disabled={!modification.trim() || modifying}
              >
                {modifying ? "Applying Changes..." : "Apply Changes"}
              </button>
            </div>
          )}

          {/* Headings */}
          <h3>Headings</h3>

          {result.headings?.length > 0 ? (
            result.headings.map((item: any, index: number) => (
              <p key={index}>
                {item.tag}: {item.text}
              </p>
            ))
          ) : (
            <p>No headings found.</p>
          )}

          {/* Images */}
          <h3>Images</h3>

          <div className="images">
            {result.images?.slice(0, 10).map((item: any, index: number) => (
              <div key={index}>
                <img
                  src={item.src}
                  alt={item.alt || "Website image"}
                />
                <p>{item.alt || "No description"}</p>
              </div>
            ))}
          </div>

          {/* Sections */}
          <h3>Sections</h3>

          {result.sections?.length > 0 ? (
            result.sections.map((item: any, index: number) => (
              <div key={index}>
                <strong>{item.tag}</strong>
                <p>{item.text}</p>
              </div>
            ))
          ) : (
            <p>No sections found.</p>
          )}

          {/* Design information */}
          <h3>Design Information</h3>

          <pre>{JSON.stringify(result.styles, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;