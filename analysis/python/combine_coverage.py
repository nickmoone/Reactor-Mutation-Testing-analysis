import csv
import os
import sys

glob_result = [0, 0, 0]

""" Get all paths to compare_coverage.csv files in root (sub)folders.
"""
def get_files(root):
    filepaths = []

    for subdir, _, files in os.walk(root):
        for file in files:
            if file.endswith("coverage.csv"):
                filepaths.append((subdir.split("/")[-1], os.path.join(subdir, file)))

    return filepaths


""" Read the compare_coverage.csv file and add values to the global result.
"""
def handle_csv(project, file, writer):
    lines = file.readlines()
    if len(lines) != 0:
        last_line = lines[-1]
        reader = csv.reader([last_line])

        data = next(reader)

        glob_result[0] += int(data[1])
        glob_result[1] += int(data[2])

        writer.writerow([project] + data[1:])


if __name__ == "__main__":
    if len(sys.argv) > 2:
        root = sys.argv[1]
        csv_path = sys.argv[2]

        with open(csv_path, "w") as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(["project", "mutations", "killed", "% killed"])
            for project, filepath in get_files(root):
                with open(filepath, "r", encoding='utf-8') as file:
                    handle_csv(project, file, writer)

            if glob_result[0] != 0:
                glob_result[2] = round(glob_result[1] / glob_result[0] * 100, 2)
            else:
                glob_result[2] = 0

            writer.writerow([])
            writer.writerow(["TOTAL"] + glob_result)
    else:
        exit("Usage: python combine_coverage.py <results_path> <csv_path>")
