from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from csv import DictReader, DictWriter
from json import dumps as dumps

db = []

NEWEST_ITEMS = 10

app = Flask(__name__)

@app.route('/')
def go_to_home():
    newest = []
    # Load entries in "database" into memory
    db.clear()
    with open("data.csv", "r") as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            db.append(row)
    newest = db[- NEWEST_ITEMS:]
    print(type(newest))
    print(type(newest[0]))
    print(type(dumps(newest)))
    print(newest)
    return render_template("home.html", newest=newest)


@app.route('/search')
def go_to_search_results():
    pass


@app.route('/create')
def go_to_create_item():
    return render_template("create.html")


if __name__ == '__main__':
    app.run(debug=True)
