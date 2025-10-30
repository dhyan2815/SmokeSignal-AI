import UploadForm from "./components/UploadForm";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">
        SmokeSignal AI — Fire Detection
      </h1>
      <UploadForm />
    </div>
  );
}
