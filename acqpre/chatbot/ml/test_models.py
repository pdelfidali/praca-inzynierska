from chatbot.ml.helpers import get_data
from chatbot.ml.models import randomForest, neuralnetwork, knn, decisionTree

#
X_train, X_test, y_train, y_test = get_data()

# X, y = get_data_nn()

# nn = neuralnetwork(X, y)

forest, print_forest = randomForest(X_train, X_test, y_train, y_test)

knnModel, print_knn = knn(X_train, X_test, y_train, y_test)

tree, print_tree = decisionTree(X_train, X_test, y_train, y_test)

print_forest()
print_knn()
print_tree()