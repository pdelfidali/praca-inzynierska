import numpy as np
import tensorflow as tf
import tflearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from .helpers import printModelStats, evaluate

N_ITER = 500


def neuralnetwork(X, y):
    tf.compat.v1.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(X[0])])
    net = tflearn.fully_connected(net, 24)
    net = tflearn.fully_connected(net, 24)
    net = tflearn.fully_connected(net, len(y[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)

    model.fit(X, y, n_epoch=1000, batch_size=8, show_metric=True)

    return model


def randomForest(X_train, X_test, y_train, y_test):
    n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num=10)]
    max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
    max_depth.append(None)
    min_samples_split = [2, 4, 6]
    min_samples_leaf = [1, 2]
    bootstrap = [True, False]

    random_grid = {'n_estimators': n_estimators,
                   'max_depth': max_depth,
                   'min_samples_split': min_samples_split,
                   'min_samples_leaf': min_samples_leaf,
                   'bootstrap': bootstrap}

    rf = RandomForestClassifier()

    rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, n_iter=N_ITER, cv=3, verbose=2,
                                   random_state=47, n_jobs=-1)

    rf_random.fit(X_train, y_train)

    base_rf = RandomForestClassifier(n_estimators=10, random_state=123)
    base_rf.fit(X_train, y_train)
    base_accuracy = evaluate(base_rf, X_test, y_test)
    best_accuracy = evaluate(rf_random.best_estimator_, X_test, y_test)

    def _print():
        printModelStats(base_accuracy, best_accuracy, "Random Forest:")

    return rf_random.best_estimator_, _print


def knn(X_train, X_test, y_train, y_test):
    weights = ['uniform', 'distance']
    algorithm = ['ball_tree', 'kd_tree', 'auto']
    n_neighbors = [int(x) for x in np.linspace(1, 8)]
    n_neighbors.extend([int(x) for x in np.linspace(9, 14, num=3)])

    knn_random_grid = {'weights': weights, 'algorithm': algorithm, 'n_neighbors': n_neighbors}

    knn_model = KNeighborsClassifier()

    knn_random = RandomizedSearchCV(estimator=knn_model, param_distributions=knn_random_grid, n_iter=N_ITER, cv=3,
                                    verbose=2, random_state=47, n_jobs=-1)

    knn_random.fit(X_train, y_train)

    base_knn = KNeighborsClassifier()
    base_knn.fit(X_train, y_train)

    base_accuracy = evaluate(base_knn, X_test, y_test)
    best_accuracy = evaluate(knn_random.best_estimator_, X_test, y_test)

    def _print():
        printModelStats(base_accuracy, best_accuracy, "KNN")

    return knn_model, _print


def decisionTree(X_train, X_test, y_train, y_test):
    criterion = ['gini', 'entropy', 'log_loss']
    splitter = ['best', 'random']
    min_samples_split = [int(x) for x in np.linspace(1, 3, 3)]
    min_samples_leaf = [int(x) for x in np.linspace(1, 3, 3)]
    max_features = [int(x) for x in np.linspace(10, 250, 13)]

    tree_random_grid = {'criterion': criterion, 'splitter': splitter, 'min_samples_split': min_samples_split,
                        'min_samples_leaf': min_samples_leaf, 'max_features': max_features}

    tree_model = DecisionTreeClassifier()

    tree_random = RandomizedSearchCV(estimator=tree_model, param_distributions=tree_random_grid, n_iter=N_ITER, cv=3,
                                     verbose=2, random_state=47, n_jobs=-1)

    tree_random.fit(X_train, y_train)

    base_tree = KNeighborsClassifier()
    base_tree.fit(X_train, y_train)

    base_accuracy = evaluate(base_tree, X_test, y_test)
    best_accuracy = evaluate(tree_random.best_estimator_, X_test, y_test)

    def _print():
        printModelStats(base_accuracy, best_accuracy, "Tree")

    return tree_random.best_estimator_, _print
