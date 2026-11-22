# PyData Sofia workshop 3.11.2026г.

На тема "Как да си направим първия AI агент".

Тук е кодът от семинара, който написахме.

Линк към клипа: [скоро](http://armenskipop.com)

## Какво има тук

Манджев е AI агент за готварски въпроси, направен с [Agno](https://github.com/agno-agi/agno). Търси рецепти в [gotvach.bg](https://recepti.gotvach.bg) и отговаря на български. Моделът се вика през [OpenRouter](https://openrouter.ai).

| Файл | Какво прави |
|---|---|
| `agent.py` | Агентът и двата му инструмента (`search_recipes`, `get_recipe`); пуска се като чат в терминала |
| `app.py` | Същият агент като уеб API с AgentOS на http://localhost:7777 |

## Инсталация

Нужни са ви:

- [git](https://git-scm.com)
- [uv](https://docs.astral.sh/uv/): сам ще свали Python 3.11, ако го нямате
- API ключ от [OpenRouter](https://openrouter.ai/keys)

### 1. Клонирайте репото

```bash
git clone https://github.com/yalishanda42/pydata-workshop-ai-agent
cd pydata-workshop-ai-agent
```

### 2. Инсталирайте зависимостите

```bash
uv sync
```

### 3. Добавете ключа си

Създайте файл `.env` в папката на проекта:

```
OPENROUTER_API_KEY=sk-or-...
```

`.env` е в `.gitignore`, така че ключът ви няма да попадне в git.

### 4. Пуснете агента

Чат в терминала:

```bash
uv run agent.py
```

Пишете въпроси; празен ред спира програмата.

Или като уеб API:

```bash
uv run app.py
```

Спира се с `Ctrl+C`.

Разговорите се пазят локално в `agent.db` (SQLite).
