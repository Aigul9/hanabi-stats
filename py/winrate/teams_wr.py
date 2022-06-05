import py.utils as u


if __name__ == "__main__":
    path = 'output/winrate/teams_wr'
    header = ['Player', 'WR', 'Wins', 'Games']
    u.run_workflow(path, header)
