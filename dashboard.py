from flask import Flask, render_template_string
import discord
import asyncio

app = Flask(__name__)

# 🧠 aqui você vai conectar com logs depois
tickets_fechados = []


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard de Tickets</title>
</head>
<body style="font-family: Arial; background:#111; color:white; padding:20px;">

    <h1>🎫 Dashboard de Tickets</h1>

    {% for t in tickets %}
        <div style="background:#222; padding:10px; margin:10px; border-radius:10px;">
            <h3>{{ t["titulo"] }}</h3>
            <p>👤 Fechado por: {{ t["user"] }}</p>
            <p>📅 Data: {{ t["data"] }}</p>
        </div>
    {% endfor %}

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML, tickets=tickets_fechados)


def add_ticket(title, user, data):
    tickets_fechados.append({
        "titulo": title,
        "user": user,
        "data": data
    })


if __name__ == "__main__":
    print("Dashboard rodando em http://127.0.0.1:5000")
    app.run(debug=True)