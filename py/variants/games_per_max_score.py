"""
Description:
    Prediction of the required number of attempts to get a max score for the given variant.
    It is calculated as a number of total games divided by a number of max scores.

Columns:
    - Variant: variant name
    - Variant id: variant id
    - Games: number of games required to get a max score
    - Total: number of total games for the variant
    - Max scores: number of max scores for the variant
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/variants/games_per_max_score'
    header = ['Variant', 'Variant id', 'Games', 'Total', 'Max scores']
    u.run_workflow(path, header)
