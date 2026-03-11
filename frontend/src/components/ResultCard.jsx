import { motion } from "framer-motion";
import { ProgressBar } from "./widgets/ProgressBar";
import {
  AlertTriangle,
  CheckCircle2,
  XCircle,
  TrendingUp,
  Info,
} from "lucide-react";

export default function ResultCard({ result }) {
  // ============================================
  // ERROR STATE
  // ============================================
  if (result.error) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        className="bg-red-500/10 backdrop-blur-md border border-red-500/30 rounded-3xl p-6 shadow-2xl"
      >
        <div className="flex items-start gap-4">
          <div className="p-3 bg-red-500/20 rounded-xl">
            <XCircle className="w-8 h-8 text-red-400" />
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-bold text-red-400 mb-1">
              Analysis Failed
            </h3>
            <p className="text-gray-300">{result.error}</p>
          </div>
        </div>
      </motion.div>
    );
  }

  // ============================================
  // EXTRACT RESULT DATA
  // ============================================
  const isFire = result.label === "Wildfire";
  const confidence = result.confidence * 100;

  // ============================================
  // SUCCESS STATE WITH RESULTS
  // ============================================
  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      className={`relative overflow-hidden backdrop-blur-md rounded-3xl p-6 md:p-8 shadow-2xl border-2 ${
        isFire
          ? "bg-red-500/10 border-red-500/30"
          : "bg-green-500/10 border-green-500/30"
      }`}
    >
      {/* ============================================
          ANIMATED BACKGROUND GLOW
      ============================================ */}
      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.5, 0.3],
        }}
        transition={{ duration: 3, repeat: Infinity }}
        className={`absolute inset-0 blur-3xl ${
          isFire ? "bg-red-500/20" : "bg-green-500/20"
        }`}
      />

      <div className="relative z-10">
        {/* ============================================
            HEADER WITH ICON AND TITLE
        ============================================ */}
        <div className="flex items-center justify-between mb-4 md:mb-6">
          <div className="flex items-center gap-3 md:gap-4">
            {/* Animated Icon */}
            <motion.div
              initial={{ rotate: 0, scale: 0 }}
              animate={{ rotate: 360, scale: 1 }}
              transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
              className={`p-3 md:p-4 rounded-xl md:rounded-2xl shadow-xl ${
                isFire
                  ? "bg-linear-to-br from-red-500 to-orange-600"
                  : "bg-linear-to-br from-green-500 to-emerald-600"
              }`}
            >
              {isFire ? (
                <AlertTriangle className="w-8 h-8 md:w-10 md:h-10 text-white" />
              ) : (
                <CheckCircle2 className="w-8 h-8 md:w-10 md:h-10 text-white" />
              )}
            </motion.div>

            {/* Title and Subtitle */}
            <div>
              <h2
                className={`text-2xl md:text-3xl font-black ${
                  isFire ? "text-red-400" : "text-green-400"
                }`}
              >
                {isFire ? "Wildfire Detected" : "No Fire Detected"}
              </h2>
              <p className="text-gray-400 text-xs mt-0.5">
                Analysis completed successfully
              </p>
            </div>
          </div>
        </div>

        {/* ============================================
            CONFIDENCE LEVEL DISPLAY
        ============================================ */}
        <div className="space-y-2 md:space-y-3 mb-4 md:mb-6">
          <div className="flex items-center justify-between">
            <span className="text-gray-300 text-sm font-medium flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Confidence
            </span>
            <span className="text-xl md:text-2xl font-bold text-white">
              {confidence.toFixed(1)}%
            </span>
          </div>

          {/* Progress Bar Component */}
          <ProgressBar value={confidence} isFire={isFire} />
        </div>

        {/* ============================================
            ADDITIONAL CONTEXT INFO
        ============================================ */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="flex items-start gap-3 p-3 md:p-4 bg-white/5 rounded-xl border border-white/10"
        >
          <Info className="w-4 h-4 text-blue-400 mt-0.5 shrink-0" />
          <p className="text-[11px] md:text-sm text-gray-300 leading-tight">
            {isFire
              ? "⚠️ Immediate action recommended. Alert local authorities."
              : "✅ No threats detected. Continue routine monitoring."}
          </p>
        </motion.div>
      </div>
    </motion.div>
  );
}