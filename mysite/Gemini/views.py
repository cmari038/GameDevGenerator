import json
import os

import google.generativeai as genai
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .models import Game

# from gemini import generateGame

# Create your views here.


def generateGame(genreList, theme, topic):
    # Using `GOOGLE_API_KEY` environment variable.
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)

    """# Checking for all available models with generateContent feature
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(model.name) """

    # print(genreString)

    # Initiate the Model
    model = genai.GenerativeModel(model_name="gemini-pro")

    if len(genreList) == 0:
        if theme == '' and topic == '':
            response = model.generate_content(
                f"Give me 3 unique ideas for games, including a long and detailed description of the game's title, setting, lore, story, characters, levels, enemies, bosses, equipment, gameplay features, and unique mechanics. Add an END on its own line to indicate the end of a game idea")
        elif theme != '' and topic == '':
            response = model.generate_content(
                f"Give me 3 unique ideas for {theme} games, including a long and detailed description of the game's genre, title, setting, lore, story, characters, enemies, levels, bosses, gameplay features (in how they fit the chosen genre), abilities, equipment, and unique features. Add an END on its own line to indicate the end of a game idea")

        elif theme == '' and topic != '':
            response = model.generate_content(
                f"Give me 3 unique ideas for games about {topic}, including a long and detailed description of the game's genre, title, setting, lore, story, characters, enemies, levels, bosses, gameplay features (in how they fit the chosen genre), abilities, equipment, and unique features. Add an END on its own line to indicate the end of a game idea")

        else:
            response = model.generate_content(
                f"Give me 3 unique ideas for {theme} games about {topic}, including a long and detailed description of the game's genre, title, setting, lore, story, characters, enemies, levels, bosses, gameplay features (in how they fit the chosen genre), abilities, equipment, and unique features. Add an END on its own line to indicate the end of a game idea")

    else:
        genreString = ''
        for genre in genreList:
            genreString = genreString + genre + ", "

        if theme == '' and topic == '':
            # Query the Model
            response = model.generate_content(
                f"Give me a unique idea for a game that fits each of the following genres:{genreString}, including a long and detailed description of the game's genre, title, setting, lore, story, characters, enemies, levels, bosses, gameplay features (in how they fit the chosen genre), abilities, equipment, and unique features. Add an END on its own line to indicate the end of a game idea")

            # print(response.text)
        elif theme != '' and topic == '':
            response = model.generate_content(
                f"Give me a unique idea for a {theme} game that fits each of the following genres:{genreString}, including a long and detailed description of the game's genre, title, setting, lore, story, characters, enemies, levels, bosses, gameplay features (in how they fit the chosen genre), abilities, equipment, and unique features. Add an END on its own line to indicate the end of a game idea")

        elif theme == '' and topic != '':
            response = model.generate_content(
                f"Give me a unique idea for a game about {topic} that fits each of the following genres:{genreString}, including a long and detailed description of the game's genre, title, setting, lore, story, characters, enemies, levels, bosses, gameplay features (in how they fit the chosen genre), abilities, equipment, and unique features. Add an END on its own line to indicate the end of a game idea")

        else:
            response = model.generate_content(
                f"Give me a unique idea for a {theme} game about {topic} that fits each of the following genres:{genreString}, including a long and detailed description of the game's genre, title, setting, lore, story, characters, enemies, levels, bosses, gameplay features (in how they fit the chosen genre), abilities, equipment, and unique features. Add an END on its own line to indicate the end of a game idea")

    # return parser(response.text)
    return response.text
    # return response.text.replace('\n', '<br>')


"""
 <script>
        function getCookie(name) {
          let cookieValue = null;
          if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                  cookie.substring(name.length + 1)
                );
                break;
              }
            }
          }
          return cookieValue;
        }
        const csrftoken = getCookie("csrftoken");
        window.csrftoken = csrftoken;
      </script>

"""


@csrf_exempt
def getGameIdea(request):
    genreList = []
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        genreList = jsonData.get('genreList')
        theme = jsonData.get('Theme')
        topic = jsonData.get('Topic')
        gameIdeas = {'gameIdeas': generateGame(genreList, theme, topic)}
        # print(gameIdeas['gameIdeas'])
        # print(genreList)
        Game.objects.create(game=gameIdeas['gameIdeas'])
        return HttpResponse('')
    if request.method == 'GET':
        game = Game.objects.first()
        output = copyString(game.game)
        # game.delete()
        # return render(request, 'response.html', gameIdeas)
        # return HttpResponse(gameIdeas['gameIdeas'])
        Game.objects.all().delete()
        return HttpResponse(output)


def parser(output, genreList):
    if len(genreList) == 0:
        for i in range(3):
            index = output.find("END")
            games.append(output[0::index])
            output = output[index+1::len(output)]
            return games
    else:
        games = []
        for i in range(len(genreList)):
            index = output.find("END")
            games.append(output[0::index])
            output = output[index+1::len(output)]
            return games


def printGenres(genreList):
    for genre in genreList:
        print(genre)


def copyString(text):
    copy = ''
    for letter in text:
        copy += letter
    return copy
