from typing import List, Dict, Tuple
from pydantic import BaseModel,computed_field
import matplotlib.pyplot as plt
import logging
import random
from trade_agents.economics.econ_agent import EconomicAgent, ZiFactory, ZiParams
from trade_agents.economics.econ_models import Trade
from functools import cached_property
# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class EquilibriumResults(BaseModel):
    price: float
    quantity: int
    buyer_surplus: float
    seller_surplus: float
    total_surplus: float
    good_name: str

class Equilibrium(BaseModel):
    agents: List[EconomicAgent]
    goods: List[str]

    def calculate_equilibrium(self) -> Dict[str, EquilibriumResults]:
        equilibria = {}
        for good in self.goods:
            logger.info(f"Calculating equilibrium for {good}")
            demand_prices, supply_prices = self._aggregate_curves(good)
            equilibrium_price, equilibrium_quantity = self._find_intersection(demand_prices, supply_prices)
            equilibria[good]=EquilibriumResults(
                price=equilibrium_price,
                quantity=equilibrium_quantity,
                buyer_surplus=self._calculate_surplus(demand_prices, equilibrium_price, equilibrium_quantity, is_buyer=True),
                seller_surplus=self._calculate_surplus(supply_prices, equilibrium_price, equilibrium_quantity, is_buyer=False),
                total_surplus=self._calculate_surplus(demand_prices, equilibrium_price, equilibrium_quantity, is_buyer=True) + self._calculate_surplus(supply_prices, equilibrium_price, equilibrium_quantity, is_buyer=False),
                good_name=good
            )  
        return equilibria
    
    @computed_field
    @cached_property
    def equilibrium(self) -> Dict[str, EquilibriumResults]:
        return self.calculate_equilibrium()
    


    def _aggregate_curves(self, good: str) -> Tuple[List[float], List[float]]:
        demand_prices = []
        supply_prices = []

        # Aggregate demand
        for agent in self.agents:
            if agent.is_buyer(good):
                schedule = agent.value_schedules[good]
                for quantity in range(1, schedule.num_units + 1):
                    value = schedule.get_value(quantity)
                    demand_prices.append(value)

        # Aggregate supply
        for agent in self.agents:
            if agent.is_seller(good):
                schedule = agent.cost_schedules[good]
                for quantity in range(1, schedule.num_units + 1):
                    cost = schedule.get_value(quantity)
                    supply_prices.append(cost)

        # Sort the marginal values and costs
        demand_prices.sort(reverse=True)
        supply_prices.sort()
        logger.debug(f"Aggregated demand prices for {good}: {demand_prices}")
        logger.debug(f"Aggregated supply prices for {good}: {supply_prices}")
        return demand_prices, supply_prices

    def _find_intersection(self, demand_prices: List[float], supply_prices: List[float]) -> Tuple[float, int]:
        # Find the quantity where demand price >= supply price
        quantity = 0
        max_quantity = min(len(demand_prices), len(supply_prices))
        for i in range(max_quantity):
            demand_price = demand_prices[i]
            supply_price = supply_prices[i]
            logger.debug(f"At quantity {i+1}: demand_price={demand_price}, supply_price={supply_price}")
            if demand_price >= supply_price:
                quantity += 1
            else:
                break
        if quantity == 0:
            logger.info("No equilibrium found")
            return 0, 0
        equilibrium_price = (demand_prices[quantity - 1] + supply_prices[quantity - 1]) / 2
        logger.info(f"Equilibrium found at price {equilibrium_price} with quantity {quantity}")
        return equilibrium_price, quantity

    def _calculate_surplus(self, prices: List[float], price: float, quantity: int, is_buyer: bool) -> float:
        surplus = 0.0
        for i in range(quantity):
            value = prices[i]
            if is_buyer:
                surplus += value - price
            else:
                surplus += price - value
        return surplus

    def plot_supply_demand(self, good: str):
        demand_prices, supply_prices = self._aggregate_curves(good)

        # Build cumulative quantities for demand and supply
        demand_quantities = [i for i in range(len(demand_prices) + 1)]
        supply_quantities = [i for i in range(len(supply_prices) + 1)]

        # Adjust prices for plotting
        demand_prices_plot = [demand_prices[0]] + demand_prices
        supply_prices_plot = [supply_prices[0]] + supply_prices

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot demand and supply curves using 'steps-pre'
        ax.step(demand_quantities, demand_prices_plot, where='pre', label='Aggregate Demand', color='blue')
        ax.step(supply_quantities, supply_prices_plot, where='pre', label='Aggregate Supply', color='red')

        # Plot equilibrium point
        equilibrium = self.equilibrium[good]
        equilibrium_quantity = equilibrium.quantity
        equilibrium_price = equilibrium.price

        ax.plot([equilibrium_quantity], [equilibrium_price], 'go', label='Equilibrium')

        ax.set_title(f'Aggregate Supply and Demand Curves for {good}')
        ax.set_xlabel('Quantity')
        ax.set_ylabel('Price')
        ax.legend()
        ax.grid(True)
        
        return fig  # Return the figure object

if __name__ == "__main__":
    # Set up logging for the main script
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Define parameters
    num_buyers = 10
    num_sellers = 10
    num_units_per_agent = 10
    goods = ["apple"]
    
    # Create ZiParams for buyers and sellers
    buyer_params = ZiParams(
        id="buyer_template",
        initial_cash=1000,
        initial_goods={"apple": 0},
        base_values={"apple": 100},
        num_units=num_units_per_agent,
        noise_factor=0.1,
        max_relative_spread=0.2,
        is_buyer=True
    )
    
    seller_params = ZiParams(
        id="seller_template",
        initial_cash=0,
        initial_goods={"apple": num_units_per_agent},
        base_values={"apple": 80},
        num_units=num_units_per_agent,
        noise_factor=0.1,
        max_relative_spread=0.2,
        is_buyer=False
    )
    
    # Create ZiFactories for buyers and sellers
    buyer_factory = ZiFactory(
        id="buyer_factory",
        goods=goods,
        num_buyers=num_buyers,
        num_sellers=0,
        buyer_params=buyer_params,
        seller_params=seller_params  # This won't be used but is required by the ZiFactory
    )
    
    seller_factory = ZiFactory(
        id="seller_factory",
        goods=goods,
        num_buyers=0,
        num_sellers=num_sellers,
        buyer_params=buyer_params,  # This won't be used but is required by the ZiFactory
        seller_params=seller_params
    )
    
    # Get all agents from the factories
    all_agents = buyer_factory.agents + seller_factory.agents
    
    # Create the Equilibrium object
    equilibrium = Equilibrium(agents=all_agents, goods=goods)
    
    # Calculate and print the theoretical equilibrium
    result = equilibrium.calculate_equilibrium()
    print("Theoretical Equilibrium Results:")
    for good, data in result.items():
        print(f"\nGood: {good}")
        dumped_data = data.model_dump() 
        for key, value in dumped_data.items():
            print(f"  {key}: {value}")
    theoretical_total_surplus = sum(dumped_data['total_surplus'] for data in result.values())
    print(f"\nTheoretical Total Surplus: {theoretical_total_surplus:.2f}")
    
    # Plot the supply and demand curves
    fig = equilibrium.plot_supply_demand("apple")
    plt.show()
    
    # Simulate the market trading process
    print("\nSimulating market trading...")
    trades = []
    trade_id = 1
    max_rounds = 1000  # Number of trading rounds
    for round_num in range(max_rounds):
        # Collect bids and asks from agents
        bids = []
        asks = []
        for agent in all_agents:
            for good in goods:
                bid = agent.generate_bid(good)
                if bid:
                    bids.append((agent, bid))
                ask = agent.generate_ask(good)
                if ask:
                    asks.append((agent, ask))
        
        # Sort bids and asks by price
        bids.sort(key=lambda x: x[1].price, reverse=True)  # Highest bids first
        asks.sort(key=lambda x: x[1].price)  # Lowest asks first
        
        # Attempt to match bids and asks
        while bids and asks:
            highest_bidder, highest_bid = bids[0]
            lowest_asker, lowest_ask = asks[0]
            if highest_bid.price >= lowest_ask.price:
                # Execute trade
                trade_price = (highest_bid.price + lowest_ask.price) / 2
                trade = Trade(
                    trade_id=trade_id,
                    buyer_id=highest_bidder.id,
                    seller_id=lowest_asker.id,
                    price=trade_price,
                    quantity=1,
                    good_name=good,
                    ask_price=lowest_ask.price,
                    bid_price=highest_bid.price
                )
                # Process trade for both buyer and seller
                buyer_success = highest_bidder.process_trade(trade)
                seller_success = lowest_asker.process_trade(trade)
                if buyer_success and seller_success:
                    trades.append(trade)
                    trade_id += 1
                    # Remove the bid and ask since they have been fulfilled
                    bids.pop(0)
                    asks.pop(0)
                else:
                    # If trade was not successful, remove the bid/ask and continue
                    bids.pop(0)
                    asks.pop(0)
            else:
                # No more matches possible in this round
                break
    
    # After trading rounds, compute the empirical surplus
    print("\nComputing empirical surplus...")
    total_buyer_surplus = sum(agent.calculate_individual_surplus() for agent in buyer_factory.agents)
    total_seller_surplus = sum(agent.calculate_individual_surplus() for agent in seller_factory.agents)
    total_empirical_surplus = total_buyer_surplus + total_seller_surplus
    print(f"Total Empirical Buyer Surplus: {total_buyer_surplus:.2f}")
    print(f"Total Empirical Seller Surplus: {total_seller_surplus:.2f}")
    print(f"Total Empirical Surplus: {total_empirical_surplus:.2f}")
    
    # Compute and print the empirical efficiency (% of theoretical surplus achieved)
    efficiency = (total_empirical_surplus / theoretical_total_surplus) * 100 if theoretical_total_surplus > 0 else 0
    print(f"\nEmpirical Efficiency: {efficiency:.2f}%")

