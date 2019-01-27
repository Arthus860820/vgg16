import pandas as pd

from sklearn.model_selection import  train_test_split
from sklearn.ensemble.gradient_boosting import GradientBoostingRegressor
from sklearn import metrics

def valiation(y_true, y_pred):
    print("MSE: ",metrics.mean_squared_error(y_true, y_pred))
    print("MAE: ",metrics.mean_absolute_error(y_true, y_pred))


def preprocess(data):
    data['killsCategories'] = pd.cut(data['kills'], [-1, 0, 2, 5, 10, 60],
                                      labels=['0_kills', '1-2_kills', '3-5_kills', '6-10_kills', '10+_kills'])

    data['healsAndBoosts'] = data['heals'] + data['boosts']
    
    data['totalDistance'] = data['walkDistance'] + data['rideDistance'] + data['swimDistance']

    data['swimDistance'] = pd.cut(data['swimDistance'], [-1, 0, 5, 20, 5286], labels=['0m', '1-5m', '6-20m', '20m+'])

    data['playersJoined'] = data.groupby('matchId')['matchId'].transform('count')

    
    data['killsNorm'] = data['kills'] * ((100 - data['playersJoined']) / 100 + 1)
    data['damageDealtNorm'] = data['damageDealt'] * ((100 - data['playersJoined']) / 100 + 1)

    data['boostsPerWalkDistance'] = data['boosts'] / (data[
                                                            'walkDistance'] + 1)  # The +1 is to avoid infinity, because there are entries where boosts>0 and walkDistance=0. Strange.
    data['boostsPerWalkDistance'].fillna(0, inplace=True)
    
    data['healsPerWalkDistance'] = data['heals'] / (data['walkDistance'] + 1)  # The +1 is to avoid infinity, because there are entries where heals>0 and walkDistance=0. Strange.
   
    data['healsPerWalkDistance'].fillna(0, inplace=True)
   
    data['healsAndBoostsPerWalkDistance'] = data['healsAndBoosts'] / (data['walkDistance'] + 1)  # The +1 is to avoid infinity.
    
    data['healsAndBoostsPerWalkDistance'].fillna(0, inplace=True)


    data['killsPerWalkDistance'] = data['kills'] / \
                                    (data['walkDistance'] + 1)  # The +1 is to avoid infinity, because there are entries where kills>0 and walkDistance=0. Strange.
    data['killsPerWalkDistance'].fillna(0, inplace=True)

    data['team'] = [1 if i > 50 else 2 if (i > 25 & i <= 50) else 4 for i in data['numGroups']]

    data['killsCategories'] = data['killsCategories'].astype('category').cat.codes

    data = data[['winPlacePerc','totalDistance', 'killsCategories', 'playersJoined', 'killsNorm',
                   'damageDealtNorm', 'boostsPerWalkDistance', 'healsPerWalkDistance',
                   'healsAndBoostsPerWalkDistance', 'killsPerWalkDistance']]

    return data

train = pd.read_csv("train_V2.csv")

train = train.sample(frac=0.3)

train = preprocess(train)

X = train[['totalDistance', 'killsCategories', 'playersJoined', 'killsNorm',
            'damageDealtNorm', 'boostsPerWalkDistance', 'healsPerWalkDistance',
            'healsAndBoostsPerWalkDistance', 'killsPerWalkDistance']]
y = train["winPlacePerc"]

X_train, X_test, y_train,y_test= train_test_split(X, y)

regressor = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1,max_depth=1, loss='ls')
regressor.fit(X_train, y_train)
test_y_predicted = regressor.predict(X_test)
valiation(y_test, test_y_predicted)
