import re
import csv
from dataclasses import dataclass
from typing import List

parent_key_pattern = re.compile("^\d+\.\d+\.\d+")
clean_select_from_pattern = re.compile(r"select from:\s*([\w\d\;\s\-\+\,\/]*)\]?\.?")


@dataclass
class NistAssessment:
    key: str
    parent_key: str
    requirement: str
    objective: str
    examine: List[str]
    interview: List[str]
    test: List[str]

    def is_parent(self) -> bool:
        return self.parent_key == self.key


def parse(file_path: str) -> List[NistAssessment]:
    results = []
    with open(file_path, "r") as handle:
        reader = csv.reader(handle)
        rows = [row for row in reader]

    for row in rows[1:]:
        _, key, _, requirement, objective, examine, interview, test = row
        key = key.strip()

        parent_key_match = parent_key_pattern.findall(key)
        if not parent_key_match:
            raise Exception(f"Couldn't extract a NIST parent key from '{key}'")

        results.append(NistAssessment(key, parent_key_match[0], requirement, objective,
                                      split_select_from(examine), split_select_from(interview),
                                      split_select_from(test)))

    return results


def split_select_from(text: str) -> List[str]:
    cleaned = clean_select_from_pattern.findall(text.lower())
    if not cleaned:
        assert not text.strip()
        return []

    return [x.strip() for x in cleaned[0].split(";")]
