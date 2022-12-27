import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

from .helpers import get_labels

N_ITER = 400


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

    rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, n_iter=N_ITER, cv=3,
                                   random_state=47, n_jobs=-1, scoring='accuracy')

    rf_random.fit(X_train, y_train)

    base_rf = RandomForestClassifier(n_estimators=10, random_state=123)
    base_rf.fit(X_train, y_train)
    base_accuracy = base_rf.score(X_test, y_test)
    best_accuracy = rf_random.score(X_test, y_test)
    y_pred = rf_random.best_estimator_.predict(X_test)

    def _print():
        x = accuracy_score(y_test, y_pred)
        print("=====================RANDOM FOREST==========================")
        print(f"Accuracy : {x} vs base accuracy: {base_accuracy}")
        print(classification_report(y_test, y_pred, target_names=get_labels()))
        print("============================================================")

    return rf_random.best_estimator_, _print

    # best_paramas = {'algorithm': 'auto', 'leaf_size': 30, 'metric': 'minkowski', 'metric_params': None, 'n_jobs': None,
    #                 'n_neighbors': 5, 'p': 2, 'weights': 'uniform'}


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

    base_accuracy = base_knn.score(X_test, y_test)
    y_pred = knn_random.best_estimator_.predict(X_test)

    def _print():
        best_accuracy = accuracy_score(y_test, y_pred)
        print("=====================KNN====================================")
        print(f"Accuracy : {best_accuracy} vs base accuracy: {base_accuracy}")
        print(classification_report(y_test, y_pred, target_names=get_labels()))
        print("============================================================")

    return knn_model, _print


def decisionTree(X_train, X_test, y_train, y_test):
    splitter = ['best', 'random']
    min_samples_split = [int(x) for x in np.linspace(1, 3, 3)]
    min_samples_leaf = [int(x) for x in np.linspace(1, 3, 3)]
    max_features = [int(x) for x in np.linspace(10, 250, 13)]

    tree_random_grid = {'splitter': splitter, 'min_samples_split': min_samples_split,
                        'min_samples_leaf': min_samples_leaf, 'max_features': max_features}

    tree_model = DecisionTreeClassifier()

    tree_random = RandomizedSearchCV(estimator=tree_model, param_distributions=tree_random_grid, n_iter=N_ITER, cv=3,
                                     random_state=47, n_jobs=-1, scoring='accuracy')

    tree_random.fit(X_train, y_train)

    base_tree = DecisionTreeClassifier()
    base_tree.fit(X_train, y_train)

    base_accuracy = base_tree.score(X_test, y_test)
    best_accuracy = tree_random.best_estimator_.score(X_test, y_test)
    y_pred = tree_random.best_estimator_.predict(X_test)

    def _print():
        x = accuracy_score(y_test, y_pred)
        print("=====================DECISION TREE==========================")
        print(f"Accuracy : {x} vs base accuracy: {base_accuracy}")
        print(classification_report(y_test, y_pred, target_names=get_labels()))
        print("============================================================")

    return tree_random.best_estimator_, _print


def neuralNetwork(X_train, X_test, y_train, y_test):
    hidden_layer_sizes = [(8, 8, 8), (256, 256, 256), (256, 64, 32)]
    learning_rate = ['adaptive', 'constant']
    # nn_random_grid = {"hidden_layer_sizes": hidden_layer_sizes, "learning_rate": learning_rate}
    nn_random_grid = {'solver': ['lbfgs'],
                      'max_iter': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000],
                      'alpha': 10.0 ** -np.arange(1, 10), 'hidden_layer_sizes': np.arange(10, 15)}
    neural_network = MLPClassifier()

    nn_random = RandomizedSearchCV(estimator=neural_network, param_distributions=nn_random_grid,
                                   random_state=47, n_jobs=-1)

    nn_random.fit(X_train, y_train)

    base_nn = MLPClassifier()
    base_nn.fit(X_train, y_train)

    base_accuracy = base_nn.score(X_test, y_test)
    best_accuracy = nn_random.best_estimator_.score(X_test, y_test)
    y_pred = nn_random.best_estimator_.predict(X_test)

    def _print():
        x = accuracy_score(y_test, y_pred)
        print("=====================NEURAL NETWORK=========================")
        print(f"Accuracy : {x} vs base accuracy: {base_accuracy}")
        print(classification_report(y_test, y_pred, target_names=get_labels()))
        print("============================================================")

    return nn_random.best_estimator_, _print


def best_model(X, y):
    model = KNeighborsClassifier()
    model.fit(X, y)
    return model
