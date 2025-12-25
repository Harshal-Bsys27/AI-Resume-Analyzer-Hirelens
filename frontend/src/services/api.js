const API_BASE = "http://127.0.0.1:5000";

export async function analyzeResume(formData) {
  try {
    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      body: formData,
    });

    // Handle backend error responses
    if (!response.ok) {
      let errorJson;
      try {
        errorJson = await response.json();
      } catch {
        errorJson = { error: await response.text() };
      }
      return errorJson;
    }

    // Successful response
    const data = await response.json();
    return data;

  } catch (error) {
    console.error("API ERROR:", error);
    return { error: "Network or server error" };
  }
}
