import sys, pdb
from logic import *

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit()
    else:
        data = readData(sys.argv[1])
        #nativeData = handleData(data)
        #drawSimpleGraph(nativeData, 'simpleGraph.png')
        noNegatives = handleDataNoNegatives(data)
        drawSimpleGraph(noNegatives, 'noNegatives.png')
        

            
