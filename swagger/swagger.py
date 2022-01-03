import random
import requests
from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info={
        'title': LazyString(lambda: 'Hanabi Stats API Documentation'),
        'version': LazyString(lambda: '0.1')
    },
    host=LazyString(lambda: request.host)
)
swagger = Swagger(app, template=swagger_template)


@swag_from("swagger.yml", methods=['GET'])
@app.route("/export")
def export_game():
    # """
    # Get actions, deck, id, options, players, notes, and seed for the game
    # ---
    # tags:
    #     - Game
    # parameters:
    #     - name: game_id
    #       in: path
    #       type: integer
    #       required: true
    #       description: The game id
    # responses:
    #     200:
    #       description: Successful response
    #       schema:
    #         id: game
    #         properties:
    #           id:
    #             type: integer
    #             description: The game id
    #           players:
    #             type: array
    #             description: List of players
    #             items:
    #               type: string
    #           deck:
    #             type: array
    #             description: Cards in the deck
    #             items:
    #               type: object
    #               description: The card
    #               properties:
    #                 suitIndex:
    #                   type: integer
    #                   description: The suit index
    #                 rank:
    #                   type: integer
    #                   description: The card rank
    #     400:
    #       description: Bad Request
    #     500:
    #       description: Internal Server Error
    # """
    url = f'https://hanab.live/export/655556'
    response = requests.get(url)
    return response.json()


# @app.route('/api/<string:language>/', methods=['GET'])
# def index(language):
#     """
#     This is the language awesomeness API
#     Call this api passing a language name and get back its features
#     ---
#     tags:
#       - Awesomeness Language API
#     parameters:
#       - name: language
#         in: path
#         type: string
#         required: true
#         description: The language name
#       - name: size
#         in: query
#         type: integer
#         description: size of awesomeness
#     responses:
#       500:
#         description: Error The language is not awesome!
#       200:
#         description: A language with its awesomeness
#         schema:
#           id: awesome
#           properties:
#             language:
#               type: string
#               description: The language name
#               default: Lua
#             features:
#               type: array
#               description: The awesomeness list
#               items:
#                 type: string
#               default: ["perfect", "simple", "lovely"]
#     """
#
#     language = language.lower().strip()
#     features = [
#         "awesome", "great", "dynamic",
#         "simple", "powerful", "amazing",
#         "perfect", "beauty", "lovely"
#     ]
#     size = int(request.args.get('size', 1))
#     if language in ['php', 'vb', 'visualbasic', 'actionscript']:
#         return "An error occurred, invalid language for awesomeness", 500
#     return jsonify(
#         language=language,
#         features=random.sample(features, size)
#     )


if __name__ == '__main__':
    app.run(debug=True)
