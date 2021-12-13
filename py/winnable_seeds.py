from database.db_connect import session, Card, Game


def init_3p_hands(deck):
    return {
        0: deck[0:5],
        1: deck[5:10],
        2: deck[10:15]
    }


def init_4p_hands(deck):
    return {
        0: deck[0:4],
        1: deck[4:8],
        2: deck[8:12],
        3: deck[12:16]
    }


def run(num_players):
    for seed in seeds:
        deck = session.query(Card).filter(Card.seed == seed[0]).all()
        # init starting hands
        if num_players == 3:
            hands = init_3p_hands(deck)
        else:
            hands = init_4p_hands(deck)
        if num_players == 3:
            cur_card = 15
        else:
            cur_card = 16
        # starting playable cards
        playable = [1, 1, 1, 1, 1]
        cur_player = 0
        num_actions = 0
        while num_actions <= 25:
            hand = hands[cur_player]
            status = False
            for card in hand:
                # print(card.card_index, playable)
                if playable[card.suit_index] == card.rank:
                    playable[card.suit_index] += 1
                    status = True
                    # print(card.suit_index, card.rank)
                    break
            if status is True:
                hand.append(deck[cur_card])
                cur_card += 1
                cur_player = (cur_player + 1) % num_players
                num_actions += 1
            if status is False:
                break
        print(seed[0], '\t', playable)
        if playable == [6, 6, 6, 6, 6]:
            print(seed[0], '\t', 'yes')


seeds = session.query(Card.seed)\
    .distinct(Card.seed)\
    .join(Game, Card.seed == Game.seed)\
    .filter(Game.variant == 'No Variant')\
    .all()

# run(3)
run(4)
