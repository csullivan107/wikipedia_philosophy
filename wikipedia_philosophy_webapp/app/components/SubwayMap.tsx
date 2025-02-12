"use client"

import type React from "react"
import { useEffect, useRef, useState } from "react"
import { motion, AnimatePresence } from "framer-motion"

interface SubwayMapProps {
  stations: string[]
  animationProgress: number
}

const SubwayMap: React.FC<SubwayMapProps> = ({ stations, animationProgress }) => {
  const colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8", "#F7DC6F", "#BB8FCE", "#82E0AA"]
  const svgRef = useRef<SVGSVGElement>(null)
  const [svgHeight, setSvgHeight] = useState(0)

  useEffect(() => {
    if (svgRef.current) {
      const height = stations.length * 100 + 50 // Increased spacing and padding
      setSvgHeight(height)
      svgRef.current.setAttribute("viewBox", `0 0 100% ${height}`)
    }
  }, [stations])

  const nodeVariants = {
    initial: { scale: 2, opacity: 0 },
    animate: { scale: 1, opacity: 1 },
    exit: { scale: 0, opacity: 0 },
  }

  const lineVariants = {
    initial: { pathLength: 0 },
    animate: { pathLength: 1 },
    transition: { duration: 0.5 },
  }

  return (
    <svg ref={svgRef} width="100%" height={svgHeight} className="subway-map">
      <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L0,6 L9,3 z" fill="#333" />
        </marker>
      </defs>

      <AnimatePresence>
        {stations.map((station, index) => {
          const y = (index + 1) * 100 // Increased spacing
          const color = colors[index % colors.length]
          const nextY = (index + 2) * 100 // Increased spacing
          const isVisible = index < animationProgress

          return (
            <motion.g
              key={index}
              initial="initial"
              animate={isVisible ? "animate" : "initial"}
              exit="exit"
              transition={{ duration: 0.5, delay: index * 0.5, staggerChildren: 0.1 }}
            >
              {/* Clickable node group */}
              <a href={`https://en.wikipedia.org${station}`} target="_blank" rel="noopener noreferrer">
                <motion.g variants={nodeVariants}>
                  {/* Station circle */}
                  <circle cx="60" cy={y} r="12" fill={color} stroke="#333" strokeWidth="2" />{" "}
                  {/* Increased size and adjusted position */}
                  {/* Station name */}
                  <text x="85" y={y + 6} fontSize="18" fill="#333">
                    {" "}
                    {/* Adjusted position and increased font size */}
                    {station.replace("/wiki/", "")}
                  </text>
                </motion.g>
              </a>

              {/* Connecting line */}
              {index < stations.length - 1 && (
                <motion.line
                  x1="60" // Adjusted to match circle center
                  y1={y + 12} // Start from bottom of the circle
                  x2="60" // Adjusted to match circle center
                  y2={nextY - 12} // End at top of the next circle
                  stroke="#333"
                  strokeWidth="3"
                  strokeDasharray="5,5"
                  variants={lineVariants}
                />
              )}
            </motion.g>
          )
        })}
      </AnimatePresence>
    </svg>
  )
}

export default SubwayMap

