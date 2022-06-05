import py.utils as u


if __name__ == "__main__":
    path = 'output/ratio/clean_games'
    header = ['Player', 'Ratio', 'Clean', 'Total']
    u.run_workflow(path, header)
