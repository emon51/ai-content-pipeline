/**
 * Form component for submitting pipeline input.
 */
import { useState } from "react";
import PropTypes from "prop-types";
import { processPipeline } from "../api/pipeline";

export default function PipelineForm({ onSuccess, onError }) {
  const [form, setForm] = useState({
    siteName: "",
    title: "",
    description: "",
    csvFile: null,
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: files ? files[0] : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    onError(null);

    try {
      const result = await processPipeline({
        siteName: form.siteName,
        title: form.title,
        description: form.description,
        csvFile: form.csvFile,
      });
      onSuccess(result);
    } catch (err) {
      onError(err.response?.data?.error || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <div className="field">
        <label htmlFor="siteName">Site Name</label>
        <input
          id="siteName"
          name="siteName"
          placeholder="e.g. rentbyowner.com"
          value={form.siteName}
          onChange={handleChange}
          required
        />
      </div>

      <div className="field">
        <label htmlFor="title">Title</label>
        <input
          id="title"
          name="title"
          placeholder="e.g. Luxury Beach Villa"
          value={form.title}
          onChange={handleChange}
          required
        />
      </div>

      <div className="field">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          placeholder="e.g. A beautiful villa near the sea with pool"
          value={form.description}
          onChange={handleChange}
          rows={4}
          required
        />
      </div>

      <div className="field">
        <label htmlFor="csvFile">CSV File</label>
        <input
          id="csvFile"
          type="file"
          name="csvFile"
          accept=".csv"
          onChange={handleChange}
          required
        />
      </div>

      <button type="submit" disabled={loading}>
        {loading ? "Processing..." : "Run Pipeline"}
      </button>
    </form>
  );
}

PipelineForm.propTypes = {
  onSuccess: PropTypes.func.isRequired,
  onError: PropTypes.func.isRequired,
};