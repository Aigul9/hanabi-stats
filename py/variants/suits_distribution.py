import py.utils as u


if __name__ == "__main__":
    path = 'output/variants/suits_distribution'
    header = ['Player',
              '6 suits', '6 suits %',
              '5 suits', '5 suits %',
              '4 suits', '4 suits %',
              '3 suits', '3 suits %']
    u.run_workflow(path, header)
