from flask import Flask, request, jsonify
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

app = Flask(__name__)

API_URL = "https://paid.proportalx.workers.dev/leak"
API_KEY = "ddos"

# Multi request handler
executor = ThreadPoolExecutor(max_workers=200)

# Request counter
today_used = 0


def fetch_data(query):

    global today_used

    try:

        response = requests.get(
            API_URL,
            params={
                "key": API_KEY,
                "query": query
            },
            timeout=30
        )

        raw = response.json()

        today_used += 1

        result = {
            "API_Developer": "@_keerthu__poojary_",
            "Today_Used": today_used,
            "result": {
                "query": query,
                "data": {
                    "source1": {
                        "records":
                            raw.get("result", {})
                               .get("data", {})
                               .get("source1", {})
                               .get("records", [])
                    }
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        }

        return result

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


@app.route("/")
def home():

    return jsonify({
        "status": "online",
        "server": "vercel",
        "multi_request": True,
        "workers": 200
    })


@app.route("/num")
def num():

    query = request.args.get("query")

    if not query:

        return jsonify({
            "success": False,
            "message": "Missing query parameter"
        })

    future = executor.submit(fetch_data, query)

    return jsonify(future.result())


@app.route("/aadhar")
def aadhar():

    query = request.args.get("query")

    if not query:

        return jsonify({
            "success": False,
            "message": "Missing query parameter"
        })

    future = executor.submit(fetch_data, query)

    return jsonify(future.result())


# Optional bulk API
@app.route("/bulk")
def bulk():

    queries = request.args.get("queries")

    if not queries:

        return jsonify({
            "success": False,
            "message": "Missing queries"
        })

    query_list = queries.split(",")

    futures = []

    for q in query_list:
        futures.append(executor.submit(fetch_data, q))

    results = []

    for future in futures:
        results.append(future.result())

    return jsonify({
        "success": True,
        "total": len(results),
        "results": results
    })


if __name__ == "__main__":
    app.run(threaded=True)
