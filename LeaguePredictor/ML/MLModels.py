import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import neighbors
from sklearn import svm
from sklearn import naive_bayes
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Read dataset in which the individual mastery scores for each player
# have been summed, reducing the total features 23 and format dataframe
# df = pd.read_csv("gamedata_summed_mastery.csv")
# X = df.loc[:, ['blue_champ1',  'blue_ban1',
#                'blue_champ2',  'blue_ban2',
#                'blue_champ3',  'blue_ban3',
#                'blue_champ4', 'blue_ban4',
#                'blue_champ5', 'blue_ban5', 'blue_team_total_mastery',
#                'red_champ1', 'red_ban1',
#                'red_champ2', 'red_ban2',
#                'red_champ3', 'red_ban3',
#                'red_champ4', 'red_ban4',
#                'red_champ5', 'red_ban5', 'red_team_total_mastery']]
# y = df['winner']

# Read dataset in which the individual mastery scores for each player
# are assigned, reducing the total features 32 and format dataframe
df = pd.read_csv("transformed_game_data.csv")
X = df.loc[:, ['blue_champ1', 'blue_mastery1', 'blue_ban1',
               'blue_champ2', 'blue_mastery2', 'blue_ban2',
               'blue_champ3', 'blue_mastery3', 'blue_ban3',
               'blue_champ4', 'blue_mastery4', 'blue_ban4',
               'blue_champ5', 'blue_mastery5', 'blue_ban5',
               'red_champ1', 'red_mastery1', 'red_ban1',
               'red_champ2', 'red_mastery2', 'red_ban2',
               'red_champ3', 'red_mastery3', 'red_ban3',
               'red_champ4', 'red_mastery4', 'red_ban4',
               'red_champ5', 'red_mastery5', 'red_ban5']]
y = df['winner']

# Read alternate game data set, as opposed to pre-match data
# a total of 20 features are utilised
# df = pd.read_csv("high_diamond_ranked_10min.csv")
# X = df.loc[:, ['blueFirstBlood', 'blueKills', 'blueAssists', 'blueDragons', 'blueHeralds',
#                'blueTowersDestroyed', 'blueTotalGold', 'blueAvgLevel', 'blueTotalExperience', 'blueTotalMinionsKilled',
#                'redFirstBlood', 'redKills', 'redAssists', 'redDragons', 'redHeralds',
#                'redTowersDestroyed', 'redTotalGold', 'redAvgLevel',	'redTotalExperience', 'redTotalMinionsKilled']]
# y = df['winner']

# Copy the dataframe for analysis
# df_clean = df.copy()

# create a correlation matrix for the dataset
# plt.figure(figsize=(16, 12))
# sns.heatmap(df_clean.drop('winner', axis=1).corr(), cmap='YlGnBu', annot=True, fmt='.2f', vmin=0)
# plt.show()

# Scale the features
# scaler = MinMaxScaler()
# for (columnName, columnData) in X.iteritems():
#    X[[columnName]] = scaler.fit_transform(X[[columnName]])

# Check the relationship between parameters of red team features
# g = sns.PairGrid(data=df_clean, vars=['redKills', 'redAssists', 'redTotalGold'], hue='winner', height=3, palette='Set1')
# g.map_diag(plt.hist)
# g.map_offdiag(plt.scatter)
# g.add_legend()
# plt.show()

# Check the relationship between parameters of blue team features
# g = sns.PairGrid(data=df_clean, vars=['redKills', 'redAssists', 'redTotalGold'], hue='winner', height=3, palette='Set1')
# g.map_diag(plt.hist)
# g.map_offdiag(plt.scatter)
# g.add_legend()
# plt.show()

# Split Training and Testing sets, 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# generic model load method
def get_score(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    # save trained model
    joblib.dump(model, "model.pkl")
    model_prediction = model.predict(X_test)
    model_accuracy = accuracy_score(y_test, model_prediction)
    actual_values = [y[20], y[21], y[22], y[23], y[24]]
    predicted_values = [model.predict(X)[20], model.predict(X)[21], model.predict(X)[22],
                        model.predict(X)[23], model.predict(X)[24]]
    return print("prediction: ", model_prediction,
                 "\naccuracy: ", model_accuracy,
                 "\nsample actual value: ", actual_values,
                 "\nsample predicted value: ", predicted_values, "\n")


# print and call the model outputs
print("Logistic Regression")
get_score(linear_model.LogisticRegression(max_iter=150), X_train, X_test, y_train, y_test)
print("K-Nearest Neighbors")
get_score(neighbors.KNeighborsClassifier(n_neighbors=30, weights='uniform', algorithm='auto'), X_train, X_test,
          y_train, y_test)
print("Support Vector Machines - SVC")
get_score(svm.SVC(), X_train, X_test, y_train, y_test)
print("Naives Bayes")
get_score(naive_bayes.GaussianNB(), X_train, X_test, y_train, y_test)
print("Random Forest")
get_score(RandomForestClassifier(max_depth=5, n_estimators=40, random_state=0), X_train, X_test, y_train, y_test)
print("Gradient Boosting")
get_score(GradientBoostingClassifier(max_depth=5, n_estimators=200, random_state=0, learning_rate=0.1), X_train,
          X_test, y_train, y_test)

