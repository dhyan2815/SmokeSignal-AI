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
      <div className="relative z-10 flex flex-col h-screen px-4 py-2 md:py-4">

        {/* ============================================
            HEADER SECTION (Compact)
        ============================================ */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-4 md:mb-6"
        >
          <div className="flex items-center justify-center gap-3 pt-1">
            <motion.div
              className="inline-flex items-center justify-center w-10 h-10 md:w-12 md:h-12 bg-linear-to-br from-orange-500 to-red-600 rounded-lg md:rounded-xl shadow-xl"
            >
              <Flame className="w-5 h-5 md:w-6 md:h-6 text-white" />
            </motion.div>

            <h1 className="text-3xl md:text-5xl font-black text-transparent bg-clip-text bg-linear-to-r from-orange-400 via-red-500 to-pink-500 tracking-tight py-1">
              SmokeSignal AI
            </h1>
          </div>

          <p className="text-gray-300 text-xs md:text-sm max-w-lg mx-auto leading-tight opacity-90">
            Advanced wildfire detection powered by deep learning.
          </p>
        </motion.div>

        {/* ============================================
            TWO COLUMN GRID LAYOUT (Tighter)
        ============================================ */}
        <div className="flex-1 max-w-6xl w-full mx-auto overflow-hidden">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6 items-start h-full">

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
                <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-3xl p-6 md:p-8 text-center min-h-[250px] md:min-h-[350px] flex flex-col items-center justify-center">
                  <motion.div
                    animate={{
                      scale: [1, 1.1, 1],
                      opacity: [0.5, 0.8, 0.5],
                    }}
                    transition={{ duration: 3, repeat: Infinity }}
                    className="w-16 h-16 md:w-20 md:h-20 mb-4 bg-linear-to-br from-orange-500/20 to-red-500/20 rounded-full flex items-center justify-center"
                  >
                    <Flame className="w-8 h-8 md:w-10 md:h-10 text-orange-400/50" />
                  </motion.div>
                  <h3 className="text-xl font-bold text-gray-400 mb-1">
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

        {/* ============================================
            FOOTER (Compact)
        ============================================ */}
        <div className="mt-auto py-2 text-center">
          <p className="text-gray-500 text-[10px] md:text-xs uppercase tracking-widest opacity-60">
            © 2026 SmokeSignal AI • Built by Dhyan Patel
          </p>
        </div>
      </div>
    </div>
  );
}