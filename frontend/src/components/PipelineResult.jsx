/**
 * Displays the pipeline processing result.
 */
import PropTypes from "prop-types";

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
        <ul>
          <li><strong>Input:</strong> {result.input_stored_at}</li>
          <li><strong>Output:</strong> {result.output_stored_at}</li>
          <li><strong>ID File:</strong> {result.id_file_stored_at}</li>
        </ul>
      </section>
    </div>
  );
}

PipelineResult.propTypes = {
  result: PropTypes.shape({
    message:          PropTypes.string.isRequired,
    input_stored_at:  PropTypes.string.isRequired,
    output_stored_at: PropTypes.string.isRequired,
    id_file_stored_at: PropTypes.string.isRequired,
    ai_result: PropTypes.shape({
      title:       PropTypes.string.isRequired,
      description: PropTypes.string.isRequired,
    }).isRequired,
  }),
};

PipelineResult.defaultProps = {
  result: null,
};