from flask import Flask, render_template, request
from dotenv import load_dotenv
from json2html import *
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import os

# Flask app setup
app = Flask(__name__)
if __name__ == '__main__':
    app.run()

# Environment Variable Management
load_dotenv()
api_key = os.getenv('SUBGRAPH_API')
subgraph_endpoint = f'https://gateway.thegraph.com/api/{api_key}/subgraphs/id/ELUcwgpm14LKPLrBRuVvPvNKHQ9HvwmtKgKSH6123cr7'


# GraphQL Setup
transport = AIOHTTPTransport(
    url=subgraph_endpoint
)

client = Client(
    transport=transport,
    fetch_schema_from_transport=True,
)

def update_subgraph_query(input_number):
    subgraph_gql_query = gql(
                """
                {
                swaps(orderBy: amountInUSD, orderDirection: desc, first: replaceMe) {
                    amountInUSD
                    from
                    to
                    timestamp
                    tokenIn {
                    name
                    }
                    tokenOut {
                    name
                    }
                }
                }
            """.replace('replaceMe', input_number))
    return subgraph_gql_query

# Front-end Routing
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        swap_input_number_data = request.form["top_swap_count"]
        subgraph_gql_query_result = update_subgraph_query(swap_input_number_data)
        response = client.execute(subgraph_gql_query_result)
        json_table = json2html.convert(json = response)
        return render_template('index.html', json_table = json_table)

    else:
        return render_template('index.html')
