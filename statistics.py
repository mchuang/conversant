
from datetime import datetime

import pandas
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

from pandas import Series
from statsmodels.tsa.stattools import adfuller
import numpy as np

"""Simple read of datafile and returns data in DataFrame"""
"""Does not add in negatives values"""
def createDataSet(filename):
    f = open(filename, 'r')
    data = []
    for line in f:
        row = line.strip().split()
        if row[0] == 'Type':
            #For simplicity, just pretend Data center = Data
            columns = row[:4]
        elif row[0] == 'rtb.requests':
            if float(row[2]) < 0:
                continue
            dataType = row[3][-1]
            data.append([row[0], int(row[1]), float(row[2]), dataType])
        else:
            continue
    return pandas.DataFrame(columns=columns, data=data)

"""Runs the relevant statistic calculations"""
"""Only decided to run adfuller and a linear regression test"""
def basicStats(data):
    #linearRegressionStats(data, 'A')
    for key in data.groupby('Data').groups.keys():
        print('LOG FOR DATA CENTER %s' % key)
        linearRegressionStats(data, key)
        adfullerStats(data, key)

    print('LOG FOR DIFFERENCE OF TWO CENTERS')
    diff = adfullerDiffOfTwoTypes(data, 'S', 'I')
    xValues = []
    yValues = []
    for key in diff.keys():
        xValues.append([key])
        yValues.append(diff[key])
    linearRegressionStats2(xValues, yValues)

"""Standard linear regression model with train and predict"""
def linearRegressionStats(data, dataType):
    groupsByType = data.groupby('Data')
    indexes = groupsByType.groups[dataType]
    xValues = []
    yValues = []
    for index in indexes:
        xValues.append([data.get_value(index, 'Time')])
        yValues.append(int(data.get_value(index, 'Value')))
    
    linearReg = LinearRegression()
    xTrain = xValues[:-20]
    xPredict = xValues[-20:]
    yTrain = yValues[:-20]
    yPredict = yValues[-20:]
    linearReg.fit(xTrain, yTrain)

    print('Linear Regression for data center %s' % dataType)
    print('Coefficients: \n', linearReg.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"
          % np.mean((linearReg.predict(xPredict) - yPredict) ** 2))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % linearReg.score(xPredict, yPredict))

    # Plot outputs
    plt.xlabel('Time')
    plt.ylabel('Value')
    fig, ax = plt.subplots()
    fig.autofmt_xdate()

    temp = []
    for val in xPredict:
        temp.append([datetime.fromtimestamp(val[0])])
    plt.plot_date(temp, yPredict, 'o')

    start = xPredict[0][0]
    end = xPredict[-1][0]
    f = lambda x: linearReg.intercept_ + x*linearReg.coef_
    plt.plot_date([[datetime.fromtimestamp(start)], [datetime.fromtimestamp(end)]],
                  f([start, end]), '-')

    fig.savefig(dataType+'LinearRegression.png')
    plt.close()

"""Same as above but directly insert own values"""
"""Assume 20 values for prediction, remainder are for training"""
def linearRegressionStats2(xValues, yValues):
    linearReg = LinearRegression()
    xTrain = xValues[:-20]
    xPredict = xValues[-20:]
    yTrain = yValues[:-20]
    yPredict = yValues[-20:]
    linearReg.fit(xTrain, yTrain)

    print('Linear Regression Data')
    print('Coefficients: \n', linearReg.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"
          % np.mean((linearReg.predict(xPredict) - yPredict) ** 2))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % linearReg.score(xPredict, yPredict))

    plt.xlabel('Time')
    plt.ylabel('Value')
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    
    temp = []
    for val in xPredict:
        temp.append([datetime.fromtimestamp(val[0])])
    plt.plot_date(temp, yPredict, 'o')
    
    f = lambda x: linearReg.intercept_ + x*linearReg.coef_
    start = xPredict[0][0]
    end = xPredict[-1][0]
    plt.plot_date([[datetime.fromtimestamp(start)], [datetime.fromtimestamp(end)]],
                  f([start, end]), '-')
    
    fig.savefig('differenceLinearRegression.png')
    plt.close()

"""Function is to accept or reject hypothesis if time series is stationary
Solution towards detecting for periodic trends and if data has unit root
Refer to https://en.wikipedia.org/wiki/Augmented_Dickey%E2%80%93Fuller_test"""
def adfullerStats(data, dataType):
    groupsByType = data.groupby('Data')
    dataCenter = groupsByType.groups[dataType]

    #times = []
    #values = []
    pair = {}
    for index in dataCenter:
        pair[data.get_value(index, 'Time')] = int(data.get_value(index, 'Value'))
        #times.append(data.get_value(index, 'Time'))
        #values.append(int(data.get_value(index, 'Value')))

    result = adfuller(Series(pair))
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
            print('\t%s: %.3f' % (key, value))

"""Similar as above but partition data stream
by center to check for periods at certain times.
Sort indexes since that means sorted times."""
def adfullerStatsPartitioned(data, dataType, partition):
    groupsByType = data.groupby('Data')
    dataCenter = sorted(groupsByType.groups[dataType])
    print('Data Center %s' % dataType)
    for i in range(0, partition):
        pair = {}
        for j in range(i*partition, (i+1)*partition):
            index = dataCenter[j]
            pair[data.get_value(index, 'Time')] = int(data.get_value(index, 'Value'))
        
        result = adfuller(Series(pair))
        print('Partition %d' % i)
        print('p-value: %f' % result[1])

"""Applies adfuller on the difference of values between two data centers"""
def adfullerDiffOfTwoTypes(data, typeA, typeB):
    groupsByTime = data.groupby('Time')

    #Sort and add all data relevant to typeA and typeB
    dataAB = {}
    for time in groupsByTime.groups.keys():
        for index in groupsByTime.groups[time]:
            dataType = data.get_value(index, 'Data')
            value = data.get_value(index, 'Value')
            if dataType == typeA or dataType == typeB:
                if time not in dataAB.keys():
                    dataAB[time] = []
                dataAB[time].append([value, dataType])

    differences = {}
    for time in dataAB:
        if len(dataAB[time]) == 2:
            #Sort by data type to stay consistent
            temp = dataAB[time]
            temp.sort(key=lambda x: x[1])
            diff = temp[0][0] - temp[1][0]
            differences[time] = diff
        

    result = adfuller(Series(differences))
    print('Differences between {} and {}'.format(typeA, typeB))
    print('%s values with same timestamp' % len(differences.keys()))
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))

    return differences
            
"""Random models testing"""
def otherPotentialModels(data):
    groupsByType = data.groupby('Data')
    groupsByTime = data.groupby('Time')
    
    #Loop through types, then indexes to gather data for models
    for dataType in groupsByType.groups.keys():
        indexes = groupsByType.groups[dataType]
        xValues = []
        yValues = []
        for index in indexes:
            xValues.append([data.get_value(index, 'Time')])
            yValues.append(int(data.get_value(index, 'Value')))

        validation_size = 0.20
        seed = 7
        x_train, x_validation, y_train, y_validation = model_selection.train_test_split(
            xValues, yValues, test_size=validation_size, random_state=seed)

        #Random models to test out accuracy
        models = []
        models.append(('LR', LinearRegression()))
        models.append(('LogR', LogisticRegression()))
        models.append(('LDA', LinearDiscriminantAnalysis()))
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('CART', DecisionTreeClassifier()))
        models.append(('NB', GaussianNB()))
        models.append(('SVM', SVC()))
                
        scoring = 'accuracy'
        results = []
        names = []
        for name, model in models:
            kfold = model_selection.KFold(n_splits=10, random_state=seed)
            cv_results = model_selection.cross_val_score(model, x_train, y_train,
                                                         cv=kfold, scoring=scoring)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            print(msg)
        
