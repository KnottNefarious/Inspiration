import requests
import re
from system_model import System
from mechanism_extractor import extract_mechanisms_from_text


def fetch_arxiv_systems():

    systems = []

    url = "http://export.arxiv.org/api/query?search_query=all:model&max_results=20"

    data = requests.get(url).text

    entries = data.split("<entry>")

    for e in entries:

        title_match = re.search(r"<title>(.*?)</title>", e)
        summary_match = re.search(r"<summary>(.*?)</summary>", e)

        if title_match and summary_match:

            title = title_match.group(1)
            summary = summary_match.group(1)

            mechanisms = extract_mechanisms_from_text(summary)

            if mechanisms:

                systems.append(

                    System(
                        title,
                        "research",
                        ["network", "field"],
                        mechanisms,
                        []
                    )

                )

    return systems
