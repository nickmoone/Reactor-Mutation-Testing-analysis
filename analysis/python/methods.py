import csv
import os
import sys
from html.parser import HTMLParser

glob_result = {}
totals = [0, 0, 0, 0, 0, 0, 0]

""" HTML parser that counts how often each Reactor reactive method is killed, survived, or timed_out.
"""
class PITReactorCountMethodParser(HTMLParser):
    def __init__(self):
        super(PITReactorCountMethodParser, self).__init__(convert_charrefs=True)
        self.result = {}
        # killed, survived, timed out, no coverage, non viable, memory error, run error. 
        self.classes = ["KILLED", "SURVIVED", "TIMED_OUT", "NO_COVERAGE", "NON_VIABLE", "MEMORY_ERROR", "RUN_ERROR"]
        self.curr_class = None

    # If we found a p tag, check if it is for one of the classes and save the class.
    def handle_starttag(self, tag, attrs):
        if tag == "p":
            for attr, value in attrs:
                if attr == "class":
                    self.curr_class = value

    def handle_endtag(self, tag):
        if tag == "p":
            self.curr_class = None

    # If this data contains a removed reactive method, update the value of this method in the result.
    def handle_data(self, data):
        if self.curr_class in self.classes and ("removed call to reactor/core/publisher/Flux::" in data or "removed call to reactor/core/publisher/Mono::" in data):
            method = data.split("removed call to reactor/core/publisher/", 1)[1].split(" ")[0]
            if method not in self.result:
                self.result[method] = [0, 0, 0, 0, 0, 0, 0]
            if method not in glob_result:
                glob_result[method] = [0, 0, 0, 0, 0, 0, 0]

            if self.curr_class == self.classes[0]:
                self.result[method][0] += 1
                glob_result[method][0] += 1
                totals[0] += 1
            elif self.curr_class == self.classes[1]:
                self.result[method][1] += 1
                glob_result[method][1] += 1
                totals[1] += 1
            elif self.curr_class == self.classes[2]:
                self.result[method][2] += 1
                glob_result[method][2] += 1
                totals[2] += 1
            elif self.curr_class == self.classes[3]:
                self.result[method][3] += 1
                glob_result[method][3] += 1
                totals[3] += 1
            elif self.curr_class == self.classes[4]:
                self.result[method][4] += 1
                glob_result[method][4] += 1
                totals[4] += 1
            elif self.curr_class == self.classes[5]:
                self.result[method][5] += 1
                glob_result[method][5] += 1
                totals[5] += 1
            elif self.curr_class == self.classes[6]:
                self.result[method][6] += 1
                glob_result[method][6] += 1
                totals[6] += 1


""" Get all Pitest result files that are not index.html.
    These files should be the reactive folder structure as created by collectHTML.py.
"""
def get_result_files(root):
    filepaths = []

    for subdir, _, files in os.walk(root):
        for file in files:
            if file.endswith(".html") and not file.endswith("index.html"):
                filepaths.append(os.path.join(subdir, file))

    return filepaths

""" Nicely print how often each method is killed, survived or timed_out.
"""
def prettyprint(filepath, result):
    result = dict(sorted(result.items()))

    print("File: ", filepath)
    for method in result:
        mutations = sum(glob_result[method])
        killed, survived, timed_out, no_coverage, non_viable, memory_error, run_error = result[method]
        print("== ", method, "===")
        print("Mutations    : ", mutations)
        print("KILLED       : ", killed)
        print("SURVIVED     : ", survived)
        print("TIMED_OUT    : ", timed_out)
        print("NO_COVERAGE  : ", no_coverage)
        print("NON_VIABLE   : ", non_viable)
        print("MEMORY_ERROR : ", memory_error)
        print("RUN_ERROR    : ", run_error)

    print("== TOTALS ===")
    print("Mutations    : ", sum(totals))
    print("KILLED       : ", totals[0])
    print("SURVIVED     : ", totals[1])
    print("TIMED_OUT    : ", totals[2])
    print("NO_COVERAGE  : ", totals[3])
    print("NON_VIABLE   : ", totals[4])
    print("MEMORY_ERROR : ", totals[5])
    print("RUN_ERROR    : ", totals[6])


""" Write results to csv file.
"""
def write_csv(csvpath, result):
    result = dict(sorted(result.items()))

    with open(csvpath, "w") as file:
        header = ["method", "mutations", "KILLED", "SURVIVED", "TIMED_OUT", "NO_COVERAGE", "NON_VIABLE", "MEMORY_ERROR", "RUN_ERROR"]
        writer = csv.writer(file)
        writer.writerow(header)
        for method in result:
            row = [method] + [sum(glob_result[method])] + result[method]
            writer.writerow(row)

        writer.writerow([])
        row = ["TOTAL"] + [sum(totals)] + totals
        writer.writerow(row)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        reactive_root = sys.argv[1]
        csv_path = sys.argv[2]

        for filepath in get_result_files(reactive_root):
            parser = None
            with open(filepath, "r", encoding='utf-8') as file:
                parser = PITReactorCountMethodParser()
                parser.feed(file.read().replace('\n', ''))
                # prettyprint(filepath, parser.result)

        # prettyprint("Global", glob_result)
        write_csv(csv_path, glob_result)
    else:
        exit("Usage: python methods.py <reactive_root> <csv_path>")
