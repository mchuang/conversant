import math

"""
The purpose of this function is to track extreme changes
in slope and locate the minimas and maximas.
"""
def slopeMinimaMaxima(data):
    result = {}
    for dataType in data:
        slopeChanges = []
        localMin = []
        localMax = []
        absMin = absMax = None
        prevPair = None
        prevSlope = None
        dataCenter = data[dataType]
        for time, value in dataCenter:
            if value < 0: continue
            
            if prevPair:
                prevTime, prevValue = prevPair
                currSlope = (value-prevValue) / (time-prevTime).total_seconds()

                #Assume start of data stream is localMin/Max
                if len(localMin) == 0 and len(localMax) == 0:
                    if currSlope > 0:
                        localMax.append([time, value])
                    elif currSlope < 0:
                        localMin.append([time, value])
                
                if prevSlope:
                    if currSlope * prevSlope < 0:
                        if prevSlope < 0:
                            #this should signify local minima at this point 
                            localMin.append([time, value])
                            #update potential absMin
                            if absMin[1] > prevValue:
                                absMin = prevPair
                        else:
                            #similar to minima but for maxima
                            localMax.append([time, value])
                            if absMax[1] < prevValue:
                                absMax = prevPair
                        slopeChanges.append([time, 0])
                    else:
                        if prevSlope < 0:
                            slopeChanges.append([time, -1*helper(prevSlope, currSlope)])
                        else:
                            slopeChanges.append([time, helper(prevSlope, currSlope)])
                #Update for next round of comparison
                prevPair = time, value
                prevSlope = currSlope
            else:
                prevPair = time, value
                absMin = time, value
                absMax = time, value

        #Assume end of data stream is localMin/Max
        if currSlope > 0:
            localMax.append([time, value])
            if absMax[1] < prevValue:
                absMax = prevPair
        elif currSlope < 0:
            localMin.append([time, value])
            if absMin[1] > prevValue:
                absMin = prevPair

        result[dataType] = {'min': localMin, 'max': localMax,
                            'absMin': absMin, 'absMax': absMax,
                            'slopes': slopeChanges}
        
    return result

"""Checks how much bigger num1 is of num2"""
def helper(num1, num2):
    return abs(num1) / abs(num2)

"""Logs all significant changes in rate of bidding"""
def logSlopeDetector(dataCenter, slopes):
    for time, slope in slopes:
        if slope > 0: sign = 'downward'
        elif slope < 0: sign = 'upward  '
        else: continue
        value = int(math.log(abs(slope)))
        if value >= 3:
            print('Notice: Significant change for data center {} at {} times the rate {} at time: {}'.format(dataCenter, value, sign, time.strftime('%c')))
            
    
                
        
