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


@swag_from("export.yml", methods=['GET'])
@app.route("/export/<game_id>")
def export_game(game_id):
    print(game_id)
    url = f'https://hanab.live/export/{game_id}'
    response = requests.get(url)
    return response.json()


@swag_from("history_pagination.yml", methods=['GET'])
@app.route("/api/v1/history/<players>")
def get_history_page(players):
    players = players.replace(",", "/")
    url = f'https://hanab.live/api/v1/history/{players}'
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
