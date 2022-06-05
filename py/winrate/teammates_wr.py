import py.utils as u


if __name__ == "__main__":
    path = 'output/winrate/teammates_wr'
    header = ['Player', 'Teammate', 'WR', 'Wins', 'Games']
    u.run_workflow(path, header)
