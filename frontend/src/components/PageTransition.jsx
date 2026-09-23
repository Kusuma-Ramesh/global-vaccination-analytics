import { motion, useReducedMotion } from "framer-motion";

/**
 * PageTransition — a single, restrained enter animation for routed pages.
 * Respects prefers-reduced-motion by skipping the animation entirely.
 */
export default function PageTransition({ children }) {
  const shouldReduceMotion = useReducedMotion();

  if (shouldReduceMotion) {
    return children;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.28, ease: [0.16, 1, 0.3, 1] }}
    >
      {children}
    </motion.div>
  );
}
