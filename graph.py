import matplotlib.dates as mdates
import matplotlib.pyplot as plt

def drawSimpleGraph(data, graphName):
    lineColors = ['k', 'y', 'm', 'c', 'r', 'g', 'b']
    assignedColors = {}
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid(True)
    fig, ax = plt.subplots()
    #ax.fmt_xdata = mdates.DateFormatter('%m-%d %H:00')
    fig.autofmt_xdate()
    for dataType in data:
        xValues, yValues = data[dataType]
            
        color = 'k' #default color
        if dataType in assignedColors:
            color = assignedColors[dataType]
        elif len(lineColors) > 0:
            color = lineColors.pop()
            assignedColors[dataType] = color

        xValues = mdates.date2num(xValues)
        plt.plot_date(xValues, yValues, color)

    plt.savefig(graphName)

def drawFinalGraph(data, graphName):
    lineColors = ['k', 'y', 'm', 'c', 'r', 'g', 'b']
    assignedColors = {}
    
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid(True)
    fig, ax = plt.subplots()
    #ax.fmt_xdata = mdates.DateFormatter('%m-%d %H:00')
    fig.autofmt_xdate()

    negatives = None
    for dataType in data:
        if dataType == 'negative':
            negatives = data[dataType]
            continue
            
        xValues, yValues = data[dataType]
            
        color = 'k' #default color
        if dataType in assignedColors:
            color = assignedColors[dataType]
        elif len(lineColors) > 0:
            color = lineColors.pop()
            assignedColors[dataType] = color

        xValues = mdates.date2num(xValues)
        plt.plot_date(xValues, yValues, color)

    if negatives:
        for xValue, yValue, dataType in negatives:
            color = assignedColors[dataType]
            plt.axvline(x=xValue, color=color, linestyle='--')

    fig = plt.gcf()
    fig.set_size_inches(30, 10)
    fig.savefig(graphName, dpi=200)    
    #plt.savefig(graphName)
    
