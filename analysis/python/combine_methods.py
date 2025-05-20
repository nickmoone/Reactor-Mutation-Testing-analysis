import csv
import os
import sys

glob_result = {}
glob_totals = [0, 0, 0, 0, 0, 0, 0, 0]

""" Get all paths to count_methods.csv files in root (sub)folders.
"""
def get_files(root):
    filepaths = []

    for subdir, _, files in os.walk(root):
        for file in files:
            if file.endswith("methods.csv"):
                filepaths.append(os.path.join(subdir, file))

    return filepaths


""" Read the count_methods.csv file and add values to the global result.
"""
def read_csv(file):
    def skip_last(iterator):
        prev = next(iterator)
        for item in iterator:
            yield prev
            prev = item

    reader = csv.reader(file)

    next(reader)
    for row in skip_last(reader):
        if len(row) > 0:
            if row[0] not in glob_result:
                glob_result[row[0]] = [0, 0, 0, 0, 0, 0, 0, 0]

            for i in range(0, len(row) - 1):
                glob_result[row[0]][i] += int(row[i + 1])

            for i in range(0, len(row) - 1):
                glob_totals[i] += int(row[i + 1])


""" Write the global result to csv.
"""
def write_csv(path, result):
    with open(path, "w") as file:
        writer = csv.writer(file)

        writer.writerow(["method", "mutations", "KILLED", "SURVIVED", "TIMED_OUT", "NO_COVERAGE", "NON_VIABLE", "MEMORY_ERROR", "RUN_ERROR"])
        for method in dict(sorted(result.items())):
            writer.writerow([method] + result[method])
        writer.writerow([])
        writer.writerow(["TOTAL"] + glob_totals)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        root = sys.argv[1]
        csv_path = sys.argv[2]

        for filepath in get_files(root):
            with open(filepath, "r", encoding='utf-8') as file:
                read_csv(file)

        write_csv(csv_path, glob_result)
    else:
        exit("Usage: python combine_methods.py <results_path> <csv_path>")
