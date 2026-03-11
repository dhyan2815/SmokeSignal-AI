import { useState } from "react";
import { useDropzone } from "react-dropzone";
import { predictImage } from "../services/api";
import { Upload, X, Image as ImageIcon, Loader2, Flame } from "lucide-react";
import { motion } from "framer-motion";
import clsx from "clsx";

export default function UploadForm({ result, setResult, loading, setLoading }) {
  // ✅ Local state for file and preview only
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);

  // ============================================
  // DRAG & DROP HANDLER
  // ============================================
  const onDrop = (acceptedFiles) => {
    const uploadedFile = acceptedFiles[0];
    setFile(uploadedFile);
    setResult(null); // Clear previous results when new file is uploaded

    // Create image preview
    const reader = new FileReader();
    reader.onload = () => setPreview(reader.result);
    reader.readAsDataURL(uploadedFile);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
    multiple: false,
  });

  // ============================================
  // FORM SUBMISSION HANDLER
  // ============================================
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    const res = await predictImage(file);
    setResult(res); // Update parent state - will show in right column
    setLoading(false);
  };

  // ============================================
  // CLEAR FILE HANDLER
  // ============================================
  const clearFile = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
  };

  return (
    <div className="w-full space-y-6">
      
      {/* ============================================
          FILE UPLOAD ZONE (Drag & Drop or Click)
      ============================================ */}
      {!preview ? (
        <div
          {...getRootProps()}
          className={clsx(
            "relative group cursor-pointer transition-all duration-300",
            "bg-white/5 backdrop-blur-md border-2 border-dashed rounded-3xl p-12",
            "hover:bg-white/10 hover:border-orange-500/50",
            isDragActive
              ? "border-orange-500 bg-orange-500/10 scale-105"
              : "border-white/20"
          )}
        >
          <input {...getInputProps()} />
          <div className="flex flex-col items-center justify-center text-center space-y-4">
            {/* Upload Icon */}
            <motion.div
              animate={{
                y: isDragActive ? -10 : 0,
                scale: isDragActive ? 1.1 : 1,
              }}
              className="p-6 bg-linear-to-br from-orange-500/20 to-red-500/20 rounded-2xl"
            >
              <Upload className="w-12 h-12 text-orange-400" />
            </motion.div>

            {/* Upload Text */}
            <div>
              <h3 className="text-2xl font-bold text-white mb-2">
                {isDragActive ? "Drop it here!" : "Upload Satellite Image"}
              </h3>
              <p className="text-gray-400">
                Drag & drop or click to browse
              </p>
              <p className="text-sm text-gray-500 mt-2">
                Supports: JPG, PNG, WEBP
              </p>
            </div>

            {/* Select File Button */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="button"
              className="px-6 py-3 bg-linear-to-r from-orange-500 to-red-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-orange-500/50 transition-shadow"
            >
              Select File
            </motion.button>
          </div>
        </div>
      ) : (
        /* ============================================
            IMAGE PREVIEW WITH PREDICT BUTTON
        ============================================ */
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="relative bg-white/5 backdrop-blur-md rounded-3xl p-6 border border-white/10"
        >
          {/* Image Preview Container */}
          <div className="relative group">
            <img
              src={preview}
              alt="Preview"
              className="w-full max-h-[300px] md:max-h-[450px] object-contain md:object-cover rounded-2xl shadow-2xl bg-black/20"
            />

            {/* Remove Image Button */}
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={clearFile}
              className="absolute top-4 right-4 p-2 bg-red-500 hover:bg-red-600 text-white rounded-full shadow-lg transition-colors"
              title="Remove image"
            >
              <X className="w-5 h-5" />
            </motion.button>

            {/* File Info Overlay */}
            <div className="absolute bottom-4 left-4 right-4 bg-black/60 backdrop-blur-sm rounded-xl p-3">
              <div className="flex items-center gap-3">
                <ImageIcon className="w-5 h-5 text-orange-400" />
                <div className="flex-1 min-w-0">
                  <p className="text-white font-medium truncate">
                    {file.name}
                  </p>
                  <p className="text-gray-400 text-sm">
                    {(file.size / 1024).toFixed(2)} KB
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* ============================================
              PREDICT BUTTON
          ============================================ */}
          <motion.button
            whileHover={{ scale: loading ? 1 : 1.02 }}
            whileTap={{ scale: loading ? 1 : 0.98 }}
            onClick={handleSubmit}
            disabled={loading}
            className={clsx(
              "w-full mt-6 py-4 rounded-xl font-bold text-lg transition-all",
              "flex items-center justify-center gap-3",
              loading
                ? "bg-gray-600 cursor-not-allowed"
                : "bg-linear-to-r from-orange-500 to-red-600 hover:shadow-2xl hover:shadow-orange-500/50 text-white"
            )}
          >
            {loading ? (
              <>
                <Loader2 className="w-6 h-6 animate-spin" />
                <span>Analyzing Image...</span>
              </>
            ) : (
              <>
                <Flame className="w-6 h-6" />
                <span>Detect Wildfire</span>
              </>
            )}
          </motion.button>
        </motion.div>
      )}
    </div>
  );
}