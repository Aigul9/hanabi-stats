import py.utils as u


if __name__ == "__main__":
    path = 'output/ratio/terminated_2p'
    header = ['Player1', 'Player2', 'Total', 'Terminated', '%']
    u.run_workflow(path, header)
