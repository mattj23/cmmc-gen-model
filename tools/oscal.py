import json
from typing import List


def parse(file_path: str) -> List:
    with open(file_path, "r", encoding='utf-8') as handle:
        data = json.load(handle)


    return []