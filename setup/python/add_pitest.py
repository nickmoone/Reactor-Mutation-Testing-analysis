# Add Pitest plugin to pom.xml file of a project.

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


""" Add Pitest plugin from snippet_path to pom.xml at pom_path.
"""
def add_pitest_to_pom(pom_path, snippet_path):
    f = open(pom_path, "r")
    if "org.pitest" in f.read():
        exit("pitest is already in pom.xml file.")
    f.close()

    pom = ET.parse(pom_path)
    root = pom.getroot()

    namespace = root.tag.split('{')[1].split('}')[0]
    namespace_mapping = {'': namespace}
    ET.register_namespace('', namespace)

    build = root.find("build", namespace_mapping)
    if build is None:
        build = ET.SubElement(root, "build")

    plugins = build.find("plugins", namespace_mapping)
    if plugins is None:
        plugins = ET.SubElement(build, "plugins")

    snippet = ET.parse(snippet_path)
    plugin = snippet.getroot()

    plugins.append(plugin)

    ET.indent(pom, '    ')
    pom.write(pom_path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        project_folder = sys.argv[1]
        snippet_path = sys.argv[2]
    else:
        exit("Usage: python add_pitest_to_pom.py <project_folder> <snippet_path>")

    add_pitest_to_pom(get_pom_path(project_folder), snippet_path)
    
