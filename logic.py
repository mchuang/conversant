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
        else:
            dataType = row[3][-1]
            if dataType not in dataCenters:
                dataCenters[dataType] = []
            dataCenters[dataType].append([row[1], row[2]])

    return dataCenters

def drawGraph(dataCenters):
    #Plots up to 7 data centers
    lineColors = ['k', 'y', 'm', 'c', 'r', 'g', 'b']
    assignedColors = {}
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid(True)
    for dataType in dataCenters:
        dataCenter = dataCenters[dataType]
        color = 'k' #default color
        if dataType in assignedColors:
            color = assignedColors[dataType]
        elif len(lineColors) > 0:
            color = lineColors.pop()
            assignedColors[dataType] = color

        xValues = []
        yValues = []
        for dataPair in dataCenter:
            time = dataPair[0]
            value = dataPair[1]
            xValues.append(time)
            yValues.append(value)
            #date = datetime.fromtimestamp(time).strftime('%c')
        plt.plot(xValues, yValues, color)
        
    plt.savefig("simpleGraph.png")
    plt.show()
