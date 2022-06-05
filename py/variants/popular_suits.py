import py.utils as u


if __name__ == "__main__":
    path = 'output/variants/popular_suits'
    header = ['Suit', 'Count', '%']
    u.run_workflow(path, header)
