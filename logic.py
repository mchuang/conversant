from datetime import datetime
import matplotlib.pyplot as plt

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
            dataCenters[dataType].append([int(row[1]), float(row[2])])
        else:
            #for other request types?
            continue
    return dataCenters

#Organizes, manipulates, or removes data
def handleData(dataCenters):
    data = {}
    for dataType in dataCenters:
        dataCenter = dataCenters[dataType]

        xValues = []
        yValues = []
        for time, value in dataCenter:
            xValues.append(time)
            yValues.append(value)
    
        data[dataType] = [xValues, yValues]
    return data

def drawSimpleGraph(dataCenters, graphName):
    lineColors = ['k', 'y', 'm', 'c', 'r', 'g', 'b']
    assignedColors = {}
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid(True)
    for dataType in dataCenters:
        xValues, yValues = dataCenters[dataType]
        color = 'k' #default color
        if dataType in assignedColors:
            color = assignedColors[dataType]
        elif len(lineColors) > 0:
            color = lineColors.pop()
            assignedColors[dataType] = color

        plt.plot(xValues, yValues, color)
        
    plt.savefig(graphName)
    plt.show()

#Assume rtb = real time bids so value is money so it cannot be negative
#Also the negatives values heavily skewed the simple graph making it unreadable
def handleDataNoNegatives(dataCenters):
    data = {}
    for dataType in dataCenters:
        dataCenter = dataCenters[dataType]

        xValues = []
        yValues = []
        for time, value in dataCenter:
            if value < 0:
                continue
            else:
                xValues.append(time)
                yValues.append(value)
    
        data[dataType] = [xValues, yValues]
    return data
