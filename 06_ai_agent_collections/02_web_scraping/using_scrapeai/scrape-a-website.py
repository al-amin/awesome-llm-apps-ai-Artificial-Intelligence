# import nest_asyncio
# nest_asyncio.apply()

from scrapegraphai.graphs import SmartScraperGraph

graph_config = {
    "llm": {
        "model": "ollama/llama3.2:latest",
        "temperature": 0,
        "format": "json",  # Ollama needs the format to be specified explicitly
        "base_url": "http://localhost:11434",  # set Ollama URL
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text:latest",
        "base_url": "http://localhost:11434",  # set Ollama URL
    }
}

smart_scraper_graph = SmartScraperGraph(
    prompt="List me all the articles",
    source="https://www.facebook.com/",
    config=graph_config
)

result = smart_scraper_graph.run()
print("**************************************")
print("\n")
print(result)
print("\n")
print("**************************************")