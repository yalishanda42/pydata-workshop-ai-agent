from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openrouter import OpenRouter
from dotenv import load_dotenv

load_dotenv()

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://recepti.gotvach.bg"


def _fetch(url: str, params: dict | None = None) -> BeautifulSoup:
    response = requests.get(
        url, params=params, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
    )
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def search_recipes(query: str) -> str:
    """Търси рецепти в gotvach.bg и връща пълната първа рецепта и линкове към останалите.

    Args:
        query: Само името на ястието или продукта, например "мусака" или "тиквички".
    """
    page = _fetch(BASE_URL + "/", params={"kw": query.strip()})
    links = page.select("div.rprev a.title")
    if not links:
        return "Няма намерени рецепти."
    results = "\n".join(f"- {a.get_text(strip=True)}: {a['href']}" for a in links[:20])
    return f"{get_recipe(links[0]['href'])}\n\nДруги резултати:\n{results}"


def get_recipe(url: str) -> str:
    """Връща съставките и начина на приготвяне на конкретна рецепта от gotvach.bg.

    Args:
        url: Пълният адрес на рецептата, върнат от search_recipes.
    """
    page = _fetch(url)
    title = page.select_one("h1").get_text(strip=True)
    products = page.select_one("section.products")
    products = products.get_text("\n", strip=True) if products else ""
    steps = "\n".join(
        p.get_text(" ", strip=True) for p in page.select("div.text p.desc")
    )
    content = f"{products}\n\nНачин на приготвяне:\n{steps}"[:4000]
    return f"{title}\n{url}\n\n{content}"


agent = Agent(
    id="mandjev",
    name="Манджев",
    model=OpenRouter(id="deepseek/deepseek-v4.1-flash-1017", max_tokens=4096),
    instructions=[
        "Ти си асистент, помагащ на потребителя с всякакви готварски въпроси. Казваш се Манджев.",
        "Говориш като пълен селяндур само и единствено на български език.",
        "Въпреки това винаги си отзивчив и в помощ на потребителя.",
    ],
    db=SqliteDb(db_file="agent.db"),
    add_history_to_context=True,
    tools=[search_recipes, get_recipe],
)


if __name__ == "__main__":
    while prompt := input("Питай ма нещо: "):
        agent.print_response(prompt)
