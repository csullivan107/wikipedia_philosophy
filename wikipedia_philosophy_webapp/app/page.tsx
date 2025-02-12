"use client"

import { useState, useEffect } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2 } from "lucide-react"
import SubwayMap from "./components/SubwayMap"

export default function WikipediaPhilosophyGame() {
  const [startArticle, setStartArticle] = useState("")
  const [results, setResults] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [animationProgress, setAnimationProgress] = useState(0)

  useEffect(() => {
    if (results.length > 0) {
      const interval = setInterval(() => {
        setAnimationProgress((prev) => {
          if (prev < results.length) {
            return prev + 1
          }
          clearInterval(interval)
          return prev
        })
      }, 500) // Adjust this value to control animation speed

      return () => clearInterval(interval)
    }
  }, [results])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")
    setResults([])
    setAnimationProgress(0)

    try {
      const response = await fetch("/api/philosophy-game", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ startArticle }),
      })

      if (!response.ok) {
        throw new Error("Failed to fetch results")
      }

      const data = await response.json()
      setResults(data.path)
    } catch (err) {
      setError("An error occurred while fetching results.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container mx-auto p-4">
      <Card className="w-full max-w-6xl mx-auto">
        {" "}
        {/* Increased max-width */}
        <CardHeader>
          <CardTitle className="text-3xl font-bold text-center">Wiki Philosophy Subway</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4 mb-8">
            <Input
              type="text"
              placeholder="Enter Wikipedia article title or leave blank for random"
              value={startArticle}
              onChange={(e) => setStartArticle(e.target.value)}
              className="text-lg"
            />
            <Button type="submit" disabled={isLoading} className="w-full text-lg">
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-6 w-6 animate-spin" />
                  Mapping route...
                </>
              ) : (
                "Start Journey to Philosophy"
              )}
            </Button>
          </form>
          {error && <p className="text-red-500 text-center">{error}</p>}
          {results.length > 0 && (
            <div className="w-full">
              <SubwayMap stations={results} animationProgress={animationProgress} />
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

