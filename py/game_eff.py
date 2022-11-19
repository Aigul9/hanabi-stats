import pandas as pd
from sqlalchemy import false, desc

from database.db_connect import session, Game, Variant, CardAction, Clue


def current_eff(game):
    variant, max_score, suits = session\
        .query(Variant.variant, Variant.max_score, Variant.suits)\
        .filter(Variant.variant_id == game.variant_id)\
        .first()
    score = game.score
    if score != max_score:
        return
    
    num_suits = len(suits)
    if not is_hard_var(variant, num_suits, len(game.players)):
        return

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
    num_lost_clues = get_lost_clues(actions, clues, discard_value) if 'Throw' not in variant else 0

    # Efficiency is simply "cardsGotten / potentialCluesLost"
    eff = round(score / (num_clues + (num_misplays + num_lost_clues) * discard_value), 2)
    print(game.game_id, eff, score, num_clues, num_misplays, num_lost_clues)
    return eff


# hard variants by default
# https://github.com/Hanabi-Live/hanabi-live/blob/main/packages/client/src/game/rules/hGroup.ts
# minEfficiency
# https://github.com/Hanabi-Live/hanabi-live/blob/main/packages/client/src/game/rules/stats.ts#L228
# efficiency
# https://github.com/hanabi/hanabi.github.io/blob/main/misc/efficiency.md
def is_hard_var(variant, num_suits, num_players):
    eff_table = pd.read_csv('../input/eff.tsv', sep='\t')
    eff_table.set_index('Variant Type', inplace=True)

    var_parts = ['Mix', 'Color Mute', 'Number Mute', 'Throw It in a Hole', 'Cow & Pig', 'Duck', 'Up or Down']
    if any(vp in variant for vp in var_parts):
        return True

    # Dark [Suit] / Gray / Cocoa Rainbow / Gray Pink
    var_parts = ['Black', 'Dark', 'Gray', 'Cocoa Rainbow']
    num_dark = [vp in variant for vp in var_parts].count(True)

    f_suits = f'{num_suits} Suits'
    f_players = f'{num_players}-player' if num_players in (2, 5, 6) else '3/4-player'
    one_of_each = 'w/ 1x 1oE'
    two_of_each = 'w/ 2x 1oE'
    eff = -1

    if variant.startswith('Clue Starved'):
        eff = eff_table.loc[f'{f_suits} (Clue Starved)', f_players]
    elif variant.startswith('Critical Fours'):
        if num_dark > 0:
            eff = eff_table.loc[f'{f_suits} (Critical Fours) {one_of_each}', f_players]
        else:
            eff = eff_table.loc[f'{f_suits} (Critical Fours)', f_players]
    elif num_players in (3, 4, 5, 6):
        if num_dark == 2 or variant.count('Gray') == 2 or variant.count('Dark') == 2:
            eff = eff_table.loc[f'{f_suits} {two_of_each}', f_players]
        elif num_dark == 1 and (variant.count('Gray') in (0, 1) or variant.count('Dark') in (0, 1)):
            eff = eff_table.loc[f'{f_suits} {one_of_each}', f_players]
        elif num_dark == 0:
            eff = eff_table.loc[f_suits, f_players]
    return eff >= 1.25


def get_lost_clues(actions, clues, discard_value):
    play_actions = actions[actions['action_type'] == 'play']
    last_cards = play_actions.groupby(['card_suit']).max().sort_values(['turn_action'])
    num_lost_clues = 0
    num_clues_back = 0
    for suit, card in last_cards.iterrows():
        num_discards = len(actions[(actions['action_type'] == 'discard') & (actions['turn_action'] < card.turn_action)])
        num_clues = len(clues[clues['turn_clued'] < card.turn_action])
        current_clues = 8 + (num_clues_back + num_discards) * discard_value - num_clues
        num_clues_back += 1
        num_lost_clues += 1 if current_clues == 8 else 0
    return num_lost_clues


if __name__ == '__main__':
    # g = session.query(Game).filter(Game.game_id == 292758).first()
    # print(current_eff(g))

    games_Jeff = session.query(Game)\
        .filter(Game.players.any('IAMJEFF'))\
        .filter(Game.end_condition == 1)\
        .filter(Game.num_players != 2)\
        .filter(Game.all_or_nothing == false())\
        .order_by(desc(Game.game_id))\
        .all()

    for g in games_Jeff:
        current_eff(g)
