from flask import Flask, render_template, request
from prompter import call_chatgpt

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        code = request.form.get("code")
        chat_response = call_chatgpt(code)
        return render_template("index.html", chat_response=chat_response)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
