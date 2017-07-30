import math

"""
The purpose of this function is to track calculate slopes and acceleration
and locate the minimas and maximas.
"""
def slopeMinimaMaxima(data):
    result = {}
    for dataType in data:
        slopes = []
        slopesByUnitRequest = []
        acceleration = []
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
                slopes.append([time, currSlope])
                slopesByUnitRequest.append([time, value-prevValue])
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
                    #Scale up acceleration by 10 for integer data
                    acc = 10* (currSlope-prevSlope) / (time-prevTime).total_seconds()
                    acceleration.append([time, acc])
                        #if currSlope < 0:
                            #acceleration.append([time, -1*helper(prevSlope, currSlope)])
                        #else:
                            #acceleration.append([time, helper(prevSlope, currSlope)])

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
                            'slopes': slopes, 'acceleration': acceleration,
                            'slopesByUnitRequest': slopesByUnitRequest}
        
    return result

"""Checks how much bigger num2 is of num1"""
def helper(num1, num2):
    return abs(num2) / abs(num1)

"""FUNCTIONS FOR SINGLE DATA CENTER ACROSS TIME"""

"""Logs all significant values of slope of bidding
Only notes increase in slope by factor of given value"""
def sigSlopeDetector(dataCenter, slopes, threshold):
    for time, value in slopes:
        #Assume slope of 100 is significant threshold in bidding
        if abs(int(value)) > threshold:
            print('Notice: Significant slope in bidding for data center {} by factor of {} at: {}'
                  .format(dataCenter, int(value), time.strftime('%c')))

"""Logs all significant values of acceleration of bidding
Only notes increase in acceleration by factor of given value
Ignores values <1 since that means slow down in bidding change"""
def sigAccelerationDetector(dataCenter, acceleration, threshold):
    for time, value in acceleration:
        #Assume acceleration of 10 is significant threshold in bidding
        if abs(int(value)) > threshold:
            print('Notice: Significant acceleration in bidding for data center {} by factor of {} at: {}'
                  .format(dataCenter, int(value), time.strftime('%c')))

"""FUNCTIONS FOR ACROSS TIME AND DATA CENTERS"""

"""Logs all common bid changes with slope variable.
Slope is rounded here for simplicity."""
def checkCommonSlopesByTimeStamp(data):
    result = {}
    for dataType in data:
        dataCenter = data[dataType]
        for time, slope in dataCenter['slopes']:
            if time not in result:
                result[time] = []
            result[time].append([int(slope), dataType])

    for time, items in sorted(result.items()):
        items.sort(key=lambda x: x[0])
        commonSlope = 0
        commonCenters = set()
        for slope, dataType in items:
            if len(commonCenters) == 0:
                commonCenters.add(dataType)
                commonSlope = slope  
                continue
            elif slope == commonSlope:
                commonCenters.add(dataType)
            else:
                if len(commonCenters) > 1 and slope != 0:
                    list(commonCenters).sort(key=lambda x: x)
                    print("Data centers {} share common slope of {} at time {}"
                          .format('-'.join(commonCenters), slope, time.strftime('%c')))
                    commonCenters = set()
                commonCenters.add(dataType)
                commonSlope = slope

        if len(commonCenters) > 1 and slope!= 0:
            list(commonCenters).sort(key=lambda x: x)
            print("Data centers {} share common slope of {} at time {}"
                  .format('-'.join(commonCenters), slope, time.strftime('%c')))

"""Same as common slope functin.
Logs all common bid changes with acceleration variable.
Acceleration is rounded here for simplicity."""
def checkCommonAccelerationByTimeStamp(data):
    result = {}
    for dataType in data:
        dataCenter = data[dataType]
        for time, acc in dataCenter['acceleration']:
            if time not in result:
                result[time] = []
            result[time].append([int(acc), dataType])

    for time, items in sorted(result.items()):
        items.sort(key=lambda x: x[0])
        commonAcc = 0
        commonCenters = set()
        for acc, dataType in items:
            if len(commonCenters) == 0:
                commonCenters.add(dataType)
                commonAcc = acc  
                continue
            elif acc == commonAcc:
                commonCenters.add(dataType)
            else:
                if len(commonCenters) > 1 and acc != 0:
                    list(commonCenters).sort(key=lambda x: x)
                    print("Data centers {} share common acceleration of {} at time {}"
                          .format('-'.join(commonCenters), acc, time.strftime('%c')))
                    commonCenters = set()
                commonCenters.add(dataType)
                commonAcc = acc

        if len(commonCenters) > 1 and acc != 0:
            list(commonCenters).sort(key=lambda x: x)
            print("Data centers {} share common acceleration of {} at time {}"
                  .format('-'.join(commonCenters), acc, time.strftime('%c')))

"""Same as common slope and acc functions
Logs all common values by timestamp.
Value is rounded here for simplicity."""
def checkCommonValuesByTimeStamp(data):
    result = {}
    for dataType in data:
        dataCenter = data[dataType]
        for time, value in dataCenter:
            if time not in result:
                result[time] = []
            result[time].append([int(value), dataType])

    for time, items in sorted(result.items()):
        items.sort(key=lambda x: x[0])
        commonValue = 0
        commonCenters = set()
        for value, dateType in items:
            if len(commonCenters) == 0:
                commonCenters.add(dataType)
                commonValue = value  
                continue
            elif value == commonValue:
                commonCenters.add(dataType)
            else:
                if len(commonCenters) > 1 and value != 0:
                    list(commonCenters).sort(key=lambda x: x)
                    print("Data centers {} share common value of {} at time {}"
                          .format('-'.join(commonCenters), value, time.strftime('%c')))
                    commonCenters = set()
                commonCenters.add(dataType)
                commonValue = value

        if len(commonCenters) > 1 and value!= 0:
            list(commonCenters).sort(key=lambda x: x)
            print("Data centers {} share common value of {} at time {}"
                  .format('-'.join(commonCenters), value, time.strftime('%c')))
  
                
            
            


            
    
                
        
