/**
 * Root application component.
 */
import { useState } from "react";
import PipelineForm from "./components/PipelineForm";
import PipelineResult from "./components/PipelineResult";
import "./App.css";

export default function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  return (
    <div className="container">
      <h1>AI Content Pipeline</h1>
      <p className="subtitle">SEO-enhanced property content generator</p>

      <PipelineForm onSuccess={setResult} onError={setError} />

      {error && <div className="error">{error}</div>}

      <PipelineResult result={result} />
    </div>
  );
}