import sys, pdb
import handler, graph, analysis, statistics

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit()
    else:
        data = handler.readData(sys.argv[1])
        simpleData = handler.handleData(data)
        graph.drawSimpleGraph(simpleData, 'simpleGraph.png')
        noNegData = handler.rmNegatives(data)
        graph.drawSimpleGraph(noNegData, 'noNegatives.png')
        graphData = handler.setAsideNegatives(data)
        graph.drawFinalGraph(graphData, 'simplify.png')
        
        dataset = statistics.createDataSet(sys.argv[1])
        statistics.basicStats(dataset)
        

        """
        analysisData = analysis.slopeMinimaMaxima(data)
        for dataType in analysisData:
            dataCenter = analysisData[dataType]
            print("Log for data center {}".format(dataType))
            print("Absolute smallest value is {} at time {}"
                  .format(dataCenter['absMin'][1], dataCenter['absMin'][0].strftime('%c')))
            print("Absolute largest  value is {} at time {}"
                  .format(dataCenter['absMax'][1], dataCenter['absMax'][0].strftime('%c')))
            analysis.sigSlopeDetector(dataType, dataCenter['slopes'], 100)
            analysis.sigAccelerationDetector(dataType, dataCenter['acceleration'], 10)
        analysis.checkCommonValuesByTimeStamp(data)
        analysis.checkCommonSlopesByTimeStamp(analysisData)
        analysis.checkCommonAccelerationByTimeStamp(analysisData)
        """
            

            
