from py.HQL.Options import Options


class UserStats:
    def __init__(self,
                 game_id,
                 options,
                 seed,
                 score,
                 num_turns,
                 end_condition,
                 datetime_started,
                 datetime_finished,
                 num_games_on_this_seed,
                 player_names,
                 increment_num_games,
                 tags):
        """Model of the game
        ----------

        Parameters
        ----------
        game_id : int
            Game id
        options : Options
            Game options
        seed : str
            Seed
        score : int
            Score
        num_turns : int
            Number of turns
        end_condition : int
            End condition
        datetime_started : str
            Start date
        datetime_finished : str
            End date
        num_games_on_this_seed : int
            Number of groups played the same seed
        player_names : list
            List of players
        increment_num_games : bool
            Increment of game id
        tags : str
            Tags
        """
        self.game_id = game_id
        self.options = Options(*options.values())
        self.seed = seed
        self.score = score
        self.num_turns = num_turns
        self.end_condition = end_condition
        self.datetime_started = datetime_started
        self.datetime_finished = datetime_finished
        self.num_games_on_this_seed = num_games_on_this_seed
        self.player_names = player_names
        self.increment_num_games = increment_num_games
        self.tags = tags
