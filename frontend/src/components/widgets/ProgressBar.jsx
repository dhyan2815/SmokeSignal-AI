import { motion } from "framer-motion";

export function ProgressBar({ value, isFire = true }) {
  return (
    <div className="relative w-full h-4 bg-white/10 rounded-full overflow-hidden backdrop-blur-sm">
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: `${value}%` }}
        transition={{ duration: 1, ease: "easeOut" }}
        className={`h-full rounded-full relative ${
          isFire
            ? "bg-gradient-to-r from-orange-500 to-red-600"
            : "bg-gradient-to-r from-green-500 to-emerald-600"
        }`}
      >
        {/* Shimmer Effect */}
        <motion.div
          animate={{
            x: ["-100%", "200%"],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "linear",
          }}
          className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent"
        />
      </motion.div>

      {/* Percentage Markers */}
      <div className="absolute inset-0 flex justify-between px-2 items-center pointer-events-none">
        {[25, 50, 75].map((marker) => (
          <div
            key={marker}
            className="w-px h-2 bg-white/30"
            style={{ marginLeft: `${marker}%` }}
          />
        ))}
      </div>
    </div>
  );
}