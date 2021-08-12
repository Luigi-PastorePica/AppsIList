from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from csv import DictReader, DictWriter
from json import dumps as dumps
from copy import deepcopy as deepcopy

from mydatabase import MyDatabase as MyDatabase

# db: list = []
current_id = 12  # TODO get from last item in csv file
fieldnames = ["id", "title", "media", "description", "numerical", "external_link", "list"]

NEWEST_ITEMS = 10

app = Flask(__name__)


# # Load entries in "database" into memory
# def load_data():
#     with open("data.csv", "r") as csvfile:
#         reader = DictReader(csvfile)
#         for row in reader:
#             row["list"] = eval(row["list"])  # String to Dict
#             db.append(row)

db_file_path = "data.csv"
mdb = MyDatabase(db_file_path)
db: list = mdb.load_data()


@app.route('/')
def go_to_home():
    # TODO Explore a more efficient way of updating the data loaded in memory
    global db
    db.clear()
    db = mdb.load_data()

    # with open("data.csv", "r") as csvfile:
    #     reader = DictReader(csvfile)
    #     for row in reader:
    #         row["list"] = eval(row["list"])  # String to Dict
    #         db.append(row)
    newest = db[- NEWEST_ITEMS:]
    # print(type(newest))
    # print(type(newest[0]))
    # print(type(dumps(newest)))
    # print(dumps(newest, indent=2))
    return render_template("home.html", newest=newest)


@app.route('/view/<id_str>')
def go_to_view(id_str=None):
    print("VIEW")
    global db
    id_nbr = int(id_str)
    details = {}
    for item in db:  # TODO Use hashmap or another search method instead for efficiency.
        if int(item["id"]) == id_nbr:
            # print("item[\"id\"]: " + item["id"])  # Debugging
            # print("id_nbr: " + id_str)  # Debugging
            # print(item)  # Debugging
            details = deepcopy(item)
            break
    # TODO Last time I left here
    # for review in details["list"]:

    print(type(details["list"]))  # Debugging
    print(details["list"])  # Debugging
    details["list"] = dumps(details["list"])  # Dict to String
    print(type(details["list"]))  # Debugging
    print(details["list"])  # Debugging
    return render_template("view_details.html", details=details)

@app.route('/create')
def go_to_create_item():
    return render_template("create.html")


@app.route('/add_item', methods=['POST'])
def add_item():
    print("ADD ITEM")
    global current_id
    global db
    item_row = {}

    json_data = request.get_json()
    # print(json_data)  # Debugging
    current_id += 1

    # Creating row to be stored
    for field_name in fieldnames:
        # print(field_name)
        if field_name == "id":
            # print("I am inside the id conditional statement")  # Debugging
            item_row[field_name] = current_id
        elif field_name == "list":
            # print("I am inside the list conditional statement")  # Debugging
            print(type(json_data["list_elem"]))
            print(json_data["list_elem"])
            print(dumps(json_data["list_elem"]))
            user_id = json_data["list_elem"].keys();
            # Using string instead of boolean simplifies storage and retrieval from a csv file
            json_data["list_elem"][list(user_id)[0]]["mark_as_deleted"] = "False"
            item_row[field_name] = dumps(json_data["list_elem"])  # Dict to String
        elif field_name is None or json_data[field_name] is None:
            item_row[field_name] = None
        else:
            # print("I am inside the else statement")  # Debugging
            item_row[field_name] = json_data[field_name]

    try:
        with open("data.csv", "a") as csvfile:
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(item_row)
    except FileNotFoundError as e:
        print(e, "Creating new file")
        with open("data.csv", "w") as output_file:
            writer = DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(item_row)
    except Exception as e:
        current_id -= 1
        # TODO return something that tells the user the record could not be created
        raise e
    print("APPEND TO DB")
    # db.append(item_row) # NOOO this is the thing that is causing inconsistencies.
    print(type(item_row["list"]))
    print(item_row["list"])
    item_row["list"] = eval(item_row["list"])
    db.append(item_row)
    print(type(item_row["list"]))
    print(item_row["list"])

    # try:
    #     print(type(item_row["list"]))
    #     print(item_row["list"])
    #     item_row["list"] = eval(item_row["list"])
    #     db.append(item_row)
    #     print(type(item_row["list"]))
    #     print(item_row["list"])
    # except NameError as e:
    #     if
    new_link = "view/" + str(current_id)
    # print(new_link)  # Debugging
    # send back the link to the new page so the client can be redirected there
    return jsonify(link=new_link)


@app.route('/search/<search_str>', methods=['GET'])
def search(search_str=None):

    print(search_str)  # Debugging

    search_str_lower = search_str.lower()
    title_results = []
    content_results = []
    for item in db:
        if search_str_lower in item["title"].lower():
            title_results.append(item)
        elif search_str_lower in item["description"].lower():
            content_results.append(item)

    print(title_results)  # Debugging
    print(content_results)  # Debugging

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
