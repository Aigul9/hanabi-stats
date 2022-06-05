import py.utils as u


if __name__ == "__main__":
    path = 'output/variants/popular_variants'
    header = ['Variant', 'Count']
    u.run_workflow(path, header)
