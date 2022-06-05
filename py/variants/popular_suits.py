"""
Description:
    Number and percentage of games containing each suit sorted by count in descending order.

Columns:
    - Suit: suit name
    - Count: number of games containing the suit
    - %: percentage of games containing the suit
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/variants/popular_suits'
    header = ['Suit', 'Count', '%']
    u.run_workflow(path, header)
