from flask import Flask, render_template, request
from dotenv import load_dotenv
from json2html import *
import requests
import json
import os

app = Flask(__name__)
if __name__ == '__main__':
    app.run()

def update_query(input_number): 
    query = """
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
    """.replace('replaceMe', input_number)
    return query

# subgraph_endpoint = 'https://gateway.thegraph.com/api/[api-key]/subgraphs/id/ELUcwgpm14LKPLrBRuVvPvNKHQ9HvwmtKgKSH6123cr7'

# Environment Variable Management
load_dotenv()
api_key = os.getenv('SUBGRAPH_API')
subgraph_endpoint = f'https://gateway.thegraph.com/api/{api_key}/subgraphs/id/ELUcwgpm14LKPLrBRuVvPvNKHQ9HvwmtKgKSH6123cr7'


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        swapInputNumberData = request.form["top_swap_count"]
        query = update_query(swapInputNumberData)
        response = requests.post(url=subgraph_endpoint, json={"query": query})
        print(response)
        formatted_subgraph_json = json.loads(response.content)
        json_table = json2html.convert(json = formatted_subgraph_json)
       
        if response.status_code == 200:
            return render_template('index.html', json_table = json_table)


    else:
        return render_template('index.html')
