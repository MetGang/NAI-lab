# Patryk Kośmider s16863
# Krzysztof Marek s16663
# 
# 1st dataset -> http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# The Wine Quality Dataset involves predicting the quality of white wines on a scale given chemical measures of each wine.
# 
# 2nd dataset -> https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html
# The Breast Cancer Dataset involves predicting the probability of positive case of breast cancer with given attributes.
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

from sklearn import metrics

from sklearn.model_selection import train_test_split

from sklearn.datasets import load_breast_cancer

from sklearn.svm import SVC

def get_SVC():
    """ 
        Helper returning classification engine.
        
        Returns: 
            SVC: C-Support Vector classification engine
    """
    return SVC(kernel = 'linear')

def testify(inputs, targets, test_size):
    """ 
        Performs training and testing on datasets with given size of test sample.

        Parameters:
            inputs (array): Array containg inputs for train function.
            targets (array): Array containg targets for train function.
            test_size (float): Represents the proportion of the dataset to include in the train split in range (0.0, 1.0).
    """
    print(f'  Training and predicting for {test_size * 100}% ({round(test_size * len(inputs))}) test samples')
    X_train, X_test, y_train, y_test = train_test_split(inputs, targets, test_size = test_size)

    svc = get_SVC()

    # Fitting engine with train data
    svc.fit(X_train, y_train)

    # Computing prediction
    y_pred = svc.predict(X_test)

    # How accurate our prediction is
    print('    Accuracy:', round(metrics.accuracy_score(y_test, y_pred), 2))

    # Ability not to label a sample as positive when it is negative
    print('    Precision:', round(metrics.precision_score(y_test, y_pred, average = 'weighted', zero_division = 0), 2))

    # Ability yto find all positive samples
    print('    Recall:', round(metrics.recall_score(y_test, y_pred, average = 'weighted', zero_division = 0), 2))

def breast_cancer():
    """ 
        Classification on breast cancer dataset imported from sklearn datasets
    """
    print('Breast cancer problem:')

    predata = load_breast_cancer()

    testify(predata['data'], predata['target'], float(sys.argv[1]))

def wine_quality():
    """ 
        Classification on wine quality dataset got from http://archive.ics.uci.edu/ml/datasets
    """
    print('Wine quality problem:')

    predata = numpy.genfromtxt('wine_quality.csv', delimiter = ';', dtype = float, encoding = 'utf8')

    testify(predata[1:, :11], predata[1:, 11], float(sys.argv[1]))

if __name__ == "__main__":
    # Breast cancer classification
    breast_cancer()

    # Wine quality classification
    wine_quality()
