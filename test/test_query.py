import requests


your_query=input("Enter your query: ")

query = {
    "question":  your_query,
}

res = requests.post("http://localhost:8000/ask", json=query)

if res.status_code == 200:
    print(" Answer:\n", res.json()["answer"])
else:
    print(" Error:", res.text)
