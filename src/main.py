import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import tensorflow as tf

# Define function to create a simple feedforward network
class FeedForward(nn.Module):
    features: int
    
    def setup(self):
        self.dense1 = nn.Dense(self.features)
        self.dense2 = nn.Dense(1)
        
    def __call__(self, x):
        x = nn.Dense(32)(x)
        x = nn.relu(x)
        x = self.dense1(x)
        return self.dense2(x)
    
# Load the data
data = pd.read_csv('clozapine_test.csv')

# Preprocess the data
# ...

# Split the data into features (X) and target variable (y)
X = data[['feature1', 'feature2', 'feature3']].values
y = data[['blood_concentration']].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest regressor
rf_regressor = RandomForestRegressor(n_estimators=100, n_jobs=-1, random_state=42)
rf_regressor.fit(X_train, y_train)

# Evaluate the model on the testing set
y_pred = rf_regressor.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print("Random Forest MAE:", mae)

# Save the trained model as a TensorFlow frozen graph
tf.saved_model.save(tf.keras.models.clone_model(rf_regressor), "bump")


# Load training data
test_data = pd.read_csv('data/clozapine_test.csv')

# Create model instances
nclo_model_regressor = FeedForward(features=50)
clo_model_regressor = FeedForward(features=50)

# Load saved scalers from disk
scaler_clo = joblib.load('models/scaler_clo.jld')
scaler_nclo = joblib.load('models/scaler_nclo.jld')

# Preprocess input data
X_test_scaled_clo = scaler_clo.transform(test_data[['age', 'weight', 'sex']])
X_test_scaled_nclo = scaler_nclo.transform(test_data[['age', 'weight', 'sex']])

# Predict output values
y_pred_clo = clo_model_regressor(X_test_scaled_clo).numpy()
y_pred_nclo = nclo_model_regressor(X_test_scaled_nclo).numpy()

# Invert scaling of predicted outputs
y_pred_clo = scaler_clo.inverse_transform(y_pred_clo)
y_pred_nclo = scaler_nclo.inverse_transform(y_pred_nclo)

# Add predictions to test dataset
test_data['PredictClo'] = y_pred_clo[:, 0]
test_data['PredictNcLo'] = y_pred_nclo[:, 0]

# Save predictions to csv file
test_data.to_csv('output/clozapine_test_predictions.csv', index=False)




