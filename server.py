from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from csv import DictReader, DictWriter
from json import dumps as dumps

db = []
current_id = 3  # TODO get from last item in csv file
fieldnames = ["id", "title", "media", "description", "numerical", "external_link", "list"]

NEWEST_ITEMS = 10

app = Flask(__name__)


@app.route('/')
def go_to_home():
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
    print(dumps(newest, indent=2))
    return render_template("home.html", newest=newest)


@app.route('/search')
def go_to_search_results():
    pass

@app.route('/view/<id_str>')
def go_to_view(id_str=None):
    id_nbr = int(id_str)
    details = {}
    for item in db:  # TODO Use hashmap instead for efficiency.
        if int(item["id"]) == id_nbr:
            print("item[\"id\"]: " + item["id"])  # Debugging
            print("id_nbr: " + id_str)  # Debugging
            print(item)  # Debugging
            details = item
            break
    print(details)
    return render_template("view_details.html", details=details)

@app.route('/create')
def go_to_create_item():
    return render_template("create.html")


@app.route('/add_item', methods=['POST'])
def add_item():
    global current_id
    global db
    item_row = {}

    json_data = request.get_json()
    print(json_data)  # Debugging
    current_id += 1

    # Creating row to be stored
    for field_name in fieldnames:
        print(field_name)
        if field_name == "id":
            print("I am inside the id conditional statement")  # Debugging
            item_row[field_name] = current_id
        elif field_name == "list":
            print("I am inside the list conditional statement")  # Debugging
            item_row[field_name] = []
            item_row[field_name].append(json_data["list_elem"])
        elif field_name is None or json_data[field_name] is None:
            item_row[field_name] = None
        else:
            print("I am inside the else statement")  # Debugging
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

    db.append(item_row)

    new_link = "view/" + str(current_id)
    print(new_link)
    # send back the link to the new page so the client can be redirected there
    return jsonify(link=new_link)
    # return render_template("view_details.html", item_row=item_row)


if __name__ == '__main__':
    app.run(debug=True)
