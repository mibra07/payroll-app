
import axios from "axios";

// STEP A1: Create API instance
const API = axios.create({
    baseURL: "http://127.0.0.1:8000",
    headers: {
        "Content-Type": "application/json",
    },
});

// --------------------------------------------------------------
// STEP A2: UPLOAD FILE FUNCTIO 
// --------------------------------------------------------------
export const uploadFile = async(url, file) => {
    console.log("STEP A2.1: uploadFile() called");
    console.log("STEP A2.2: URL", url);
    console.log("STEP A2.2: file", file);

    const formData = new FormData();

    // STEP A2.4 attach file
    // 👇 IMPORTANT: key must match FastAPI parameter name
    formData.append("file", file);
    console.log("STEP A2.4 File appended", file?.name);

    try {
        // STEP A2.5 send request
        console.log("STEP A2.5: sending POST request...");
        const response = await API.post(url, formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });
        // STEP A2.6: Response Received
        console.log("STEP A2.6: Response Received", response.data);
        return response;
    } catch (error) {
        console.error("A2.ERROR: upload failed", error);
        throw error;
    }

}

// --------------------------------------------------------------
// STEP A3: GET SUMMARY FUNCTION
// --------------------------------------------------------------
export const getSummary = async (params) => {

  console.log("STEP A3.1 → getSummary called with params:", params);

  try {
    // STEP A3.2 → API CALL
    const response = await API.get('/summary', { params });

    console.log("STEP A3.3 → Summary response:", response.data);

    return response;

  } catch (error) {
    console.error("STEP A3.4 → Summary error:", error);
    throw error;
  }
};


// --------------------------------------------------------------
// STEP A4: GET CSV DOWNLOAD URL FUNCTION
// --------------------------------------------------------------
export const getCSVUrl = (params = {}) => {

  console.log("STEP A4.1 → generating CSV URL params:", params);

  // STEP A4.2 → Create query builder
  const query = new URLSearchParams();

  // STEP A4.3 → Append valid params
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== "") {

      console.log(`STEP A4.3 → Appending ${key} = ${value}`);

      query.append(key, value);
    }
  });

  // STEP A4.4 → Convert to query string
  const queryString = query.toString();

  // STEP A4.5 → Build final URL
  const url = queryString
    ? `http://127.0.0.1:8000/summary.csv?${queryString}`
    : `http://127.0.0.1:8000/summary.csv`;

  console.log("STEP A4.6 → Generated CSV URL:", url);

  // STEP 4.7 → Return URL
  return url;
};

