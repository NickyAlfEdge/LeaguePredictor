import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Read dataset and format dataframe
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

# Split Training and Testing sets, 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# estimator and learning rate arrays
estimators = [50, 100, 200]
learning_rates = [0.1, 0.25, 0.5, 0.75, 1]

# loop through each estimator value, then each learning rate and test the models prediction on the dataset
for estimator in estimators:
    print("N Estimators: ", estimator)
    for learning_rate in learning_rates:
        gb_model = GradientBoostingClassifier(n_estimators=estimator, learning_rate=learning_rate, max_depth=5,
                                              random_state=0)
        gb_model.fit(X_train, y_train)
        print("Learning rate: ", learning_rate)
        # print("Accuracy score (training): {0:.3f}".format(accuracy_score(y_train, gb_model.predict(X_train))))
        print("Accuracy score (testing): {0:.3f}".format(accuracy_score(y_test, gb_model.predict(X_test))), "\n")
