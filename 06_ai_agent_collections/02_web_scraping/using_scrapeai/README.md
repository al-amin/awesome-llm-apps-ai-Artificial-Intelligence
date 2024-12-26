# ScrapeGraphAI

ScrapeGraphAI is a web scraping python library that uses LLM and direct graph logic to create scraping pipelines for websites and local documents (XML, HTML, JSON, Markdown, etc.). The library is designed to be easy to use and flexible, allowing users to extract information from websites and local files.

## Features

*   Uses LLM to extract information from a website or local document
*   Supports web scraping of websites and local documents (XML, HTML, JSON, Markdown, etc.)
*   Supports multiple scraping pipelines
*   Supports user-defined prompts and source URLs
*   Supports optional dependencies

## Optional Dependencies

The library has the following optional dependencies:

*   `playwright` for web scraping
*   `beautifulsoup4` for local document parsing
*   `requests` for web scraping

## Installation

To install the library, use the following command:

```bash
conda create -n scrapeai python=3.11
conda activate scrapeai 
pip install scrapegraphai
pip install nest_asyncio
pip install playwright
playwright install-deps
playwright install
```

ref [ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai)


