from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os
from functools import lru_cache
import time

app = Flask(__name__)

API_URL = "https://paid.proportalx.workers.dev/leak"
API_KEY = "ddos"

# Use a simple counter with file storage for persistence (optional)
COUNTER_FILE = "/tmp/counter.txt"

def get_today_used():
    """Thread-safe counter using file storage"""
    try:
        if os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, 'r') as f:
                return int(f.read().strip())
    except:
        pass
    return 0

def increment_counter():
    """Increment the counter"""
    try:
        current = get_today_used()
        with open(COUNTER_FILE, 'w') as f:
            f.write(str(current + 1))
        return current + 1
    except:
        return 0

def fetch_data(query):
    """Fetch data from external API"""
    try:
        response = requests.get(
            API_URL,
            params={
                "key": API_KEY,
                "query": query
            },
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        
        # Check if response is valid
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API returned status {response.status_code}"
            }
        
        raw = response.json()
        
        # Increment counter
        today_count = increment_counter()
        
        # Extract data safely
        result_data = raw.get("result", {})
        if isinstance(result_data, dict):
            data_section = result_data.get("data", {})
            if isinstance(data_section, dict):
                source1 = data_section.get("source1", {})
                if isinstance(source1, dict):
                    records = source1.get("records", [])
                else:
                    records = []
            else:
                records = []
        else:
            records = []
        
        result = {
            "API_Developer": "@_keerthu__poojary_",
            "Today_Used": today_count,
            "result": {
                "query": query,
                "data": {
                    "source1": {
                        "records": records
                    }
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        return {
            "success": True,
            "data": result
        }
        
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timeout"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Network error: {str(e)}"
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Invalid JSON response: {str(e)}"
        }
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
        "multi_request": False,  # Vercel doesn't support multi-threading well
        "workers": 1,
        "endpoints": ["/num", "/aadhar", "/bulk"]
    })


@app.route("/num")
def num():
    query = request.args.get("query")
    
    if not query:
        return jsonify({
            "success": False,
            "message": "Missing query parameter"
        }), 400
    
    result = fetch_data(query)
    return jsonify(result)


@app.route("/aadhar")
def aadhar():
    query = request.args.get("query")
    
    if not query:
        return jsonify({
            "success": False,
            "message": "Missing query parameter"
        }), 400
    
    result = fetch_data(query)
    return jsonify(result)


@app.route("/bulk")
def bulk():
    queries = request.args.get("queries")
    
    if not queries:
        return jsonify({
            "success": False,
            "message": "Missing queries parameter"
        }), 400
    
    query_list = [q.strip() for q in queries.split(",") if q.strip()]
    
    if not query_list:
        return jsonify({
            "success": False,
            "message": "No valid queries provided"
        }), 400
    
    # Process sequentially (Vercel-friendly)
    results = []
    for q in query_list[:10]:  # Limit to 10 queries to avoid timeout
        results.append(fetch_data(q))
    
    return jsonify({
        "success": True,
        "total": len(results),
        "results": results
    })


# Health check endpoint for Vercel
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
