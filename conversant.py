import sys, pdb
from logic import *

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit()
    else:
        data = readData(sys.argv[1])
        drawGraph(data)
        

            
