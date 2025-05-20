import copy
import csv
import os
import sys

def checklog(log_file, stats):
    with open(log_file, 'r') as f:
        text = f.read()

        checked = 0
        description = ""

        if "Project has no tests, it is empty." in text and not "run mutation analysis" in text:
            print("NO_TESTS")
            description += "NO_TESTS "
            stats["no_tests"] += 1
            checked = 1
        if "Mutation testing requires a green suite." in text:
            print("NO_GREEN_SUITE")
            description += "NO_GREEN_SUITE "
            stats["no_green_suite"] += 1
            checked = 1
        if "Non-resolvable parent POM for" in text:
            print("PARENT_POM_PROBLEM")
            description += "PARENT POM PROBLEM "
            stats["parent_pom"] += 1
            checked = 1
        if "COMPILATION ERROR" in text:
            print("COMPILATION_ERROR")
            description += "COMPILATION_ERROR "
            stats["compilation_error"] += 1
            checked = 1
        if "UNKNOWN_ERROR" in text:
            print("UNKNOWN_ERROR")
            description += "UNKNOWN_ERROR "
            stats["unknown_error"] += 1
            checked = 1
        if "BUILD SUCCESS" in text:
            print("BUILD_SUCCESS")
            description += "BUILD_SUCCESS "
            stats["build_success"] += 1
            checked = 1
        if "error: invalid target release: 20" in text:
            print("INVALID_TARGET_RELEASE_20")
            description += "INVALID_TARGET_RELEASE_20 "
            stats["invalid_target_release_20"] += 1
            checked = 1
        if "Some Enforcer rules have failed." in text:
            print("ENFORCER_RULES_FAILED")
            description += "ENFORCER_RULES_FAILED "
            stats["enforcer_rules_failed"] += 1
            checked = 1
        if "Cannot find matching toolchain definitions for the following toolchain types" in text:
            print("CANNOT_FIND_MATCHING_TOOLCHAIN_DEFINITIONS")
            description += "CANNOT_FIND_MATCHING_TOOLCHAIN_DEFINITIONS "
            stats["cannot_find_matching_toolchain_definitions"] += 1
            checked = 1
        if "Could not resolve version conflict among" in text:
            print("DEPENDENCY_VERSION_CONFLICT")
            description += "DEPENDENCY_VERSION_CONFLICT "
            stats["dependency_version_conflict"] += 1
            checked = 1
        if "Could not resolve dependencies for project" in text:
            print("COULD_NOT_RESOLVE_DEPENDENCIES")
            description += "COULD_NOT_RESOLVE_DEPENDENCIES "
            stats["could_not_resolve_dependencies"] += 1
            checked = 1
        if "module jdk.compiler does not" in text:
            print("COMPILER_DOES_NOT_EXPORT")
            description += "COMPILER_DOES_NOT_EXPORT "
            stats["compiler_does_not_export"] += 1
            checked = 1
        if "No mutations found. This probably means there is an issue with either the supplied classpath or filters." in text:
            print("NO_MUTATIONS_FOUND")
            description += "NO_MUTATIONS_FOUND "
            stats["no_mutations_found"] += 1
            checked = 1
        if "Cannot run program" in text:
            print("CANNOT_RUN_LOCAL_PROGRAM")
            description += "CANNOT_RUN_LOCAL_PROGRAM "
            stats["cannot_run_local_program"] += 1
            checked = 1
        if "License for" in text:
            print("LICENSE_NEEDED")
            description += "LICENSE_NEEDED "
            stats["license_needed"] += 1
            checked = 1
        if "Illegal repetition near index" in text:
            print("ILLEGAL_REPETITION_IN_POM")
            description += "ILLEGAL_REPETITION_IN_POM "
            stats["illegal_repetition_in_pom"] += 1
            checked = 1
        if "Non-parseable POM" in text:
            print("NON-PARSEABLE_POM")
            description += "NON-PARSEABLE_POM "
            stats["non_parseable_pom"] += 1
            checked = 1

        if "BUILD SUCCESS" in text:
            if "Project has no tests, it is empty." in text and not "run mutation analysis" in text:
                stats["success_no_tests"] += 1
            else:
                stats["success_with_tests"] += 1

        stats["total_checked"] += checked
        stats["total_logs"] += 1

        return description


def checklogs(logs_folder, csv_path):
    stats = {
        "no_tests": 0,
        "no_green_suite": 0,
        "parent_pom": 0,
        "compilation_error": 0,
        "unknown_error": 0,
        "build_success": 0,
        "invalid_target_release_20": 0,
        "enforcer_rules_failed": 0,
        "cannot_find_matching_toolchain_definitions": 0,
        "dependency_version_conflict": 0,
        "could_not_resolve_dependencies": 0,
        "compiler_does_not_export": 0,
        "no_mutations_found": 0,
        "cannot_run_local_program": 0,
        "license_needed": 0,
        "illegal_repetition_in_pom": 0,
        "non_parseable_pom": 0,
        "success_no_tests": 0,
        "success_with_tests": 0,

        "total_checked": 0,
        "total_logs": 0
    }
    

    with open(csv_path, "w") as file:
        stats_reactive = copy.deepcopy(stats)
        stats_noreactive = copy.deepcopy(stats)
        
        writer = csv.writer(file)
        writer.writerow(["log_file", "reactive description", "no-reactive description"])

        for file in os.listdir(logs_folder + "/reactive"):
            if file.endswith(".log"):
                print(file)
                reactive_description = checklog(logs_folder + "/reactive/" + file, stats_reactive)
                noreactive_description = checklog(logs_folder + "/no-reactive/" + file, stats_noreactive)
                writer.writerow([file, reactive_description, noreactive_description])
                print()

    for key in stats_reactive:
        print(key, stats_reactive[key])

    print()
    
    for key in stats_noreactive:
        print(key, stats_noreactive[key])


if __name__ == '__main__':
    if len(sys.argv) == 3:
        checklogs(sys.argv[1], sys.argv[2])
    else:
        exit('Usage: python3 checklogs.py <logs_folder> <csv_path>')
        sys.exit(1)
