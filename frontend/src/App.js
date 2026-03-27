import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const API = "https://your-backend.onrender.com/api";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const upload = async () => {
    const reader = new FileReader();

    reader.onloadend = async () => {
      const base64 = reader.result.split(",")[1];

      const res = await axios.post(`${API}/diagnose`, {
        image_base64: base64,
        mime_type: file.type,
      });

      setResult(res.data);
    };

    reader.readAsDataURL(file);
  };

  return (
    <div className="container">
      <h1>🌿 Leaf Health Check</h1>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <br />
      <button onClick={upload}>Analyze</button>

      {result && (
        <div>
          <h3>{result.plant_species}</h3>
          <p>{result.disease_name}</p>
          <p>{result.description}</p>

          <div className="severity-bar">
            <div
              className="fill"
              style={{
                width:
                  result.severity === "Healthy"
                    ? "20%"
                    : result.severity === "Mild"
                    ? "40%"
                    : result.severity === "Moderate"
                    ? "60%"
                    : result.severity === "Severe"
                    ? "80%"
                    : "100%",
              }}
            />
          </div>

          <ul>
            {result.rescue_tips.map((t, i) => (
              <li key={i}>{t}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
