import { motion } from 'framer-motion'

export default function LoadingDots({ size = 6, color = '#3b82f6' }) {
  return (
    <span className="inline-flex items-center gap-1 py-0.5">
      {[0, 1, 2].map((i) => (
        <motion.span
          key={i}
          className="rounded-full block flex-shrink-0"
          style={{ width: size, height: size, backgroundColor: color }}
          animate={{ opacity: [0.3, 1, 0.3], y: [0, -3, 0] }}
          transition={{ duration: 1.2, repeat: Infinity, delay: i * 0.2 }}
        />
      ))}
    </span>
  )
}
