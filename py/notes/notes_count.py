"""
Description:
    Average number of notes per game.

Exclusions:
    - speedruns
    - games which do not contain any notes

Columns:
    - Player: player name
    - Ratio: average number of notes per game
    - Games: number of games containing notes
    - Notes: number of notes
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/notes/notes_count'
    header = ['Player', 'Ratio', 'Games', 'Notes']
    u.run_workflow(path, header)
