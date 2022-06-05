import py.utils as u


if __name__ == "__main__":
    path = 'output/time/top_degenerates'
    header = ['Player', 'Year', 'Month', 'Hours']
    # TODO: fix 2020 instead of 2020.0
    u.run_workflow(path, header)
