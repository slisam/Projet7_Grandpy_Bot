import urllib.request

from classes import Parser, GoogleMaps, Wiki, GrandPyMessages


class TestParser:
    """ Parser test """
    #   - Controling the whole sentence parsing.
    def test_parser(self):
        """ Parse a resquest to test the parser"""
        test_user_request = Parser(
            "bonjour papy, pourrais-tu me dire où se trouve openclassrooms?"
        )
        assert test_user_request.parsing() == "openclassrooms"


class TestGoogleMaps:
    """ To mock the Google Maps Geocoding API """

    # - GoogleMaps Mock :
    #   - Query 1, that gives a result (latitude, longitude and global address).
    def test_http_google_return(self, monkeypatch):
        """To test the Google Maps Geocoding API by mocking the response
        and expecting the right result for 'openclassrooms'."""
        test_place = GoogleMaps("openclassrooms")
        results = {
            "results": [
                {
                    "formatted_address": "7 Cité Paradis, 75010 Paris, France",
                    "geometry": {"location": {"lat": 48.8748465, "lng": 2.3504873}},
                }
            ],
            "status": "OK",
        }

        def mockreturn():
            return results

        monkeypatch.setattr(urllib.request, "urlopen", mockreturn)
        assert test_place.location() == (
            results["results"][0]["formatted_address"],
            results["results"][0]["geometry"]["location"]["lat"],
            results["results"][0]["geometry"]["location"]["lng"],
        )


class TestWiki:
    """ To mock the Media Wiki API """

    # - Wiki Mock :
    #   - Charging the first two sentences, from the 'extract' of the wikipedia page related to the wanted place.
    def test_http_wiki_extract(self, monkeypatch):
        """To test a place, "musée d'orsay", with its latitude and longitude, that has a wikipedia page."""
        story = Wiki(48.8599614, 2.3265614)
        results = {
            "query": {
                "pages": [
                    {
                        "extract": "Le musée d’Orsay est un musée national inauguré en 1986, "
                        "situé dans le 7e arrondissement de Paris le long de la rive "
                        "gauche de la Seine. Il est installé dans l’ancienne gare d'Orsay, "
                        "construite par Victor Laloux de 1898 à 1900 et réaménagée en musée "
                        "sur décision du Président de la République Valéry Giscard d'Estaing."
                    }
                ]
            }
        }

        def mockreturn():
            return results

        monkeypatch.setattr(urllib.request, "urlopen", mockreturn)
        assert story.comment()[0] == results["query"]["pages"][0]["extract"]


class TestGrandPyMessages:
    """ To test the random messages. """

    # - Ramdom messages :
    #   - Controling GrandPy Bot answer.
    def test_randomAnswer(self):
        """To test that GrandPy Bot is answering the address."""
        address_answer = GrandPyMessages.randomAnswer()
        assert address_answer in GrandPyMessages.LISTANSWER

    #   - Controling GrandPy Bot no answer.
    def test_randomNoAnswer(self):
        """To test that GrandPy Bot is answering that he didn't understand the user query."""
        no_answer = GrandPyMessages.randomNoAnswer()
        assert no_answer in GrandPyMessages.LISTANOANSWER

    #   - Controling GrandPy Bot wikipedia story answer.
    def test_randomStory(self):
        """To test that GrandPy Bot is giving the wikipedia comment of the address."""
        story_answer = GrandPyMessages.randomStory()
        assert story_answer in GrandPyMessages.LISTWIKIPEDIA

    #   - Controling GrandPy Bot wikipedia no story.
    def test_randomNoStory(self):
        """To test that GrandPy Bot has no wikipedia story about the place."""
        no_story = GrandPyMessages.randomNoStory()
        assert no_story in GrandPyMessages.LISTNOWIKIPEDIA
