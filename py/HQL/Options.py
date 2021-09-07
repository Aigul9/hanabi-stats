class Options:
    def __init__(self,
                 num_players,
                 starting_player,
                 variant_id,
                 variant_name,
                 timed,
                 time_base,
                 time_per_turn,
                 speedrun,
                 card_cycle,
                 deck_plays,
                 empty_clues,
                 one_extra_card,
                 one_less_card,
                 all_or_nothing,
                 detrimental_characters):
        """Model of the options
        ----------

        Parameters
        ----------
        num_players : int
            Number of players
        starting_player : int
            Index of starting player
        variant_id : int
            Variant id
        variant_name : str
            Name of the variant
        timed : bool
            A flag which represents whether or not the game is timed
        time_base : int
            Base time at the start
        time_per_turn : int
            Time increment at each turn
        speedrun : bool
            A flag which represents speedrun games
        card_cycle : bool
            A flag which represents card cycling
        deck_plays : bool
            A flag which represents bottom-deck blind-plays
        empty_clues : bool
            A flag which represents empty-clues
        one_extra_card : bool
            A flag which represents one extra card option
        one_less_card : bool
            A flag which represents one less card option
        all_or_nothing : bool
            A flag which represents all or nothing option
        detrimental_characters : bool
            A flag which represents detrimental characters
        """
        self.num_players = num_players
        self.starting_player = starting_player
        self.variant_id = variant_id
        self.variant_name = variant_name
        self.timed = timed
        self.time_base = time_base
        self.time_per_turn = time_per_turn
        self.speedrun = speedrun
        self.card_cycle = card_cycle
        self.deck_plays = deck_plays
        self.empty_clues = empty_clues
        self.one_extra_card = one_extra_card
        self.one_less_card = one_less_card
        self.all_or_nothing = all_or_nothing
        self.detrimental_characters = detrimental_characters
