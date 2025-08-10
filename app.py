from flask import Flask, request, redirect
import json
from pathlib import Path

app = Flask(__name__)
DB = Path("todo.json")

def load():
    return json.loads(DB.read_text(encoding="utf-8")) if DB.exists() else []

def save(items):
    DB.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

@app.get("/")
def index():
    items = load()
    lis = "".join(f"<li>{'[x]' if t['done'] else '[ ]'} {t['title']}</li>" for t in items)
    form = """
      <form action="/add" method="post" style="margin-top:12px">
        <input name="title" placeholder="やること" autofocus>
        <button>追加</button>
      </form>
    """
    return f"<h1>ToDo</h1><ul>{lis}</ul>{form}"

@app.post("/add")
def add():
    items = load()
    title = request.form.get("title", "").strip()
    if title:
        items.append({"title": title, "done": False})
        save(items)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
