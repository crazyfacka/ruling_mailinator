"""Commons library"""

import json
import os

def load_confs(confs):
    """Standard func to load confs into JSON parsed variable"""
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(f'{__location__}/../confs/{confs}.json') as f:
        loaded_file = json.load(f)
    return loaded_file