export default function ResultCard({ result }) {
    if (result.error) {
      return (
        <div className="bg-red-100 text-red-800 p-4 rounded-lg shadow-md">
          <strong>Error:</strong> {result.error}
        </div>
      );
    }
  
    return (
      <div className="bg-white shadow-lg rounded-xl p-6 w-80 text-center border">
        <h2 className="text-xl font-bold mb-3">
          {result.label === "Wildfire" ? "🔥 Wildfire Detected" : "✅ No Fire Detected"}
        </h2>
        <p className="text-gray-700">
          Confidence: <strong>{(result.confidence * 100).toFixed(2)}%</strong>
        </p>
      </div>
    );
  }
  