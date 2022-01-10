from sqlalchemy import true

import py.utils as u
from database.db_connect import session, Game, Card, GameAction, PlayerNotes, Player


def get_notes_count(game_id, username):
    """Gets number of player's notes.

    Parameters
    ----------
    game_id : int
        Game id
    username : str
        Player name

    Returns
    -------
    int
        Number of player's notes
    """
    notes = session.query(PlayerNotes.notes) \
        .filter(PlayerNotes.game_id == game_id) \
        .filter(PlayerNotes.player == username) \
        .scalar()
    return len([r for r in notes if r != ''])


def get_starting_cards_count(players_count, one_less_card, one_extra_card):
    """Gets number of cards in starting hands.

    Parameters
    ----------
    players_count : int
        Number of players in game
    one_less_card : bool
        A flag representing one less card option
    one_extra_card : bool
        A flag representing one extra card option

    Returns
    -------
    int
        Number of cards in starting hands
    """
    return u.get_number_of_starting_cards(
        players_count,
        one_less_card,
        one_extra_card
    )


def get_notes_ratio(username):
    """Gets ratio of player's notes per game.

    Parameters
    ----------
    username : str
        Player name

    Returns
    -------
    int
        Ratio of notes per game
    """
    notes_list = session.query(PlayerNotes.game_id, PlayerNotes.notes) \
        .filter(PlayerNotes.player == username) \
        .all()
    player_notes_visible_cards_dict = {'notes_count': 0, 'visible_cards_count': 0}

    if len(notes_list) == 0:
        return 0

    for note_row in notes_list:
        game_id = note_row.game_id
        game = session.query(Game)\
            .filter(Game.game_id == game_id)\
            .first()

        if game.num_players == 2 or game.speedrun == true():
            continue

        notes_count = get_notes_count(game_id, username)

        if notes_count == 0:
            continue

        actions = session.query(GameAction.action_type).filter(GameAction.game_id == game.game_id).all()
        players = session.query(Game.players).filter(Game.game_id == game.game_id).scalar()
        cards_count = len(session.query(Card).filter(Card.seed == game.seed).all())

        starting_cards_count = get_starting_cards_count(len(players), game.one_less_card, game.one_extra_card)

        drawn_cards_count = u.get_number_of_plays_or_discards(actions)
        visible_cards_count = min(starting_cards_count + drawn_cards_count, cards_count)

        player_notes_visible_cards_dict['notes_count'] += notes_count
        player_notes_visible_cards_dict['visible_cards_count'] += visible_cards_count

    return u.p(player_notes_visible_cards_dict['notes_count'],
               player_notes_visible_cards_dict['visible_cards_count'])


if __name__ == "__main__":
    users = session.query(Player.player).all()
    users_notes = {}
    for user in users:
        user = user[0]
        users_notes[user] = get_notes_ratio(user)

    u.save_header('../../output/notes/notes_per_game', ['Player', 'Ratio'])
    for user, user_ratio in u.sort_by_value(users_notes).items():
        u.save_value(
            '../../output/notes/notes_per_game',
            {user: user_ratio}
        )
