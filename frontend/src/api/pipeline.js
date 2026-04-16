/**
 * API client for the content pipeline backend.
 */
import axios from "axios";

const BASE_URL = "http://localhost:8000/api/v1";

/**
 * Submit pipeline form data to the backend.
 *
 * @param {Object} params
 * @param {string} params.siteName
 * @param {string} params.titlePrompt
 * @param {string} params.descriptionPrompt
 * @param {File}   params.csvFile
 * @returns {Promise<Object>} API response data
 */
export async function processPipeline({
  siteName,
  titlePrompt,
  descriptionPrompt,
  csvFile,
}) {
  const formData = new FormData();
  formData.append("site_name",          siteName);
  formData.append("title_prompt",       titlePrompt);
  formData.append("description_prompt", descriptionPrompt);
  formData.append("csv_file",           csvFile);

  const response = await axios.post(`${BASE_URL}/process/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
}