import py.utils as u


if __name__ == "__main__":
    path = 'output/winrate/winning_streak'
    header = ['Player', 'Count', 'Start game_id']
    u.run_workflow(path, header)
