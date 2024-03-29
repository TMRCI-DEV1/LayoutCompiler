# Author Rangachari Anand Copyright (C) 2021
# This is free software; you can redistribute it and/or modify it under the
# terms of version 2 of the GNU General Public License as published by the Free
# Software Foundation.

# Compare the original layout.xml with result of round trip through extract and compile

import xml.etree.ElementTree as ET
import argparse

def attributeMatches(original, updated, attributeName):
    if attributeName in original.attrib:
        if attributeName in updated.attrib:
            return original.attrib[attributeName] == updated.attrib[attributeName]
        else:
            return False
    else:
        if attributeName in updated.attrib:
            return False
        else:
            return True

def optionalTagMatches(original, updated, tagName):
    originalChild = original.find(tagName)
    updatedChild = updated.find(tagName)
    if originalChild == None:
        if updatedChild == None:
            return True
        else:
            return False
    else:
        if updatedChild == None:
            return False
        else:
            return originalChild.text == updatedChild.text

def optionalTagMatchesByPattern(original, updated, pattern):
    t = original.findall(pattern)
    u = updated.findall(pattern)
    if len(t) != len(u):
        return False
    if len(t) == 1 and len(u) == 1:
        originalChild = t[0]
        updatedChild = u[0]
        return originalChild.text == updatedChild.text
    return len(t) == 0 and len(u) == 0

def getSensorBySystemName(root, systemName):
    queryString = ".sensors/sensor/systemName[.='%s']/.." % systemName
    sensors = root.findall(queryString)
    if len(sensors) != 1:
        return None
    else:
        return sensors[0]

def getTurnoutBySystemName(root, systemName):
    queryString = ".turnouts/turnout/systemName[.='%s']/.." % systemName
    turnouts = root.findall(queryString)
    if len(turnouts) != 1:
        return None
    else:
        return turnouts[0]

def getLightBySystemName(root, systemName):
    queryString = ".lights/light/systemName[.='%s']/.." % systemName
    lights = root.findall(queryString)
    if len(lights) != 1:
        return None
    else:
        return lights[0]

def getSignalheadBySystemName(root, systemName):
    queryString = ".signalheads/signalhead/systemName[.='%s']/.." % systemName
    signalheads = root.findall(queryString)
    if len(signalheads) != 1:
        return None
    else:
        return signalheads[0]

def getSignalmastBySystemName(root, systemName):
    queryString = ".signalmasts/signalmast/systemName[.='%s']/.." % systemName
    signalheads = root.findall(queryString)
    if len(signalheads) != 1:
        return None
    else:
        return signalheads[0]
    
def getReporterBySystemName(root, systemName):
    queryString = ".reporters/reporter/systemName[.='%s']/.." % systemName
    reporters = root.findall(queryString)
    if len(reporters) != 1:
        return None
    else:
        return reporters[0]

def getAllSensors(root):
    queryString = '.sensors/sensor'
    return root.findall(queryString)

def getAllTurnouts(root):
    queryString = '.turnouts/turnout'
    return root.findall(queryString)

def getAllLights(root):
    queryString = '.lights/light'
    return root.findall(queryString)

def getAllSignalheads(root):
    queryString = '.signalheads/signalhead'
    return root.findall(queryString)

def getAllSignalmasts(root):
    queryString = '.signalmasts/signalmast'
    return root.findall(queryString)

def getAllBlocks(root):
    queryString = '.blocks/block'
    return root.findall(queryString)

def getAllReporters(root):
    queryString = '.reporters/reporter'
    return root.findall(queryString)

def sensorMatches(original, updated):
    if not attributeMatches(original, updated, 'inverted'):
        return False
    if not optionalTagMatches(original, updated, 'userName'):
        return False
    return optionalTagMatches(original, updated, 'comment')

def sensorsMatch(originalRoot, updatedRoot):
    originalSensors = getAllSensors(originalRoot)
    updatedSensors = getAllSensors(updatedRoot)
    if len(originalSensors) != len(updatedSensors):
        print('Error: number of sensors do not match')
        originalSensorSystemNames = set()
        updatedSensorSystemNames = set()
        for x in originalSensors:
            originalSensorSystemNames.add(x.find('systemName').text)
        for x in updatedSensors:
            updatedSensorSystemNames.add(x.find('systemName').text)
        difference = originalSensorSystemNames.symmetric_difference(updatedSensorSystemNames)
        print(difference)
        return False
    print('Num sensors matches', len(originalSensors))
    for originalSensor in originalSensors:
        originalSystemName = originalSensor.find('systemName').text
        print('Checking sensor ', originalSystemName)
        updatedSensor = getSensorBySystemName(updatedRoot, originalSystemName)
        if updatedSensor == None:
            print('Error missing sensor in update: ', originalSystemName)
            return False
        elif not sensorMatches(originalSensor, updatedSensor):
            print('Sensor mismatch', originalSystemName)
            return False
    return True

def turnoutMatches(original, updated):
    if not attributeMatches(original, updated, 'feedback'):
        return False
    if not attributeMatches(original, updated, 'inverted'):
        return False
    if not attributeMatches(original, updated, 'automate'):
        return False
    if not attributeMatches(original, updated, 'controlType'):
        return False
    if not attributeMatches(original, updated, 'sensor1'):
        return False
    if not attributeMatches(original, updated, 'sensor2'):
        return False
    if not optionalTagMatches(original, updated, 'userName'):
        return False
    if not optionalTagMatches(original, updated, 'comment'):
        return False
    if not optionalTagMatches(original, updated, 'divergingSpeed'):
        return False
    if not optionalTagMatches(original, updated, 'straightSpeed'):
        return False
    return True
    

def turnoutsMatch(originalRoot, updatedRoot):
    originalTurnouts = getAllTurnouts(originalRoot)
    updatedTurnouts = getAllTurnouts(updatedRoot)
    if len(originalTurnouts) != len(updatedTurnouts):
        print('Number of turnouts do not match')
        return False
    print('Num turnouts matches', len(originalTurnouts))
    for originalTurnout in originalTurnouts:
        originalSystemName = originalTurnout.find('systemName').text
        print('Checking turnout', originalSystemName)
        updatedTurnout = getTurnoutBySystemName(originalRoot, originalSystemName)
        if updatedTurnout == None:
            print('Missing updated turnout')
            return False
        elif not turnoutMatches(originalTurnout, updatedTurnout):
            print('Turnout mismatch', originalSystemName)
            return False
    return True

def lightMatches(originalLight, updatedLight):
    if not attributeMatches(originalLight, updatedLight, 'minIntensity'):
        return False
    if not attributeMatches(originalLight, updatedLight, 'maxIntensity'):
        return False
    if not attributeMatches(originalLight, updatedLight, 'transitionTime'):
        return False
    if not optionalTagMatches(originalLight, updatedLight, 'userName'):
        return False
    if not optionalTagMatches(originalLight, updatedLight, 'comment'):
        return False
    originalLightcontrol = originalLight.find('lightcontrol')
    updatedLightcontrol = updatedLight.find('lightcontrol')
    if originalLightcontrol is None:
        if updatedLightcontrol is None:
            pass
        else:
            return False
    else:
        if updatedLightcontrol is None:
            return False
        else:
            if not attributeMatches(originalLightcontrol, updatedLightcontrol, 'controlType'):
                return False
            if not attributeMatches(originalLightcontrol, updatedLightcontrol, 'controlSensor'):
                return False
            if not attributeMatches(originalLightcontrol, updatedLightcontrol, 'sensorSense'):
                return False
    return True

def reporterMatches(originalReporter, updatedReporter):
    if not optionalTagMatches(originalReporter, updatedReporter, 'userName'):
        return False
    if not optionalTagMatches(originalReporter, updatedReporter, 'comment'):
        return False
    return True

def lightsMatch(originalRoot, updatedRoot):
    originalLights = getAllLights(originalRoot)
    updatedLights = getAllLights(updatedRoot)
    numOriginalLights = len(originalLights)
    numUpdatedLights = len(updatedLights)
    if numOriginalLights != numUpdatedLights:
        print('Number of lights do not match', numOriginalLights, numUpdatedLights)
        originalSet = set(originalLights)
        updatedSet = set(updatedLights)
        differenceSet = originalSet.difference(updatedSet)
        for e in differenceSet:
            print(e.find('systemName').text)
        return False
    print('Num lights matches', len(originalLights))
    for originalLight in originalLights:
        originalSystemName = originalLight.find('systemName').text
        print('Checking light', originalSystemName)
        updatedLight = getLightBySystemName(originalRoot, originalSystemName)
        if updatedLight == None:
            print('Missing updated light')
            return False
        elif not lightMatches(originalLight, updatedLight):
            print('Light mismatch', originalSystemName)
            return False
    return True

def reportersMatch(originalRoot, updatedRoot):
    originalReporters = getAllReporters(originalRoot)
    updatedReporters = getAllReporters(updatedRoot)
    numOriginalReporters = len(originalReporters)
    numUpdatedReporters = len(updatedReporters)
    if numOriginalReporters != numUpdatedReporters:
        print('Number of reporters do not match', numOriginalReporters, numUpdatedReporters)
        originalSet = set(originalReporters)
        updatedSet = set(updatedReporters)
        differenceSet = originalSet.difference(updatedSet)
        for e in differenceSet:
            print(e.find('systemName').text)
        return False
    print('Num reporters matches', len(originalReporters))
    for originalReporter in originalReporters:
        originalSystemName = originalReporter.find('systemName').text
        print('Checking reporter', originalSystemName)
        updatedReporter = getReporterBySystemName(originalRoot, originalSystemName)
        if updatedReporter == None:
            print('Missing updated reporter')
            return False
        elif not reporterMatches(originalReporter, updatedReporter):
            print('Reporter mismatch', originalSystemName)
            return False
    return True
    

def signalheadMatches(originalSignalhead, updatedSignalhead):
    if not attributeMatches(originalSignalhead, updatedSignalhead, 'class'):
        return False
    if not optionalTagMatches(originalSignalhead, updatedSignalhead, 'userName'):
        return False
    if not optionalTagMatches(originalSignalhead, updatedSignalhead, 'comment'):
        return False
    if not optionalTagMatchesByPattern(originalSignalhead, updatedSignalhead, "./turnoutname[@defines='green']"):
        return False
    if not optionalTagMatchesByPattern(originalSignalhead, updatedSignalhead, "./turnoutname[@defines='yellow']"):
        return False
    if not optionalTagMatchesByPattern(originalSignalhead, updatedSignalhead, "./turnoutname[@defines='red']"):
        return False
    if not optionalTagMatchesByPattern(originalSignalhead, updatedSignalhead, "./appearance[@defines='thrown']"):
        return False
    if not optionalTagMatchesByPattern(originalSignalhead, updatedSignalhead, "./appearance[@defines='closed']"):
        return False
    if not optionalTagMatchesByPattern(originalSignalhead, updatedSignalhead, "./turnoutname[@defines='aspect']"):
        return False
    return True

def signalHeadsMatch(originalRoot, updatedRoot):
    originalSignalheads = getAllSignalheads(originalRoot)
    updatedSignalheads = getAllSignalheads(updatedRoot)
    numOriginalSignalheads = len(originalSignalheads)
    numUpdatedSignalheads = len(updatedSignalheads)
    if numOriginalSignalheads != numUpdatedSignalheads:
        print('Number of signalheads do not match', numOriginalSignalheads, numUpdatedSignalheads)
        originalSet = set(originalSignalheads)
        updatedSet = set(updatedSignalheads)
        differenceSet = originalSet.difference(updatedSet)
        for e in differenceSet:
            print(e.find('systemName').text)
        return False
    print('Num signalheads match', numOriginalSignalheads)
    for originalSignalhead in originalSignalheads:
        originalSystemName = originalSignalhead.find('systemName').text
        print('Checking signalhead', originalSystemName)
        updatedSignalhead = getSignalheadBySystemName(originalRoot, originalSystemName)
        if updatedSignalhead is None:
            print('Missing updated signalhead')
            return False
        elif not signalheadMatches(originalSignalhead, updatedSignalhead):
            print('Signalhead mismatch', originalSystemName)
            return False
    return True

def signalmastMatches(originalSignalmast, updatedSignalmast):
    if not optionalTagMatches(originalSignalmast, updatedSignalmast, 'userName'):
        return False
    if not optionalTagMatches(originalSignalmast, updatedSignalmast, 'comment'):
        return False
    # This is required because optionalTagMatches does not check attributes of unlit
    originalUnlit = originalSignalmast.find('unlit')
    updatedUnlit = updatedSignalmast.find('unlit')
    if originalUnlit is None:
        if updatedUnlit is None:
            pass
        else:
            return False
    else:
        if updatedUnlit is None:
            return False
        else:
            if originalUnlit.attrib['allowed'] != updatedUnlit.attrib['allowed']:
                return False
    originalDisabledAspects = originalSignalmast.find('disabledAspects')
    updatedDisabledAspects = updatedSignalmast.find('disabledAspects')
    if originalDisabledAspects is None:
        if updatedDisabledAspects is None:
            pass
        else:
            return False
    else:
        if updatedDisabledAspects is None:
            return False
        else:
            oda = set()
            uda = set()
            for e in originalDisabledAspects:
                oda.add(e.text)
            for e in updatedDisabledAspects:
                uda.add(e.text)
            return oda == uda
    
    return True

def signalmastsMatch(originalRoot, updatedRoot):
    originalSignalmasts = getAllSignalmasts(originalRoot)
    updatedSignalmasts = getAllSignalmasts(updatedRoot)
    numOriginalSignalmasts = len(originalSignalmasts)
    numUpdatedSignalmasts = len(updatedSignalmasts)
    if numOriginalSignalmasts != numUpdatedSignalmasts:
        print('Number of signalmasts do not match', numOriginalSignalmasts, numUpdatedSignalmasts)
        originalSet = set(originalSignalmasts)
        updatedSet = set(updatedSignalmasts)
        differenceSet = originalSet.difference(updatedSet)
        for e in differenceSet:
            print(e.find('systemName').text)
        return False
    print('Num signalheads match', numOriginalSignalmasts)
    for originalSignalmast in originalSignalmasts:
        originalSystemName = originalSignalmast.find('systemName').text
        print('Checking signalmast', originalSystemName)
        updatedSignalmast = getSignalmastBySystemName(originalRoot, originalSystemName)
        if updatedSignalmast is None:
            print('Missing updated signalhead')
            return False
        elif not signalmastMatches(originalSignalmast, updatedSignalmast):
            print('Signalmatch mismatch', originalSystemName)
            return False
    return True


def blocksMatch(originalRoot, updatedRoot):
    originalBlocks = getAllBlocks(originalRoot)
    updatedBlocks = getAllBlocks(updatedRoot)
    numOriginalBlocks = len(originalBlocks)
    numUpdatedBlocks = len(updatedBlocks)
    if numOriginalBlocks != numUpdatedBlocks:
        print('Number of blocks do not match', numOriginalBlocks, numUpdatedBlocks)
    # We can use this simplified approach for comparison because there is only one 
    # <blocks> element and the blocks contained therein must be in the same order.
    for (originalBlock, updatedBlock) in zip(originalBlocks, updatedBlocks):
        print('Checking block', originalBlock.attrib['systemName'])
        if not optionalTagMatches(originalBlock, updatedBlock, 'systemName'):
            return False
        if not attributeMatches(originalBlock, updatedBlock, 'systemName'):
            return False
        if not attributeMatches(originalBlock, updatedBlock, 'length'):
            return False
        if not attributeMatches(originalBlock, updatedBlock, 'curve'):
            return False
        if not optionalTagMatches(originalBlock, updatedBlock, 'permissive'):
            return False
        if not optionalTagMatches(originalBlock, updatedBlock, 'occupancySensor'):
            return False
        if not optionalTagMatches(originalBlock, updatedBlock, 'speed'):
            return False
    return True

def main(args):
    print('Original file: ', args.originalFile, 'Updated file:', args.updatedFile)
    originalTree = ET.parse(args.originalFile)
    originalRoot = originalTree.getroot()
    updatedTree = ET.parse(args.updatedFile)
    updatedRoot = updatedTree.getroot()
    if not sensorsMatch(originalRoot, updatedRoot):
        return
    if not turnoutsMatch(originalRoot, updatedRoot):
        return
    if not lightsMatch(originalRoot, updatedRoot):
        return
    if not reportersMatch(originalRoot, updatedRoot):
        return
    if not signalHeadsMatch(originalRoot, updatedRoot):
        return
    if not signalmastsMatch(originalRoot, updatedRoot):
        return
    if not blocksMatch(originalRoot, updatedRoot):
        return
    print('Test passed')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare the original layout.xml with result of round trip through extract and compile')
    parser.add_argument('originalFile', type=str, help='JMRI layout description file in XML format')
    parser.add_argument('updatedFile', type=str, help='XML file result of running round trip extract followed by compile')
    args = parser.parse_args()

    main(args)