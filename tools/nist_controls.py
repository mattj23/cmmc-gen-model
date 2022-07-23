import csv
import re
from dataclasses import dataclass
from typing import List

key_pattern = re.compile("^\d+\.\d+\.\d+$")


@dataclass
class NistControl:
    key: str
    category: str
    type: str
    description: str
    discussion: str


def parse(file_path: str) -> List[NistControl]:
    results = []
    with open(file_path, "r") as handle:
        reader = csv.reader(handle)
        for row in reader:
            category, control_type, key, _, description, discussion = row
            if not key_pattern.match(key):
                continue
            results.append(NistControl(key, category, control_type, description, discussion))

    return results
