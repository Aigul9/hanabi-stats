import py.utils as u


if __name__ == "__main__":
    path = 'output/variants/games_per_max_score'
    header = ['Variant', 'Variant id', 'Games', 'Total', 'Max scores']
    u.run_workflow(path, header)
