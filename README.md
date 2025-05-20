# Run and analyse pitest for Project Reactor research
This repository contains scripts for analysing the effectiveness of mutation testing for reactive programming.

The scripts in <em>/setup</em> clone a list of projects from GitHub, add our created [pitest plugin for mutating Project Reactor reactive method calls (pitest-reactor)](https://github.com/nickmoone/pitest-reactor) to the <em>pom.xml</em> of all projects, and run pitest on all projects. 

The scripts in <em>/analysis</em> extract all pitest results from the projects, exports general mutation statistics to CSV, and exports mutation statistics specific for Project Reactor reactive method calls to CSV.

## Setup

### Downloading projects
Running <em>download_projects.sh</em> requires a file containing a newline separated list of GitHub clone URLs to projects that will be cloned into a specific folder.

### Adding pitest-reactor to projects
To add pitest-reactor to the projects <em>add_pitest_to_projects.sh</em> can be used, this script adds the plugin snippet in <em>/setup/plugin-snippet.xml</em> to the plugins section of the <em>pom.xml</em> of each project.

### Changing pitest mutators
To change the mutator used by pitest-reactor in all projects <em>change_mutator_projects.sh</em> can be used, this script changes the <em>mutator</em> tag of the pitest-reactor plugin of each project.

### Running projects
To run pitest on all projects <em>run_projects.sh</em> is used, this script executes command <em>mvn test-compile org.pitest:pitest-maven:mutationCoverage</em> inside all project folders.

## Analysis

### Collecting pitest results
Running <em>collect.py</em> with the root folder of a project as input will move all pitest report files to a provided results folder. Inside the results folders a new project folder is created for this project, this folder has the full structure of the original project but only contains the pitest reports of the project. Collecting results can be done for many projects at once by using collect_results_projects.sh.

### Counting reactive methods mutation coverage
After collecting the pitest HTML result files, running <em>methods.py</em> with the results folder as input will count for each reactive method call (in Flux or Mono class) how many times they were killed, survived, timed_out, no_coverage, non_viable, memory_error, or run_error. The results are written to a CSV file. Counting methods can be done for many projects at once by using get_methods_projects.sh.

### Generating mutation coverage reports
After collecting the pitest HTML result files, runing <em>coverage.py</em> with the results folder as input generates a report of the the mutation coverage of all sub-projects of this project combined. The results are written to a CSV file. Generating reports can be done for many projects at once by using get_coverage_projects.sh.


## Tests of scripts
### collect.py
This code is tested by running it on a project with a known file structure and where the folder containing the newest results was known. After running the algorithm on the project the results folder contained the pitest reports of the correct timestamps with the expected folder structure.

### methods.py
This code is tested by running it on a project results folder (created by <em>collect.py</em>) and comparing its exported .csv to the statistics of the reactive results counted by hand. This matched exactly.

### coverage.py
This code is tested by manually checking all Project Summary index.html files in the results folder (created by <em>collect.py</em>) of a test project and comparing it to the exported .csv. The sum values is checked by comparing it to the manually added mutation coverage values of all projects.
