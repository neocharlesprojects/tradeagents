TradeAgents is an open-source framework for creating intelligent agents that simulate complex market dynamics. 

It combines economic principles with modern AI tools, enabling users to model decision-making, optimize outcomes, and explore market behaviors.

Key features include:

- Dynamic Market Simulations: Build and test agents in realistic market environments.
- AI Integration: Use large language models for parallel inference and adaptive decision-making.
- Customizable Memory System: Manage agent knowledge bases with a scalable and intuitive database layer.
- Modular Design: Easily extend, test, and deploy simulations with built-in tools and mock dependencies.


TradeAgents is perfect for developers, researchers, and enthusiasts looking to experiment with intelligent agent systems in competitive settings.

<p align="center">
  <img src="assets/tradeagents.jpeg" alt="Image Alt Text" width="80%" height="80%">
</p>

## Installation

To install the `trade_agents` package in editable mode, follow these steps:

1. Clone the repository:

    ```sh
    git clone https://github.com/tradeagents-ai/TradeAgents.git
    cd TradeAgents
    ```

2. Install the package in editable mode:

    ```sh
    pip install -e .
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Follow the README.md (just navigate to trade_agents/agents/db)
    ```sh
    cat ./trade_agents/agents/db/README.md
    ```

5. Make a copy of .env.example
    ```sh
    cp .env.example .env
    ```

    *Note: Setup API keys and more...*

7. Edit the ```trade_agents/orchestrator_config.yaml``` accoding to your configuration

## Running Examples

You can run the `run_simulation.sh` as follows:

```sh
sh trade_agents/run_simulation.sh
```

