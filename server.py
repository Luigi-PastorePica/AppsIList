from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from json import dumps as dumps

from mydatabase import MyDatabase as MyDatabase


NEWEST_ITEMS = 10

app = Flask(__name__)

db_file_path = "data.csv"
mdb = MyDatabase(db_file_path)
db: [dict] = mdb.load_basic_data()
# current_id = mdb.get_newest_id()


@app.route('/')
def go_to_home():
    """
    Prepares and displays the landing/home page. It displays at most the NEWEST_ITEMS number of entries.\

    :return: Renders the home page.
    """

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
    """
    Display the details page for the resource with identifier equal to the integer representation of id_str.

    :param id_str: A string representing the unique identifier of a resource stored in the database.
    :return: Renders the item detail view for the resource with id equal to the integer value of id_str.
    """
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
    """
    Displays the page with the form to add a new resource to the database.

    :return: Render the page with the form to add a new resource to the database.
    """
    return render_template("create.html")


@app.route('/add_item', methods=['POST'])
def add_item():
    """
    Sends request to add new entry in the database.

    :return: A string containing the link to the details page of the newly created resource.
    """

    print("ADD ITEM") # Debugging

    json_data = request.get_json()
    # print("json_data: {}".format(json_data))  # Debugging

    new_id = mdb.add_resource(json_data)

    # Provides the link to the new page so the client can be redirected there
    new_link = "view/" + str(new_id)

    return jsonify(link=new_link)


@app.route('/search/<search_str>', methods=['GET'])
def search(search_str=None):
    """
    Searches for the given string in all entries in the database

    :param search_str: The string containing the word or word fragment to search for.
    :return: Display the search results page.
    """

    title_results, content_results = mdb.search_for_string(search_str)

    return render_template("search_results.html", search_str=search_str,
                           title_results=title_results, content_results=content_results)


@app.route('/auto/<fragment_str>')
def provide_autocomplete(fragment_str=None):
    """
    Provide autocomplete for the search functionality. Not in use yet.
    :param fragment_str: A string containing the partially written search term.
    :return: A JSON formatted search results list.
    """
    search_results = []
    for item in db:
        if fragment_str in item["title"].lower() or fragment_str in item["description"].lower():
            search_results.append(item["title"])

    print(search_results)
    return jsonify(search_results=search_results)


if __name__ == '__main__':
    app.run(debug=True)
