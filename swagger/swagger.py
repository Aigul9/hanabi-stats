import requests
from flask import Flask, request
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
    filters = ''
    page = request.args.get('page')
    page = page if page is not None else 0
    size = request.args.get('size')
    size = size if size is not None else 10
    sorting = request.args.get('sorting')
    sorting = sorting if sorting is not None else 1
    game_id = request.args.get('game_id')
    filters += f'&fcol[0]={game_id}' if game_id is not None else ''
    num_players = request.args.get('num_players')
    filters += f'&fcol[1]={num_players}' if num_players is not None else ''
    score = request.args.get('score')
    filters += f'&fcol[2]={score}' if score is not None else ''
    variant_id = request.args.get('variant_id')
    filters += f'&fcol[3]={variant_id}' if variant_id is not None else ''
    url = f'https://hanab.live/api/v1/history/{players}?page={page}&size={size}&col[0]={sorting}{filters}'
    response = requests.get(url)
    return response.json()


if __name__ == '__main__':
    app.run(debug=True)
