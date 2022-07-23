"""
    This main script retrieves the artifacts and generates the model.
"""
import os
import requests

from tools import (cmmc_mapping, nist_controls, nist_assessments, dod_scores)

working_folder = "build"


def empty(document: str):
    pass


artifacts = {
    "cmmc_mapping": {
        "parser": cmmc_mapping.parse,
        "url": "https://www.acq.osd.mil/cmmc/docs/CMMCModel_V2_Mapping.xlsx",
    },
    "nist_controls": {
        "parser": nist_controls.parse,
        "url": "https://csrc.nist.gov/csrc/media/Publications/sp/800-171/rev-2/final/documents/sp800-171r2-security-reqs.csv",
    },
    "nist_assessments": {
        "parser": nist_assessments.parse,
        "url": "https://csrc.nist.gov/csrc/media/Publications/sp/800-171a/final/documents/sp800-171A-assessment-procedures.csv",
    },
    "nist_mapping": {
        "parser": empty,
        "url": "https://csrc.nist.gov/CSRC/media/Publications/sp/800-171/rev-2/final/documents/csf-v1-0-to-sp800-171rev2-mapping.xlsx",
    },
    "dod_scores": {
        "parser": dod_scores.parse,
        "url": "https://www.acq.osd.mil/asda/dpc/cp/cyber/docs/safeguarding/NIST-SP-800-171-Assessment-Methodology-Version-1.2.1-6.24.2020.pdf",
    },
    "nist_800_53_r4": {
        "parser": empty,
        "url": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev4/json/NIST_SP-800-53_rev4_catalog.json",
    },
    "nist_800_53_r5": {
        "parser": empty,
        "url": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json",
    },
}


def main():
    # Create the build folder if it doesn't exist
    if not os.path.exists(working_folder):
        os.makedirs(working_folder)

    parsed = {}
    for key, artifact in artifacts.items():
        # Download from internet
        file_path = os.path.join(working_folder, artifact['url'].split("/")[-1])
        if os.path.exists(file_path):
            print(f"File {file_path} already exists, skipping.")
        else:
            print(f"Downloading {file_path} from {artifact['url']}")
            response = requests.get(artifact['url'], allow_redirects=True)
            with open(file_path, "wb") as handle:
                handle.write(response.content)

        # Parse the file with the specified parser function and save it to a temporary dictionary
        parsed[key] = artifact['parser'](file_path)


if __name__ == '__main__':
    main()
