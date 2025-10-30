import { useState } from "react";
import { predictImage } from "../services/api";
import ResultCard from "./ResultCard";

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please upload an image first.");

    setLoading(true);
    const res = await predictImage(file);
    setResult(res);
    setLoading(false);
  };

  return (
    <div className="flex lex-col items-center gap-6 p-6">
      <form onSubmit={handleSubmit} className="flex flex-col items-center gap-4">
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
          className="p-2 border rounded-md"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          {loading ? "Analyzing..." : "Predict Fire"}
        </button>
      </form>

      {result && <ResultCard result={result} />}
    </div>
  );
}
