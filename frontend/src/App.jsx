import { useState } from "react";
import UploadForm from "./components/UploadForm";
import ResultCard from "./components/ResultCard";
import { Flame, Shield, Sparkles } from "lucide-react";
import { motion } from "framer-motion";

export default function App() {
  // ✅ Lift state up to App level for sharing between left and right panels
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* ============================================
            FOREST FIRE CLIP BACKGROUND VIDEO
        ============================================ */}
      <video
        src="/forest_fire_clip.mp4"
        autoPlay
        loop
        muted
        className="absolute inset-0 w-full h-full object-cover z-0"
      />
      {/* ============================================
          ANIMATED BACKGROUND ELEMENTS
      ============================================ */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 90, 0],
          }}
          transition={{ duration: 20, repeat: Infinity }}
          className="absolute top-1/4 -left-20 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"
        />
        <motion.div
          animate={{
            scale: [1.2, 1, 1.2],
            rotate: [90, 0, 90],
          }}
          transition={{ duration: 15, repeat: Infinity }}
          className="absolute bottom-1/4 -right-20 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"
        />
      </div>

      {/* ============================================
          MAIN CONTENT WRAPPER
      ============================================ */}
      <div className="relative z-10 flex flex-col min-h-screen px-4 py-4 md:py-8">

        {/* ============================================
            HEADER SECTION (Full Width)
        ============================================ */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-6 md:mb-10"
        >
          <div className="flex flex-col md:flex-row items-center justify-center gap-2 md:gap-4 pt-2">
            {/* Logo/Icon */}
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
              className="inline-flex items-center justify-center w-12 h-12 md:w-16 md:h-16 mb-2 md:mb-0 bg-linear-to-br from-orange-500 to-red-600 rounded-xl md:rounded-2xl shadow-2xl"
            >
              <Flame className="w-6 h-6 md:w-8 md:h-8 text-white" />
            </motion.div>

            {/* Title */}
            <h1 className="text-4xl md:text-6xl font-black text-transparent bg-clip-text bg-linear-to-r from-orange-400 via-red-500 to-pink-500 tracking-tight py-2">
              SmokeSignal AI
            </h1>
          </div>

          {/* Subtitle */}
          <p className="text-gray-300 text-sm md:text-base max-w-xl mx-auto leading-relaxed px-4">
            Advanced wildfire detection powered by deep learning. Upload
            satellite imagery for instant analysis with{" "}
            <span className="text-orange-400 font-semibold">95%+ accuracy</span>
          </p>

          {/* Feature Pills */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="flex flex-wrap justify-center gap-3 mt-4"
          >
            {[
              { icon: Sparkles, text: "Real-time Detection" },
              { icon: Shield, text: "CNN-Based Model" },
              { icon: Flame, text: "High Accuracy" },
            ].map((feature, idx) => (
              <div
                key={idx}
                className="flex items-center gap-2 px-3 py-1.5 bg-white/5 backdrop-blur-sm rounded-full border border-white/10"
              >
                <feature.icon className="w-4 h-4 text-orange-400" />
                <span className="text-sm text-gray-300">{feature.text}</span>
              </div>
            ))}
          </motion.div>
        </motion.div>

        {/* ============================================
            TWO COLUMN GRID LAYOUT
            - Left: Upload Form & Image Preview
            - Right: Results Card
        ============================================ */}
        <div className="flex-1 max-w-7xl w-full mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">

            {/* ============================================
                LEFT COLUMN - Upload Form
            ============================================ */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="w-full"
            >
              <UploadForm
                result={result}
                setResult={setResult}
                loading={loading}
                setLoading={setLoading}
              />
            </motion.div>

            {/* ============================================
                RIGHT COLUMN - Results Display
            ============================================ */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
              className="w-full lg:sticky lg:top-8"
            >
              {/* Show result card when available, otherwise show placeholder */}
              {result ? (
                <ResultCard result={result} />
              ) : (
                // ============================================
                // PLACEHOLDER WHEN NO RESULTS
                // ============================================
                <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-3xl p-8 md:p-12 text-center min-h-[300px] md:min-h-[400px] flex flex-col items-center justify-center">
                  <motion.div
                    animate={{
                      scale: [1, 1.1, 1],
                      opacity: [0.5, 0.8, 0.5],
                    }}
                    transition={{ duration: 3, repeat: Infinity }}
                    className="w-24 h-24 mb-6 bg-linear-to-br from-orange-500/20 to-red-500/20 rounded-full flex items-center justify-center"
                  >
                    <Flame className="w-12 h-12 text-orange-400/50" />
                  </motion.div>
                  <h3 className="text-2xl font-bold text-gray-400 mb-2">
                    Awaiting Analysis
                  </h3>
                  <p className="text-gray-500 max-w-sm">
                    Upload an image to see wildfire detection results here
                  </p>
                </div>
              )}
            </motion.div>

          </div>
        </div>
      </div>
    </div>
  );
}