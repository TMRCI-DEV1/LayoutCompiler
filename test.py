# Author Rangachari Anand Copyright (C) 2021
# This is free software; you can redistribute it and/or modify it under the
# terms of version 2 of the GNU General Public License as published by the Free
# Software Foundation.

# Compare the original layout.xml with result of round trip through extract and compile

import xml.etree.ElementTree as ET
import csv
import re
import argparse

def getSensorBySystemName(root, systemName):
    queryString = ".sensors/sensor/systemName[.='%s']/.." % systemName
    sensors = root.findall(queryString)
    return sensors[0]

def main(args):
    print(args.layoutFile)
    print(args.updatedLayoutFile)
    originalTree = ET.parse(args.layoutFile)
    originalRoot = originalTree.getroot()
    updatedTree = ET.parse(args.updatedLayoutFile)
    updatedRoot = updatedTree.getroot()


    sensorX = getSensorBySystemName(originalRoot, 'C3S4010')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare the original layout.xml with result of round trip through extract and compile')
    parser.add_argument('layoutFile', type=str, help='JMRI layout description file in XML format')
    parser.add_argument('updatedLayoutFile', type=str, help='XML file result of running round trip extract followed by compile')
    args = parser.parse_args()

    main(args)