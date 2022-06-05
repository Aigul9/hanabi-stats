import py.utils as u


if __name__ == "__main__":
    path = 'output/time/hours_wr'
    header = ['Player', 'Hour', 'WR', 'Wins', 'Games']
    u.run_workflow(path, header)
