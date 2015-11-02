
initial = {}
current = {'progress': {'completion': None, 'printTimeLeft': None, 'printTime': None, 'filepos': None}, 'state': {'text': 'None', 'flags': {'operational': False, 'paused': False, 'printing': False, 'sdReady': False, 'error': False, 'ready': False, 'closedOrError': True}}, 'currentZ': None, 'job': {'estimatedPrintTime': None, 'file': {'origin': None, 'date': None, 'name': None, 'size': None}, 'filament': {'volume': None, 'length': None}, 'lastPrintTime': None}, 'offsets': {}}

def setCurrentData(data):
    global current
    current = data

def getCurrentData():
    global current
    return current
