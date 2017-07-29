from datetime import datetime

"""Standard read file row by row."""
def readData(data):
    dataCenters = {}
    
    f = open(data, 'r')
    for line in f:
        row = line.strip().split()
        if row[0] == 'Type':
            #First row should just be Type, Time, Value, Data center
            continue
        elif row[0] == 'rtb.requests':
            dataType = row[3][-1]
            if dataType not in dataCenters:
                dataCenters[dataType] = []
            dataCenters[dataType].append([datetime.fromtimestamp(int(row[1])), float(row[2])])
        else:
            #ignore other request types?
            continue
    return dataCenters  

"""Organizes a simple data structure of given data"""
def handleData(data):
    result = {}
    for dataType in data:
        dataCenter = data[dataType]

        xValues = []
        yValues = []
        for time, value in dataCenter:
            xValues.append(time)
            yValues.append(value)
    
        data[dataType] = [xValues, yValues]
    return result

"""Assume rtb = real time bids so value is money so it cannot be negative.
Also the negatives values heavily skewed the simple graph making it unreadable"""
def rmNegatives(data):
    result = {}
    for dataType in data:
        dataCenter = data[dataType]

        xValues = []
        yValues = []
        for time, value in dataCenter:
            if value < 0:
                continue
            else:
                xValues.append(time)
                yValues.append(value)
    
        result[dataType] = [xValues, yValues]
    return result

"""Similar as rmNegatives but make negatives its own data set"""
def setAsideNegatives(data):
    result = {}
    negatives = []
    
    for dataType in data:
        dataCenter = data[dataType]
        xValues = []
        yValues = []
        for time, value in dataCenter:
            if value < 0:
                negatives.append([time, value, dataType])
            else:
                xValues.append(time)
                yValues.append(value)
    
        result[dataType] = [xValues, yValues]

    result['negative'] = negatives
    
    return result

def gatherNegatives(data):
    result = {}
    for dataType in data:
        dataCenter = data[dataType]
        for time, value in dataCenter:
            if value < 0:
                negatives.append([time, value, dataType])

    result['negative'] = negatives
    
    return result

"""Organizes data by timestamp rather than data center"""
def organizeByTimeStamp(data):
    result = {}
    for dataType in data:
        dataCenter = data[dataType]
        for time, value in dataCenter:
            if time not in result:
                result[time] = []
            result[time].append([value, dataType])

    return result


