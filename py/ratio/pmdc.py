import py.utils as u


if __name__ == "__main__":
    path = 'output/ratio/pmdc/clues'
    header = ['Player', 'Ratio', 'Clues', 'Games']
    u.run_workflow(path, header)

    path = 'output/ratio/pmdc/discards'
    header = ['Player', 'Ratio', 'Discards', 'Games']
    u.run_workflow(path, header)

    path = 'output/ratio/pmdc/plays'
    header = ['Player', 'Ratio', 'Plays', 'Games']
    u.run_workflow(path, header)

    path = 'output/ratio/pmdc/misplays'
    header = ['Player', 'Ratio', 'Misplays', 'Games']
    u.run_workflow(path, header)
