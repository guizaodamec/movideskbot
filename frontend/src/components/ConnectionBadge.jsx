import { motion } from 'framer-motion'

export default function ConnectionBadge({ connected, animate = false, size = 10 }) {
  const color = connected ? '#22c55e' : '#ef4444'

  return (
    <span className="relative inline-flex items-center justify-center flex-shrink-0"
      style={{ width: size + 4, height: size + 4 }}>
      <span
        className="rounded-full block"
        style={{ width: size, height: size, backgroundColor: color }}
      />
      {animate && connected && (
        <motion.span
          className="absolute rounded-full"
          style={{ inset: 0, backgroundColor: color }}
          animate={{ scale: [1, 2, 1], opacity: [0.5, 0, 0.5] }}
          transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
        />
      )}
    </span>
  )
}
