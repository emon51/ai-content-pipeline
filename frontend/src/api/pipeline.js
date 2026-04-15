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
 * @param {string} params.title
 * @param {string} params.description
 * @param {File}   params.csvFile
 * @returns {Promise<Object>} API response data
 */
export async function processPipeline({ siteName, title, description, csvFile }) {
  const formData = new FormData();
  formData.append("site_name", siteName);
  formData.append("title", title);
  formData.append("description", description);
  formData.append("csv_file", csvFile);

  const response = await axios.post(`${BASE_URL}/process/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
}