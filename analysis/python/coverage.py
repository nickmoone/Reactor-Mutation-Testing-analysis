import csv
import os
import sys
from html.parser import HTMLParser

glob_killed = 0
glob_mutations = 0

""" Split string by delimiter and keep delimiter.
"""
def split_keep(string, delimiter):
    return [delimiter + s for s in string.split(delimiter) if s]

""" HTML parser that finds the mutation coverage shown in a index.html file.
"""
class PitReactorParser(HTMLParser):
    def __init__(self):
        super(PitReactorParser, self).__init__(convert_charrefs=True)
        self.result = {}
        self.killed = 0
        self.mutations = 0
        self.use_data = False
        self.n_data_found = 0

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for attr, value in attrs:
                if attr == "class" and value == "coverage_legend":
                    self.use_data = True
        else:
            self.use_data = False

    def handle_endtag(self, tag):
        if tag == "div":
            self.use_data = False

    def handle_data(self, data):
        if self.use_data:
            if self.n_data_found == 1: # Only use the second finding because this is the mutation coverage.
                self.killed += int(data.split("/")[0])
                self.mutations += int(data.split("/")[1])
            self.n_data_found += 1


""" Get paths to index.html reports and return in list of tuples.
    Only gets the most outer index.html (the one that is Package Summary).
"""
def get_filepaths(root):
    filepaths = []

    for subdir, _, files in os.walk(root):
        for file in files:
            if file.endswith("index.html") and "Project Summary" in open(os.path.join(subdir, file), "r").read():
                file = os.path.join(subdir, file)
                filepaths.append(file)

    return filepaths


if __name__ == "__main__":
    if len(sys.argv) > 2:
        root = sys.argv[1]
        csvpath = sys.argv[2]

        filepaths = get_filepaths(root)

        with open(csvpath, "w") as csvfile:
            header = ["report", 
                    "mutations",
                    "killed",
                    "% killed"]
            writer = csv.writer(csvfile)
            writer.writerow(header)

            for path in filepaths:
                parser = None
                with open(path, "r", encoding='utf-8') as file:
                    # Sum coverage numbers.
                    parser = PitReactorParser()
                    parser.feed(file.read().replace('\n', ''))
                    glob_killed += parser.killed
                    glob_mutations += parser.mutations

                    row = ["".join(split_keep(path, "/")[-4:]),
                        parser.mutations,
                        parser.killed,
                        round(parser.killed/parser.mutations*100, 2)]

                    writer.writerow(row)

            # Calculate percentage and export results.
            writer.writerow([])
            row = ["TOTAL",
                glob_mutations,
                glob_killed,
                round(glob_killed/glob_mutations*100, 2)]

            writer.writerow(row)
    else:
        exit("Usage: python coverage.py <root> <csvpath>")
