from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    Index route for home page
    :return: rendered index.html
    """
    return render_template("index.html")


def main():
    app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == '__main__':
    main()
