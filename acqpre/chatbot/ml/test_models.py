from chatbot.ml.helpers import get_data
from chatbot.ml.models import randomForest, neuralNetwork, knn, decisionTree

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = get_data()

    forest, print_forest = randomForest(X_train, X_test, y_train, y_test)
    knnModel, print_knn = knn(X_train, X_test, y_train, y_test)
    nnModel, print_nn = neuralNetwork(X_train, X_test, y_train, y_test)
    tree, print_tree = decisionTree(X_train, X_test, y_train, y_test)

    print_tree()
    print_forest()
    print_knn()
    print_nn()