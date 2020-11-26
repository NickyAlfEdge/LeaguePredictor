import pandas as pd
from numpy import mean
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

# Read dataset in which the individual mastery scores for each player
# are assigned, reducing the total features 32 and format dataframe
# df = pd.read_csv("gamedata_individual_player_mastery.csv")
# X = df.loc[:, ['blue_champ1', 'blue_mastery1', 'blue_ban1',
#                'blue_champ2', 'blue_mastery2', 'blue_ban2',
#                'blue_champ3', 'blue_mastery3', 'blue_ban3',
#                'blue_champ4', 'blue_mastery4', 'blue_ban4',
#                'blue_champ5', 'blue_mastery5', 'blue_ban5',
#                'red_champ1', 'red_mastery1', 'red_ban1',
#                'red_champ2', 'red_mastery2', 'red_ban2',
#                'red_champ3', 'red_mastery3', 'red_ban3',
#                'red_champ4', 'red_mastery4', 'red_ban4',
#                'red_champ5', 'red_mastery5', 'red_ban5']]
# y = df['winner']

# Read alternate game data set, as opposed to pre-match data
# a total of 20 features are utilised
df = pd.read_csv("scaled_diamond_ranked_games.csv")
X = df.loc[:, ['blueFirstBlood', 'blueKills', 'blueAssists', 'blueDragons', 'blueHeralds',
               'blueTowersDestroyed', 'blueTotalGold', 'blueAvgLevel', 'blueTotalExperience', 'blueTotalMinionsKilled',
               'redFirstBlood', 'redKills', 'redAssists', 'redDragons', 'redHeralds',
               'redTowersDestroyed', 'redTotalGold', 'redAvgLevel',	'redTotalExperience', 'redTotalMinionsKilled']]
y = df['winner']

# accuracy score arrays for tested models
scores_knn = []
scores_lr = []
scores_svm = []
scores_nb = []
scores_rf = []
scores_gb = []

# load KFold method with 10 splits
kf = StratifiedKFold(n_splits=10)


# generic model load method
def get_score(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    model_prediction = model.predict(X_test)
    model_accuracy = accuracy_score(y_test, model_prediction)
    return model_accuracy


# loop through the dataframe and test/train with KFold split data
for train_index, test_index in kf.split(X, y):
    X_train, X_test, y_train, y_test = X.loc[train_index], X.loc[test_index], y[train_index], y[test_index]
    scores_knn.append(get_score(KNeighborsClassifier(n_neighbors=30, weights='uniform', algorithm='auto'), X_train, X_test, y_train, y_test))
    scores_lr.append(get_score(linear_model.LogisticRegression(max_iter=150), X_train, X_test, y_train, y_test))
    scores_svm.append(get_score(SVC(), X_train, X_test, y_train, y_test))
    scores_nb.append(get_score(GaussianNB(), X_train, X_test, y_train, y_test))
    scores_rf.append(get_score(RandomForestClassifier(max_depth=5, n_estimators=40, random_state=0), X_train, X_test, y_train, y_test))
    scores_gb.append(get_score(GradientBoostingClassifier(max_depth=5, n_estimators=50, random_state=0, learning_rate=0.1), X_train, X_test, y_train, y_test))

# print resulting data
print("KNN", "\nKFold Accuracy: ", scores_knn, "\nAverage:", mean(scores_knn), "\n")
print("Logistic Regression", "\nKFold Accuracy: ", scores_lr, "\nAverage:", mean(scores_lr), "\n")
print("SVM", "\nKFold Accuracy: ", scores_svm, "\nAverage:", mean(scores_svm), "\n")
print("Naives Bayes", "\nKFold Accuracy: ", scores_nb, "\nAverage:", mean(scores_nb), "\n")
print("Random Forest", "\nKFold Accuracy: ", scores_rf, "\nAverage:", mean(scores_rf), "\n")
print("Gradient Boosting", "\nKFold Accuracy: ", scores_gb, "\nAverage:", mean(scores_gb), "\n")