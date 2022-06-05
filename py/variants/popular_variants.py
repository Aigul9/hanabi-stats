"""
Description:
    Number of games for each variant sorted in descending order.

Columns:
    - Variant: variant name
    - Count: number of games for the variant
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/variants/popular_variants'
    header = ['Variant', 'Count']
    u.run_workflow(path, header)
