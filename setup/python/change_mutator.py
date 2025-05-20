# Change mutator used by Pitest plugin in pom.xml of a project.

import os
import sys

import xml.etree.ElementTree as ET

""" Get pom.xml from project at project_folder.
"""
def get_pom_path(project_folder):
    pom_path = os.path.join(project_folder, "pom.xml")
    if not os.path.exists(pom_path):
        exit("pom.xml file does not exist in the project folder:\n" + project_folder)
    return pom_path

""" Change old_mutator to new_mutator used by Pitest in pom.xml at pom_path.
"""
def change_mutator(pom_path, old_mutator, new_mutator):
    f = open(pom_path, "r")
    if old_mutator not in f.read():
        exit("old_mutator is not in pom.xml file.")
    f.close()

    pom = ET.parse(pom_path)
    root = pom.getroot()

    namespace = root.tag.split('{')[1].split('}')[0]
    namespace_mapping = {'': namespace}
    ET.register_namespace('', namespace)

    build = root.find("build", namespace_mapping)
    if build is None:
        exit("pom.xml does not contain a build tag")

    plugins = build.find("plugins", namespace_mapping)
    if plugins is None:
        exit("pom.xml does not contain a plugins tag")

    for plugin in plugins:
        groupId = plugin.find("groupId", namespace_mapping)
        if groupId is not None and groupId.text == "org.pitest":
            configuration = plugin.find("configuration", namespace_mapping)
            if configuration is None:
                exit("Pitest plugin in pom.xml does not contain a configuration tag")
            mutators = configuration.find("mutators", namespace_mapping)
            if mutators is None:
                exit("Pitest plugin in pom.xml does not contain a mutators tag")
            for mutator in mutators:
                if mutator.text == old_mutator:
                    mutator.text = new_mutator
                    break

    ET.indent(pom, '    ')
    pom.write(pom_path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        project_folder = sys.argv[1]
        old_mutator = sys.argv[2]
        new_mutator = sys.argv[3]
    else:
        exit("Usage: python change_mutator.py <project_folder> <old_mutator> <new_mutator")

    change_mutator(get_pom_path(project_folder), old_mutator, new_mutator)
    
