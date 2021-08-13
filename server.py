from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from csv import DictReader, DictWriter
from json import dumps as dumps
from copy import deepcopy as deepcopy

from mydatabase import MyDatabase as MyDatabase

# current_id = 12  # TODO get from last item in csv file
# fieldnames = ["id", "title", "format","media", "description", "numerical", "external_link", "list"]

NEWEST_ITEMS = 10

app = Flask(__name__)

db_file_path = "data.csv"
mdb = MyDatabase(db_file_path)
db: [dict] = mdb.load_basic_data()
current_id = mdb.get_newest_id()


@app.route('/')
def go_to_home():
    # TODO Explore a more efficient way of updating the data loaded in memory
    global db
    db.clear()
    db = mdb.load_basic_data()

    newest = db[- NEWEST_ITEMS:]
    # print(type(newest))  # Debugging
    # print(type(newest[0]))  # Debugging
    # print(type(dumps(newest)))  # Debugging
    # print(dumps(newest, indent=2))  # Debugging
    return render_template("home.html", newest=newest)


@app.route('/view/<id_str>')
def go_to_view(id_str=None):
    print("VIEW")
    global db
    id_nbr = int(id_str)
    details: dict = {}

    details = mdb.load_detailed_resource(id_nbr)
    print("item with id {}: {}".format(id_nbr, details))


    # print(type(details["list"]))  # Debugging
    # print(details["list"])  # Debugging
    details["list"] = dumps(details["list"])  # Dict to String
    # print(type(details["list"]))  # Debugging
    # print(details["list"])  # Debugging
    return render_template("view_details.html", details=details)


@app.route('/create')
def go_to_create_item():
    return render_template("create.html")


@app.route('/add_item', methods=['POST'])
def add_item():
    print("ADD ITEM")

    json_data = request.get_json()
    # print("json_data: {}".format(json_data))  # Debugging

    new_id = mdb.add_resource(json_data)

    # Provides the link to the new page so the client can be redirected there
    new_link = "view/" + str(new_id)

    return jsonify(link=new_link)


@app.route('/search/<search_str>', methods=['GET'])
def search(search_str=None):

    title_results, content_results = mdb.search_for_string(search_str)

    return render_template("search_results.html", search_str=search_str,
                           title_results=title_results, content_results=content_results)


@app.route('/auto/<fragment_str>')
def provide_autocomplete(fragment_str=None):
    search_results = []
    for item in db:
        if fragment_str in item["title"].lower() or fragment_str in item["description"].lower():
            search_results.append(item["title"])

    print(search_results)
    return jsonify(search_results=search_results)


if __name__ == '__main__':
    app.run(debug=True)
