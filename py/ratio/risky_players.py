import py.utils as u


if __name__ == "__main__":
    path = 'output/ratio/risky_players'
    header = ['Player', 'Ratio', 'Third strike', 'Total']
    u.run_workflow(path, header)
