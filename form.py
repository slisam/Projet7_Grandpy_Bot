from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import requests
import random
import re



STOPWORDS = ['là', 'flac', 'étante', 'ceux', 'celle-ci', 'eus', 'que', 'ce', 'peut', 'selon', 'tous', 'hop', 'possibles', 'tenir', 'quant-à-soi', 'sur', 'anterieur', 'chères', 'relativement', 'jusque', 'pfut', 'holà', 'fûmes', 'apres', 'quarante', 'e', 'quatorze', 'sienne', 'différentes', 'ta', 'soi', 'afin', 'na', 'doivent', 'avec', 'unique', 'beaucoup', 'du', 'probante', 'papy', 'pan', 'moyennant', 'certaine', 'sous', 'pas', 'vif', 'naturelle', 'revoici', 'pourrait', 'rarement', 'quelconque', 'elle-même', 'hors', 'nul', 'k', 'donne', 'celle', 'hue', 'hep', 'eussiez', 'aussi', 'possessif', 'gens', 'vé', 'exactement', 'desormais', 'serait', 'chacun', 'semblable', 'ceci', 'soient', 'uniques', 'douzième', 'jusqu', 'étées', 'eux', 'nôtres', 'partant', 'dessus', 'aurions', 'trois', 'alors', 'serons', 'puis', 'vas', 'fûtes', 'autrui', 'sait', 'bas', 'pouvait', 'celui-ci', 'certains', 'tsoin', 'sauf', 'couic', 'eussent', 'x', 'zut', 'auront', 'celles-ci', 'troisièmement', 'seraient', 'attendu', 'vont', 'était', 'certain', 'celle-là', 'dix-huit', 'doit', 'etc', 'euh', 'dix-neuf', 'va', 'hurrah', 'cet', 'eue', 'plouf', 'deuxième', 'soyons', 'furent', 'extenso', 'brrr', 'le', 'pfft', 'revoilà', 'vôtre', 'votre', 'dix-sept', 'suis', 'serais', 'pourrais', 'autrement', 'eux-mêmes', "s'il te plait", 'ouias', 'miennes', 'vous-mêmes', 'fait', 'r', 'donner', 'derriere', 'hi', 'egalement', 'sans', 'floc', 'ci', 'moindres', 'neanmoins', 'allô', 'eûmes', 'effet', 'specifiques', 'v', 'vive', 'quatrièmement', 'ayez', 'eh', 'tiens', 'après', 'lui', 'possible', 'soyez', 'dixième', 'd', 'hélas', 'ils', 'ma', 'pff', 'dix', 'peu', 'allo', 'multiples', 'avoir', 'hé', 'plutôt', 'rare', 'mes', 'ainsi', 'bot', 'vos', 'cinquantième', 'o|', 'trop', 'pure', 'tu', 'ai', 'cinquante', 'bah', "quelqu'un", 'relative', 'particulière', 'desquels', 'sent', 'egales', 'speculatif', 'qu', 'faisaient', 'aupres', 'deuxièmement', 'très', 'differents', 'on', 'bye', 'vais', 'mêmes', 'différente', 'environ', 'p', 'auxquels', 'si', 'mince', 'étiez', 'miens', 'semblaient', 'aie', 'nombreuses', 'serai', 'laisser', 'quoi', 'même', 'comparable', 'h', 'onze', 'être', 'fut', 'restrictif', 'douze', 'avons', 'avaient', 'feront', 'se', 'fusses', 'ceux-ci', 'maximale', 'quoique', 'contre', 'quatrième', 'eues', 'aucun', 'veux', 'désormais', 'entre', 'parlent', 'elles', 'étaient', 'clic', 'divers', 'auriez', 'particulier', 'celui-là', 'anterieure', 'chaque', 'dès', 'b', 'cinquième', 'olé', 'sais', 'encore', 'specifique', 'aujourd', 'car', 'première', 'quinze', 'mon', 'pire', 'vers', 'touchant', 'lesquels', 'delà', 'malgre', 'seulement', 'aura', 'via', 'eusse', 'surtout', 'combien', 'ayantes', 'parle', 'trouve', 'ayons', 'tiennes', 'vous', 'il', 'basee', 'tels', 'maint', 'êtes', 'recherche', 'salut', 'pif', 'connais', 'abord', 'dedans', 'dont', 'suivant', 'plus', 'g', 'fût', 'à', 'voici', 'aurez', 'ses', 'vingt', 'aurait', 'avez', 'ton', 'cherche', 'chère', 'étions', 'lui-même', 'ayants', 'differentes', 'parce', 'stop', 'cher', 'dehors', 'u', 'cependant', 'plein', 'lui-meme', 'oust', 'bravo', 'permet', 'étants', 'seras', 'durant', 'trente', 'un', 'n', 'bien', 'sapristi', 'ceux-là', 'juste', 'par', 'avais', 'où', 'sommes', 'toutes', 'prealable', 'eût', 'est-ce', 'dernier', 'comment', 'parmi', 'rien', 'té', 'quatre', 'tac', 'malgré', 'devant', 'concernant', 'naturel', 'paf', 'nombreux', 'desquelles', 'lequel', 'l', 'septième', 'différent', 'ore', 'sont', 'tres', 'dits', 'rendre', 'z', 'une', 'quel', 'huit', 'ollé', 'tardive', 'son', 'sois', 'debout', 'egale', 'â', 'ouvert', 'uniformement', 'uns', 'notamment', 'non', 'comparables', 'retour', 'personne', 'bat', 'tout', 'tenant', 'restant', 'probable', 'trouver', 'procedant', 'tic', 'semble', 'vives', 'ces', 'premier', 'i', 'pendant', 'hui', 'tend', 'pour', 'étantes', 'toute', 'ah', 'aucune', 'precisement', 'ait', 'dring', 'rares', 'quant', 'dans', 'lès', 'ayant', 'hein', 'beau', 'premièrement', 'quiconque', 'seule', 'da', 'restent', 'donc', 'dire', 'huitième', 'fus', 'passé', 'neuvième', 'cela', 'eu', 'ha', 'derniere', 'different', 'suivre', 'ont', 'superpose', 'importe', 'ne', 'fussions', 'subtiles', 'memes', 'ou', 'puisque', 'te', 'peux', 'connaissez', 'bigre', 'lesquelles', 'hormis', 'semblent', 'souvent', 'aurons', 'fais', 'ouverte', 'comme', 'pouah', 'quatre-vingt', 'aux', 'qui', 'deux', 'seriez', 'eusses', 'différents', 'fusse', 'auxquelles', 'autre', 'pur', 'vivat', 'pourquoi', 'celles-là', 'etant', 'parfois', 'tant', 'deja', 'tente', 'ô', 'particulièrement', 'anterieures', 'nos', 'lorsque', 'sixième', 'sera', 'bonsoir', 'meme', 'je', 'multiple', 'w', "aujourd'hui", 'depuis', 'devers', 'eut', 'des', 'ni', 'ouverts', 'etre', 'directe', 'celles', 'seul', 'avions', 'me', 'quanta', 'pense', 'serez', 'chez', 'absolument', 'compris', 'assez', 'elle', 'suivante', 'leur', 'situe', 'sa', 'laquelle', 'troisième', 'siens', 'leurs', 'merci', 'telles', 'soit', 'dite', 'suffit', 'six', 'tel', 'ailleurs', 'chers', 'fussent', 'lors', 'certes', 'q', 'toi-même', 'enfin', 'en', 'sacrebleu', 'sept', 'devra', 'quelle', 'crac', 'toi', 'directement', 'ouste', 'siennes', 'tes', 'duquel', 'cette', 'necessaire', 'onzième', 'nous-mêmes', 'avait', 'pres', 'nôtre', 'étant', 'sinon', 'mien', 'plusieurs', 'excepté', 'outre', 'vu', 'houp', 'serions', 'possessifs', 'de', 'voilà', 'la', 'été', 'seront', 'eussions', 'suffisant', 'moi', 'pu', 'seize', 'ho', 'sien', 'aurai', 'treize', 'tien', 'boum', 'clac', 'vlan', 'as', 'quelques', 'ohé', 'moi-même', 'quand', 'rend', 'faisant', 'auquel', 'stp', 'allons', 'mienne', 'o', 'peuvent', 'quelles', 'situer', 'près', 'unes', 'étés', 'minimale', 'étais', 'suivantes', 'les', 'chiche', 'moi-meme', 'suivants', 'vôtres', 'aviez', 'es', 'oh', 'derrière', 'sein', 'neuf', 'toc', 'diverses', 'bonjour', 'envers', 'ès', 'nous', 't', 'psitt', 'ça', 'parler', 'necessairement', 'quelque', 'hem', 'dessous', 'proche', 'quels', 'telle', 'peux-tu', 'notre', 'diverse', 'parseme', 'autres', 'soi-même', 'adresse', 'eurent', 'est', 'tsouin', 'exterieur', 'fussiez', 'eûtes', 'moins', 'maintenant', 'allaient', 'aurais', 'fi', 'certaines', 'suffisante', 'grandpy', 'au', 'autrefois', 'c', 'celui', 'aies', 'avant', 'chut', 'vifs', 'étée', 'auras', 'mille', 'ayante', 'chacune', 'ouf', 'longtemps', 'las', 'hum', 'toutefois', 'm', 'cinquantaine', 'néanmoins', 'voudrais', 'f', 'dit', 'strictement', 'reste', 'remarquable', 'suit', 'soixante', 'auraient', 'a', 'façon', 'naturelles', 'tellement', 'cent', 'papi', 'j', 'font', 'mais', 'aient', 'nouveau', 'hou', 'tienne', 'cinq', 'y', 'toujours', 'elles-mêmes', 'et', 's']

class Parser:

    def __init__(self, user_request):
        self.user_request = user_request

    def parsing(self):
        self.user_request = self.user_request.lower()
        self.user_request = re.sub(r"[.!:,;?\']", " ", self.user_request).split()
        self.user_request = [mot for mot in self.user_request if mot not in STOPWORDS]
        self.user_request = ' '.join(self.user_request)
        return self.user_request


class GoogleMaps:

    def __init__(self, query):
        self.query = query
        self.lat = float
        self.lng = float
        self.formatted_address = str

    def location(self):
        g_params = {
            "address": self.query,
            "key": "AIzaSyCBw0dKX6WPzdqZnBGvKMyrKQq04pxS4JM",
            "components": "country:FR",
        }
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=g_params)
        gmap=r.json()
        if gmap["status"] == "OK":
            self.formatted_address = gmap["results"][0]["formatted_address"]
            self.lat = gmap["results"][0]["geometry"]["location"]["lat"]
            self.lng = gmap["results"][0]["geometry"]["location"]["lng"]
            return self.formatted_address, self.lat, self.lng


class Wiki:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def comment(self):
        coordinates = '{}|{}'.format(self.latitude, self.longitude)
        wiki_params = {'action': 'query', 'generator': 'geosearch', 'ggsradius': 400,
             'ggscoord': coordinates, 'prop': 'extracts', 'explaintext': True, 'exsentences': 2,
             'exlimit': 1, 'redirects': True, 'format': 'json', 'formatversion': 2}
        r = requests.get('https://fr.wikipedia.org/w/api.php', params=wiki_params)
        wiki = r.json()
        try:
            comments = wiki['query']['pages'][0]['extract']
            pageid = wiki['query']['pages'][0]['pageid']
            return comments, pageid
        except KeyError:
            print("key error")
            pass


class GrandPyMessages:
    """ Class to display random messages from a list of GrandPy Bot messages. """

    # Class attributes : list of possible answers.
    LISTANSWER = ["J'ai trouvé ! L'adresse que tu cherches est : ", \
                    "Je me disais bien cela me disait quelque chose ! Le lieu que tu cherches se trouve à cette adresse : "]

    LISTANOANSWER = ["Désolé mais je n'ai pas compris ta demande.\n"\
                    "Peux-tu reformuler ta requête ?", \
                    "Je ne comprends pas.\n"\
                    "Tu peux me faire une demande plus claire et directe ?"]

    LISTWIKIPEDIA = ["Je connais très bien cet endroit "\
                    "et cela me permet de te raconter son histoire ! ", \
                    "Je connais très bien ce lieu. \n"\
                    "Voilà son histoire... "]

    LISTNOWIKIPEDIA = ["Désolé mais je n'ai pas d'histoire intéressante à ce sujet.", \
                    "Oh ! Je n'ai plus les idées claires, j'ai oublié l'histoire à ce sujet.", \
                    "Pardon mais je connais mal l'histoire de cet endroit."]


    def randomAnswer():
        """ Random messages where GrandPy Bot gives the address of the place. """
        address_answer = random.choice(GrandPyMessages.LISTANSWER)
        # print(address_result)
        return address_answer

    def randomNoAnswer():
        """ Random messages when GrandPy Bot didn't understand the user query. """
        no_answer = random.choice(GrandPyMessages.LISTANOANSWER)
        # print(no_result)
        return no_answer

    def randomStory():
        """ Random messages where GrandPy Bot tell the story about the place. """
        story_answer = random.choice(GrandPyMessages.LISTWIKIPEDIA)
        # print(wiki_result)
        return story_answer

    def randomNoStory():
        """ Random messages where GrandPy Bot tell that he has no story about the place. """
        no_story = random.choice(GrandPyMessages.LISTNOWIKIPEDIA)
        # print(wiki_result)
        return no_story

