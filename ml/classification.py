# Patryk Kośmider s16863
# Krzysztof Marek s16663
# 
# Dataset -> http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# The Wine Quality Dataset involves predicting the quality of white wines on a scale given chemical measures of each wine.
# 
# Problem:
# A classification problem is when the output variable is a category (basically 'yes' or 'no').
# A classification model attempts to draw some conclusion from observed values.
# Given one or more inputs a classification model will try to predict the value of one or more outcomes.
# 
# Usage:
# python classification.py `test_size`

import sys

import numpy
from numpy.lib.function_base import average

from tabulate import tabulate

from sklearn import metrics

from sklearn.model_selection import train_test_split

from sklearn.svm import SVC

from sklearn.neural_network import MLPClassifier

def get_SVC():
    """ 
        Helper returning standard classification engine.
        
        Returns: 
            SVC: C-Support Vector classification engine
    """
    return SVC(random_state = 1)

def get_MLP():
    """ 
        Helper returning neural classification engine.
        
        Returns: 
            MLPClassifier: Multi-Layer Perceptron classification engine
    """
    return MLPClassifier(activation = 'logistic', hidden_layer_sizes = (12), max_iter = 1000, learning_rate = 'adaptive', random_state = 1)

def get_BigMLP():
    """ 
        Helper returning neural classification engine.
        
        Returns: 
            MLPClassifier: Multi-Layer Perceptron classification engine
    """
    return MLPClassifier(activation = 'logistic', hidden_layer_sizes = (240, 120, 12), max_iter = 1000, learning_rate = 'adaptive', random_state = 1)

def testify(inputs, targets, test_size, c_getter):
    """ 
        Performs training and testing on datasets with given size of test sample.

        Parameters:
            inputs (array): Array containg inputs for train function.
            targets (array): Array containg targets for train function.
            test_size (float): Represents the proportion of the dataset to include in the train split in range (0.0, 1.0).
    """
    print(f'  Training and predicting for {test_size * 100}% ({round(test_size * len(inputs))}) test samples')
    X_train, X_test, y_train, y_test = train_test_split(inputs, targets, test_size = test_size)

    svc = c_getter()

    # Fitting engine with train data
    svc.fit(X_train, y_train)

    # Computing prediction
    y_pred = svc.predict(X_test)

    # How accurate our prediction is
    accuracy = round(metrics.accuracy_score(y_test, y_pred), 2)
    print('    Accuracy:', accuracy)

    # Ability not to label a sample as positive when it is negative
    precision = round(metrics.precision_score(y_test, y_pred, average = 'weighted', zero_division = 0), 2)
    print('    Precision:', precision)

    # Ability to find all positive samples
    recall = round(metrics.recall_score(y_test, y_pred, average = 'weighted', zero_division = 0), 2)
    print('    Recall:', recall)

    return accuracy, precision, recall

def wine_quality_svc():
    """ 
        Classification on wine quality dataset got from http://archive.ics.uci.edu/ml/datasets
    """
    print('Wine quality problem (standard classification):')

    predata = numpy.genfromtxt('wine_quality.csv', delimiter = ';', dtype = float, encoding = 'utf8')

    return testify(predata[1:, :11], predata[1:, 11], float(sys.argv[1]), get_SVC)

def wine_quality_mlp():
    """ 
        Classification on wine quality dataset got from http://archive.ics.uci.edu/ml/datasets
    """
    print('Wine quality problem (neural network):')

    predata = numpy.genfromtxt('wine_quality.csv', delimiter = ';', dtype = float, encoding = 'utf8')

    return testify(predata[1:, :11], predata[1:, 11], float(sys.argv[1]), get_MLP)

def wine_quality_big_mlp():
    """ 
        Classification on wine quality dataset got from http://archive.ics.uci.edu/ml/datasets
    """
    print('Wine quality problem (bigger neural network):')

    predata = numpy.genfromtxt('wine_quality.csv', delimiter = ';', dtype = float, encoding = 'utf8')

    return testify(predata[1:, :11], predata[1:, 11], float(sys.argv[1]), get_BigMLP)

if __name__ == "__main__":
    # Wine quality classification
    a1, p1, r1 = wine_quality_svc()
    print()
    a2, p2, r2 = wine_quality_mlp()
    print()
    a3, p3, r3 = wine_quality_big_mlp()

    # Summary
    print('\nOverall comparision:\n')
    print(tabulate([
        [ 'Accuracy', a1, a2, a3, round((a1 + a2 + a3) / 3, 2) ],
        [ 'Precision', p1, p2, p3, round((p1 + p2 + p3) / 3, 2) ],
        [ 'Recall', r1, r2, r3, round((r1 + r2 + r3) / 3, 2) ]
    ], headers = [ '', 'SVC', 'MLP', 'Bigger MLP', 'Average' ]))
