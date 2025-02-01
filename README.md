# TradeAgents

TradeAgents is an open-source framework for creating intelligent agents that simulate complex market dynamics. It combines economic principles with modern AI tools, enabling users to model decision-making, optimize outcomes, and explore market behaviors.

<p align="center">
  <img src="assets/tradeagents.jpg" alt="Image Alt Text" width="80%" height="80%">
</p>

## Key Features

- **Dynamic Market Simulations**: Build and test agents in realistic market environments.
- **AI Integration**: Use large language models for parallel inference and adaptive decision-making.
- **Customizable Memory System**: Manage agent knowledge bases with a scalable and intuitive database layer.
- **Modular Design**: Easily extend, test, and deploy simulations with built-in tools and mock dependencies.

TradeAgents is perfect for developers, researchers, and enthusiasts looking to experiment with intelligent agent systems in competitive settings.

<p align="center">
  <img src="assets/tradeagents.jpg" alt="TradeAgents Simulation" width="80%" height="80%">
</p>

---

## Installation

To install the `trade_agents` package in editable mode, follow these steps:

### Prerequisites

- Python 3.8+
- `pip` (latest version recommended)
- PostgreSQL (if using a database-backed agent system)
- API keys for AI integrations (e.g., OpenAI, Anthropic)

### Step-by-Step Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/tradeagents-ai/TradeAgents.git
    cd TradeAgents
    ```

2. **Install the package in editable mode:**

    ```sh
    pip install -e .
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Initialize database (if applicable):**

    If using PostgreSQL, ensure it is running and configure your `.env` file accordingly.

5. **Follow additional setup instructions:**

    ```sh
    cat ./trade_agents/agents/db/README.md
    ```

6. **Copy and configure the environment file:**

    ```sh
    cp .env.example .env
    ```

    *Modify the `.env` file with your API keys, database credentials, and other settings.*

7. **Modify the orchestrator configuration:**

    ```sh
    nano trade_agents/orchestrator_config.yaml
    ```

    Adjust settings according to your desired simulation parameters.

---

## Running Simulations

TradeAgents provides a shell script for running pre-configured simulations.

To run the default simulation, execute:

```sh
sh trade_agents/run_simulation.sh
```

Alternatively, run simulations manually via Python:

```sh
python trade_agents/main.py --config configs/default.yaml
```

Modify the configuration file to experiment with different parameters.

---

## Usage Examples

### Running a Simple Agent

You can start a simple agent instance using:

```python
from trade_agents.agents import Agent

def main():
    agent = Agent(name="TraderAI", strategy="mean_reversion")
    agent.run()

if __name__ == "__main__":
    main()
```

### API Usage (FastAPI)

TradeAgents exposes an API for external interactions. Run the FastAPI server:

```sh
uvicorn trade_agents.api:app --host 0.0.0.0 --port 8000
```

Then, visit `http://localhost:8000/docs` for interactive API documentation.

---

## Dependencies

TradeAgents requires the following libraries:

- `pydantic==2.8.2`
- `pydantic-settings==2.5.2`
- `psycopg2==2.9.10`
- `anthropic==0.34.1`
- `openai==1.42.0`
- `python-dotenv==1.0.1`
- `colorama==0.4.6`
- `names==0.3.0`
- `tiktoken==0.7.0`
- `fastapi==0.115.6`
- `pyfiglet==1.0.2`
- `uvicorn==0.34.0`
- `rich==13.9.4`
- `aiohttp`

Install missing dependencies with:

```sh
pip install -r requirements.txt
```

---

## Troubleshooting

### 1. Missing API Keys

- Ensure that `.env` contains valid API keys for OpenAI or Anthropic.

### 2. Database Connection Issues

- Verify that PostgreSQL is running and credentials in `.env` are correct.

### 3. Dependency Conflicts

- Run:
    ```sh
    pip check
    ```
    and reinstall conflicting packages.

---

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and test them.
4. Submit a pull request.

For detailed guidelines, see `CONTRIBUTING.md`.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## Contact

For issues and discussions, open a GitHub issue or contact the maintainers at [GitHub Issues](https://github.com/tradeagents-ai/TradeAgents/issues).

Happy trading!



```

