from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Initialize the model
lr_model = LinearRegression()

class CloPredict:
    def __init__(self):
        self.model = RandomForestRegressor()

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        return mean_squared_error(y_test, y_pred)
    
# Fit the model
lr_model.fit(X_train, y_train)