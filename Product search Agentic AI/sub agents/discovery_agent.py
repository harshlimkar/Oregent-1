from crewai import Agent
from apis.flipkart_api import search_flipkart_api
from apis.amazon_api import search_amazon_api
from apis.myntra_api import search_myntra_api
from apis.meesho_api import search_meesho_api
from discovery.search_engine import search_engine_discovery

def discover_products(query):
    products = []

    for api in [
        search_flipkart_api,
        search_amazon_api,
        search_myntra_api,
        search_meesho_api
    ]:
        try:
            products += api(query)
        except:
            pass

    if not products:
        products = search_engine_discovery(query)

    return products

discovery_agent = Agent(
    role="Product Discovery Agent",
    goal="Find real product pages using APIs or fallback methods",
    backstory="Expert in product discovery across ecommerce platforms",
    allow_delegation=False,
    verbose=True,
    function_call=discover_products
)
