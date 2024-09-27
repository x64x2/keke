import pandas as pd
from model.pharmacokinetics import OneCompartmentModel
from model.models import BenzodiazepinePredictor

# Load data
data = pd.read_csv('data/clozapine_train.csv')

# Preprocess data
X = data.drop(['inhibitors'], axis=1)
y = data['inhibitors']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = CloPredict()
model.train(X_train, y_train)

# Evaluate the model
mse = model.evaluate(X_test, y_test)
print(f'MSE: {mse:.2f}')

# Save the trained model
import pickle
with open('clozapine_regressor_model.jlso', 'wb') as f:
    pickle.dump(model, f)