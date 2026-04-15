/**
 * Displays the pipeline processing result.
 */
export default function PipelineResult({ result }) {
  if (!result) return null;

  return (
    <div className="result">
      <h2>{result.message}</h2>

      <section>
        <h3>AI Enhanced Content</h3>
        <p><strong>Title:</strong> {result.ai_result.title}</p>
        <div>
          <strong>Description:</strong>
          <div dangerouslySetInnerHTML={{ __html: result.ai_result.description }} />
        </div>
      </section>

      <section>
        <h3>Stored Files</h3>
        <p><strong>Input:</strong> {result.input_stored_at}</p>
        <p><strong>AI Response:</strong> {result.ai_response_stored_at}</p>
        <ul>
          {result.per_id_files.map((key) => (
            <li key={key}>{key}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}