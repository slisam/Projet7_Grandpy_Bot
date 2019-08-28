from flask import Flask, render_template, request, json
from classes import Parser, GoogleMaps, Wiki, GrandPyMessages




app = Flask(__name__, )

app.secret_key = "developmet-key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/_query", methods=['GET'])
def query():
    """Method to receive the query from the client side (input form) with AJAX
    and return all the objects needed in json to AJAX, after making instances
    and running the methods from classes.py."""

    # Getting the text the user type in the input form.
    user_text = request.args.get('text')
    # Parsing the user text.
    # Parser instance creation.
    user_request = Parser(user_text)

    # Running the parsing method.
    user_query = user_request.parsing()

    # GoogleMaps instance creation.
    query = GoogleMaps(user_query)
    print(user_query)
    # Find the address of the place looked for.
    try:
        # Running the coordinates method and retrieving latitude, longitude
        # and the global address of the place the user is looking for.
        address_coords = query.location()
        format_address = address_coords[0]
        latitude = address_coords[1]
        longitude = address_coords[2]
        # GrandPy Bot different possible messages in case of success.
        addressAnswer = GrandPyMessages.randomAnswer()
        # Find a story of the wanted place.
        try:
            # MediaWiki instance creation.
            coords = Wiki(latitude, longitude)
            # Running the history method to get the wikipedia page for that coordonates.
            wikiExtract = coords.comment()[0]
            pageid = coords.comment()[1]
            if wikiExtract:
                # GrandPy Bot different possible messages in case of success.
                storyAnswer = GrandPyMessages.randomStory()
            else:
                # GrandPy Bot different possible messages if there is no answer from Wikipedia.
                storyAnswer = GrandPyMessages.randomNoStory()
                # Reference this empty variable.
                wikiExtract = ''
                pageid = ''
        except:
            print("coucou")
            # GrandPy Bot different possible messages if there is no answer from Wikipedia.
            storyAnswer = GrandPyMessages.randomNoStory()
            # Reference this empty variable.
            wikiExtract = ''
            pageid = ''
    except:

        # GrandPy Bot different possible messages if there is no answer from GoogleMaps.
        addressAnswer = GrandPyMessages.randomNoAnswer()
        # Reference those empty variables.
        latitude = ''
        longitude = ''
        format_address = ''
        wikiExtract = ''
        storyAnswer = ''
        pageid = ''

    # JSON with the responses send back to AJAX (home.js).
    return json.dumps({'userText': user_text, \
        'addressAnswer': addressAnswer, \
        'lat':latitude, \
        'lng':longitude, \
        'format_address':format_address, \
        'storyAnswer': storyAnswer, \
        'wikiExtract': wikiExtract, \
        'pageid': pageid})


if __name__ == "__main__":
    app.run(debug=True)