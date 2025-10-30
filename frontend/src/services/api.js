import axios from "axios";

export const predictImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await axios.post("/api/predict", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data;
  } catch (err) {
    console.error("API Error:", err);
    return { error: "Prediction failed. Check backend logs." };
  }
};
