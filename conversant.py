import sys
import handler, graph, analysis, statistics

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error: Execute command in format 'python conversant.py [datafile]'")
        sys.exit()
    else:
        """Simple data handling for general use graphs"""
        data = handler.readData(sys.argv[1])
        simpleData = handler.handleData(data)
        graph.drawGraph(simpleData, 'simpleGraph.png')
        noNegData = handler.rmNegatives(data)
        graph.drawGraph(noNegData, 'noNegatives.png')
        graphData = handler.setAsideNegatives(data)
        graph.drawGraph(graphData, 'simplify.png')

        """Primary pattern/trend analysis"""
        dataset = statistics.createDataSet(sys.argv[1])
        statistics.basicStats(dataset)
        

            
