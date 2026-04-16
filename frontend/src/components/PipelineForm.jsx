/**
 * Form component for submitting pipeline input.
 */
import { useState } from "react";
import PropTypes from "prop-types";
import { processPipeline } from "../api/pipeline";

const DEFAULT_TITLE_PROMPT =
  `You are an expert travel blogger who creates content for high-performing travel accommodation, event, and activity booking websites that are search engine optimized. Rephrase the "{PropertyName}" title into a more SEO-friendly title. Use only the provided data without introducing new information or assumptions. The output should be in plain text. The text should be SEO-optimized for keywords related to the location. Write the sentences subtly, so that the keyword has the highest NLP Salience Score. Incorporate the location naturally within the content. Use pronouns or alternative references when the location has been established.`;

const DEFAULT_DESCRIPTION_PROMPT =
  `You are an expert travel blogger who creates content for high-performing travel accommodation, event and activity booking websites that are search engine optimized. Rephrase the following activity description "{PropertyDescription}" into a more SEO-friendly and engaging paragraph by emphasizing key experiences, unique features, and specific location highlights to attract potential guests and improve online discoverability. Use only the content provided in the given description without adding new details or assumptions. The output should be in HTML markup. The text must contain exactly ONE HTML paragraph. Wrap the entire content inside a single <p>...</p> tag. Do not include any text or HTML elements outside this one <p> tag. The text should be SEO optimized towards the keywords: relating to the location. Write the sentences subtly, so that the keyword has the highest NLP Salience Score. Incorporate the location naturally within the content. Use pronouns or alternative references when the location has been established.`;

export default function PipelineForm({ onSuccess, onError }) {
  const [form, setForm] = useState({
    siteName:            "",
    titlePrompt:         DEFAULT_TITLE_PROMPT,
    descriptionPrompt:   DEFAULT_DESCRIPTION_PROMPT,
    csvFile:             null,
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
        siteName:          form.siteName,
        titlePrompt:       form.titlePrompt,
        descriptionPrompt: form.descriptionPrompt,
        csvFile:           form.csvFile,
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
        <label htmlFor="titlePrompt">Title Prompt</label>
        <textarea
          id="titlePrompt"
          name="titlePrompt"
          value={form.titlePrompt}
          onChange={handleChange}
          rows={6}
          required
        />
        <span className="hint">
          Must contain <code>{"{PropertyName}"}</code> placeholder.
        </span>
      </div>

      <div className="field">
        <label htmlFor="descriptionPrompt">Description Prompt</label>
        <textarea
          id="descriptionPrompt"
          name="descriptionPrompt"
          value={form.descriptionPrompt}
          onChange={handleChange}
          rows={8}
          required
        />
        <span className="hint">
          Must contain <code>{"{PropertyDescription}"}</code> placeholder.
        </span>
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
        <span className="hint">
          CSV must have exactly one row with columns: id, title, description.
        </span>
      </div>

      <button type="submit" disabled={loading}>
        {loading ? "Processing..." : "Run Pipeline"}
      </button>
    </form>
  );
}

PipelineForm.propTypes = {
  onSuccess: PropTypes.func.isRequired,
  onError:   PropTypes.func.isRequired,
};