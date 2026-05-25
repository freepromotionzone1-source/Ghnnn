# app.py

from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

API_URL = "https://paid.proportalx.workers.dev/leak"
API_KEY = "ddos"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Leak API Dashboard</title>

    <style>
        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
            font-family: monospace;
        }

        body{
            background:#050505;
            color:#00ff88;
            display:flex;
            justify-content:center;
            align-items:center;
            min-height:100vh;
        }

        .box{
            width:95%;
            max-width:700px;
            background:#0d0d0d;
            border:1px solid #00ff88;
            border-radius:15px;
            padding:25px;
            box-shadow:0 0 25px #00ff88;
        }

        h1{
            text-align:center;
            margin-bottom:20px;
            color:#00ff88;
        }

        .tabs{
            display:flex;
            gap:10px;
            margin-bottom:20px;
        }

        button{
            flex:1;
            padding:12px;
            border:none;
            background:#111;
            color:#00ff88;
            border:1px solid #00ff88;
            border-radius:10px;
            cursor:pointer;
            transition:0.3s;
        }

        button:hover{
            background:#00ff88;
            color:black;
        }

        input{
            width:100%;
            padding:14px;
            background:black;
            border:1px solid #00ff88;
            color:#00ff88;
            border-radius:10px;
            outline:none;
            margin-bottom:15px;
        }

        .search-btn{
            width:100%;
        }

        pre{
            margin-top:20px;
            background:black;
            padding:15px;
            border-radius:10px;
            overflow:auto;
            border:1px solid #00ff88;
            min-height:200px;
        }

        .footer{
            margin-top:15px;
            text-align:center;
            opacity:0.7;
        }
    </style>
</head>

<body>

<div class="box">

    <h1>⚡ Leak API Dashboard ⚡</h1>

    <div class="tabs">
        <button onclick="setType('num')">Number Info</button>
        <button onclick="setType('aadhar')">Aadhar Info</button>
    </div>

    <input type="text" id="query" placeholder="Enter Number / Aadhar">

    <button class="search-btn" onclick="searchData()">
        Search
    </button>

    <pre id="result">
Ready...
    </pre>

    <div class="footer">
        Flask + Vercel API
    </div>

</div>

<script>

let type = "num";

function setType(t){
    type = t;
}

async function searchData(){

    const query = document.getElementById("query").value;

    if(!query){
        alert("Enter query");
        return;
    }

    document.getElementById("result").innerText = "Loading...";

    try{

        const response = await fetch(`/${type}?query=${query}`);

        const data = await response.json();

        document.getElementById("result").innerText =
            JSON.stringify(data, null, 4);

    }catch(err){

        document.getElementById("result").innerText =
            err.toString();

    }

}

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/num")
def num():

    query = request.args.get("query")

    if not query:
        return jsonify({
            "success": False,
            "message": "Missing query"
        })

    try:

        response = requests.get(
            API_URL,
            params={
                "key": API_KEY,
                "query": query
            },
            timeout=30
        )

        data = response.json()

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route("/aadhar")
def aadhar():

    query = request.args.get("query")

    if not query:
        return jsonify({
            "success": False,
            "message": "Missing query"
        })

    try:

        response = requests.get(
            API_URL,
            params={
                "key": API_KEY,
                "query": query
            },
            timeout=30
        )

        data = response.json()

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)
