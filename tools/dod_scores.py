import re
from typing import List
from dataclasses import dataclass
import pdfplumber

key_pattern = re.compile("^(\d+\.\d+\.\d+)")


@dataclass
class DodScore:
    key: str
    description: str
    points: List[int]
    comment: str


def parse(file_path: str) -> List[DodScore]:
    pdf = pdfplumber.open(file_path)
    results = []
    for p in pdf.pages:
        tables = p.extract_tables()
        for table in tables:
            if table[0][0].lower().strip() != "security requirement":
                continue

            for row in table[1:]:
                key_text, description, value, comments = row
                key_match = key_pattern.findall(key_text)
                if not key_match:
                    raise Exception(f"Could not find key match in '{key_text}'")

                value = value.lower().strip()
                if value == "na":
                    points = []
                elif "to" in value:
                    points = [int(x.strip()) for x in value.split("to")]
                else:
                    points = [int(value)]

            results.append(DodScore(key_match[0], description.strip(), points, comments.strip()))

    return results
