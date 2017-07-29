import sys, pdb
import handler, graph, analysis

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit()
    else:
        data = handler.readData(sys.argv[1])
        #data = handler.handleData(data)
        #graph.drawSimpleGraph(data, 'simpleGraph.png')
        #data = handler.rmNegatives(data)
        #graph.drawSimpleGraph(data, 'noNegatives.png')
        
        analysisData = analysis.slopeMinimaMaxima(data)
        for dataType in analysisData:
            dataCenter = analysisData[dataType]
            print("Log for data center {}".format(dataType))
            print("Absolute smallest value is {} at time {}"
                  .format(dataCenter['absMin'][1], dataCenter['absMin'][0].strftime('%c')))
            print("Absolute largest  value is {} at time {}"
                  .format(dataCenter['absMax'][1], dataCenter['absMax'][0].strftime('%c')))
            analysis.sigAccelerationDetector(dataType, dataCenter['acceleration'])
        #analysis.checkCommonValuesByTimeStamp(data)
        #analysis.checkCommonSlopesByTimeStamp(analysisData)
        #analysis.checkCommonAccelerationByTimeStamp(analysisData)
        graphData = handler.setAsideNegatives(data)
        graph.drawFinalGraph(graphData, 'final.png')
        
        

            
