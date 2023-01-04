import pandas as pd
from collections import defaultdict
from sqlalchemy import func, false

from database.db_connect import session, Game, Variant, CardAction, Clue, GameParticipant
import py.utils as u


def current_eff(game):
    variant = game.variant
    score = game.score

    actions = pd.read_sql(session.query(CardAction)
                          .filter(CardAction.game_id == game.game_id)
                          .filter(CardAction.turn_action != None)
                          .order_by(CardAction.turn_action)
                          .statement,
                          session.bind)
    clues = pd.read_sql(session.query(Clue)
                        .filter(Clue.game_id == game.game_id)
                        .order_by(Clue.turn_clued)
                        .statement,
                        session.bind)

    discard_value = 1 if 'Clue Starved' not in variant else 0.5
    num_misplays = len([a for idx, a in actions.iterrows() if a.action_type == 'misplay'])
    num_clues = len(clues)
    # when the last card is played at 8 clues
    num_clues_lost = get_lost_clues(actions, clues, discard_value) if 'Throw' not in variant else 0

    # Efficiency is simply "cardsGotten / potentialCluesLost"
    u.logger.debug((game.game_id, score, num_clues, num_misplays, num_clues_lost))
    eff = round(score / (num_clues + (num_misplays + num_clues_lost) * discard_value), 2)
    # print(eff)
    return eff


# hard variants by default
# https://github.com/Hanabi-Live/hanabi-live/blob/main/packages/client/src/game/rules/hGroup.ts
# minEfficiency
# https://github.com/Hanabi-Live/hanabi-live/blob/main/packages/client/src/game/rules/stats.ts#L228
# efficiency
# https://github.com/hanabi/hanabi.github.io/blob/main/misc/efficiency.md
def is_hard_var(variant, num_suits, num_players):
    if any(vp in variant for vp in VAR_PARTS):
        return True
    
    num_dark = [vp in variant for vp in DARK_PARTS].count(True)
    f_suits = f'{num_suits} Suits'
    f_players = f'{num_players}-player' if num_players in (2, 5, 6) else '3/4-player'
    one_of_each = 'w/ 1x 1oE'
    two_of_each = 'w/ 2x 1oE'
    eff = -1

    if variant.startswith('Clue Starved'):
        eff = EFF_TABLE.loc[f'{f_suits} (Clue Starved)', f_players]
    elif variant.startswith('Critical Fours'):
        if num_dark > 0:
            eff = EFF_TABLE.loc[f'{f_suits} (Critical Fours) {one_of_each}', f_players]
        else:
            eff = EFF_TABLE.loc[f'{f_suits} (Critical Fours)', f_players]
    elif num_players in (3, 4, 5, 6):
        if num_dark == 2 or variant.count('Gray') == 2 or variant.count('Dark') == 2:
            eff = EFF_TABLE.loc[f'{f_suits} {two_of_each}', f_players]
        elif num_dark == 1 and (variant.count('Gray') in (0, 1) or variant.count('Dark') in (0, 1)):
            eff = EFF_TABLE.loc[f'{f_suits} {one_of_each}', f_players]
        elif num_dark == 0:
            eff = EFF_TABLE.loc[f_suits, f_players]
    return eff >= 1.25


def get_lost_clues(actions, clues, discard_value):
    play_actions = actions[actions['action_type'] == 'play']
    last_cards = play_actions.groupby(['card_suit']).max().sort_values(['turn_action'])
    num_clues_lost = 0
    num_clues_back = 0
    for suit, card in last_cards.iterrows():
        num_discards = len(actions[(actions['action_type'] == 'discard') & (actions['turn_action'] < card.turn_action)])
        num_clues = len(clues[clues['turn_clued'] < card.turn_action])
        current_clues = 8 + (num_clues_back + num_discards) * discard_value - num_clues
        num_clues_back += 1
        num_clues_lost += 1 if current_clues == 8 else 0
    return num_clues_lost


if __name__ == '__main__':
    PLAYERS = u.open_file('../input/players.txt')
    current_eff_dict = defaultdict(float)
    num_games_dict = defaultdict(int)
    games_set = set()
    EFF_TABLE = pd.read_csv('../input/eff.tsv', sep='\t')
    EFF_TABLE.set_index('Variant Type', inplace=True)
    VAR_PARTS = ['Mix', 'Color Mute', 'Number Mute', 'Throw It in a Hole', 'Cow & Pig', 'Duck', 'Up or Down']
    # Dark [Suit] / Gray / Cocoa Rainbow / Gray Pink
    DARK_PARTS = ['Black', 'Dark', 'Gray', 'Cocoa Rainbow']

    selected_players = session.query(GameParticipant.player)\
        .join(Game, GameParticipant.game_id == Game.game_id)\
        .filter(GameParticipant.player.in_(PLAYERS))\
        .filter(Game.num_players != 2)\
        .filter(Game.speedrun == false())\
        .group_by(GameParticipant.player)\
        .having(func.count(GameParticipant.game_id) >= 1000)\
        .all()
    selected_players = [p for p, in selected_players]

    game_ids = session.query(GameParticipant.game_id)\
        .distinct(GameParticipant.game_id)\
        .filter(GameParticipant.player.in_(selected_players))\
        .all()
    game_ids = [g_id for g_id, in game_ids]
    
    GAMES = session.query(Game)\
        .join(Variant, (Game.variant_id == Variant.variant_id) & (Game.variant == Variant.variant))\
        .filter(Game.game_id.in_(game_ids))\
        .filter(Game.score == Variant.max_score)\
        .filter(Game.end_condition == 1)\
        .filter(Game.num_players != 2)\
        .filter(Game.speedrun == false())\
        .filter(Game.detrimental_characters == false())\
        .filter(Game.all_or_nothing == false())\
        .order_by(Game.game_id.desc())\
        .all()

    u.logger.debug(f'Num games: {len(GAMES)}')
    num_hard_games = 0

    for g in GAMES:
        if not is_hard_var(g.variant, u.get_number_of_suits(g.variant), g.num_players):
            continue
        u.logger.info(g.game_id)
        num_hard_games += 1
        key = ', '.join(sorted(g.players, key=lambda item: item.lower()))
        c_eff = current_eff(g)
        current_eff_dict[key] += c_eff
        num_games_dict[key] += 1

    res = {k: [round(current_eff_dict[k] / num_games_dict[k], 2), num_games_dict[k]] for k in current_eff_dict.keys()}
    sorted_res = dict(sorted(res.items(), key=lambda item: (-item[1][0], item[0])))
    path = '../output/requests/current_eff'
    u.save(path, sorted_res, ['Players', 'Avg eff', 'Num of games'])
    u.logger.debug(f'Num hard games: {num_hard_games}')
