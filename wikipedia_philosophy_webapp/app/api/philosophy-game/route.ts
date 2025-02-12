import { NextResponse } from "next/server"
import * as cheerio from "cheerio"

async function getWikiSoup(articleTitle: string) {
  const url = `https://en.wikipedia.org${articleTitle}`
  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const html = await response.text()
    return cheerio.load(html)
  } catch (error) {
    console.error(`Error fetching page: ${error}`)
    return null
  }
}

function getFirstParagraph($: cheerio.CheerioAPI) {
  const content = $("#mw-content-text")
  return content.find("p:not(.mw-empty-elt)").first()
}

function getLinksFromParagraph($: cheerio.CheerioAPI, paragraph: cheerio.Cheerio) {
  const links: string[] = []
  paragraph.find("a").each((_, element) => {
    const href = $(element).attr("href")
    if (href && href.startsWith("/wiki/") && !href.includes(":")) {
      const parentText = $(element).parent().text()
      const linkText = $(element).text()
      const beforeLink = parentText.substring(0, parentText.indexOf(linkText))
      if ((beforeLink.match(/$$/g) || []).length <= (beforeLink.match(/$$/g) || []).length) {
        links.push(href)
      }
    }
  })
  return links
}

function isPhilosophyLink(links: string[]) {
  return links[0] === "/wiki/Philosophy"
}

export async function POST(req: Request) {
  try {
    const { startArticle } = await req.json()
    let currentArticle = startArticle ? `/wiki/${startArticle}` : "/wiki/Special:Random"
    const articlesVisited: string[] = []
    const visitedSet = new Set<string>()

    while (true) {
      if (visitedSet.has(currentArticle)) {
        return NextResponse.json({ path: articlesVisited, error: "Loop detected" })
      }

      articlesVisited.push(currentArticle)
      visitedSet.add(currentArticle)

      const $ = await getWikiSoup(currentArticle)
      if (!$) {
        return NextResponse.json({ path: articlesVisited, error: "Failed to fetch page" })
      }

      const firstParagraph = getFirstParagraph($)
      const links = getLinksFromParagraph($, firstParagraph)

      if (links.length === 0) {
        return NextResponse.json({ path: articlesVisited, error: "No links found" })
      }

      if (isPhilosophyLink(links)) {
        articlesVisited.push("/wiki/Philosophy")
        return NextResponse.json({ path: articlesVisited })
      }

      currentArticle = links[0]
    }
  } catch (error) {
    console.error("Unexpected error:", error)
    return NextResponse.json({ error: "An unexpected error occurred" }, { status: 500 })
  }
}

