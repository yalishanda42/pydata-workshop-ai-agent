from dotenv import load_dotenv

load_dotenv(override=True)

from agno.os import AgentOS

from agent import agent

agent_os = AgentOS(
    agents=[agent],
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="app:app", reload=True)
