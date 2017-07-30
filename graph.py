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

    lbls = []
    for dataType in data:
        xValues, yValues = data[dataType]
            
        color = 'k' #default color
        if dataType in assignedColors:
            color = assignedColors[dataType]
        elif len(lineColors) > 0:
            color = lineColors.pop()
            assignedColors[dataType] = color

        xValues = mdates.date2num(xValues)
        lbl, = plt.plot_date(xValues, yValues, color, label=dataType)
        lbls.append(lbl)
        
    plt.legend(handles=lbls)
    plt.savefig(graphName)
    plt.close()

def drawFinalGraph(data, graphName):
    lineColors = ['k', 'y', 'm', 'c', 'r', 'g', 'b']
    assignedColors = {}
    
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid(True)
    fig, ax = plt.subplots()
    #ax.fmt_xdata = mdates.DateFormatter('%m-%d %H:00')
    fig.autofmt_xdate()

    lbls = []
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
        lbl, = plt.plot_date(xValues, yValues, color, label=dataType)
        lbls.append(lbl)

    plt.legend(handles=lbls)
    if negatives:
        for xValue, yValue, dataType in negatives:
            color = assignedColors[dataType]
            plt.axvline(x=xValue, color=color, linestyle='--')

    fig = plt.gcf()
    fig.set_size_inches(30, 10)
    fig.savefig(graphName, dpi=200)
    plt.close()
    #plt.savefig(graphName)
    
