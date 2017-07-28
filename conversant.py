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
            analysis.logSlopeDetector(dataType, dataCenter['slopes'])
        graphData = handler.setAsideNegatives(data)
        graph.drawFinalGraph(graphData, 'final.png')
        
        

            
