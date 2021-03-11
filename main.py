from flask import Flask
import tetris

app = Flask(__name__)

@app.route("/")
def index():
    tetris.prep()
    tetris.menu()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug = True)
