import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('clozapine_train.csv')

# Clean missing values
data.dropna(inplace=True)

# Encode categorical variables
encoder = OneHotEncoder()
encoded_features = encoder.fit_transform(data[['gender', 'smoker']])

# Normalize numerical features
scaler = StandardScaler()
normalized_features = scaler.fit_transform(data[['age', 'weight', 'height']])

# Combine encoded and normalized features
X = np.hstack((encoded_features.toarray(), normalized_features))
y = data['concentration']

scaler_clo = StandardScaler()
scaler_nclo = StandardScaler()

def predict_blood_concentration(patient_info):
    # Convert patient info into feature matrix X
    ...
    
    # Predict blood concentration level
    y_pred = model.predict(X)

    return y_pre


def vsearch(y, x):
    return np.where(np.absolute(x - y) == np.min(np.absolute(x - y)))[0][0]

class OrderedFactor():
    def __init__(self, levels):
        self.levels = sorted(levels)
    
    def transform(self, X):
        return np.vectorize(lambda x: self.levels.index(x))(X[:,0]).astype('float')

def ctp(patient_data, scaler_clo, scaler_nclo):

    data_nclo = patient_data.copy()
    data_nclo[1] = int(data_nclo[1])
    data_nclo[2:6] = scaler_clo.transform(data_nclo[2:6].reshape(-1, 1)).flatten()
    data_nclo[np.isnan(data_nclo)] = 0

    df_nclo = pd.DataFrame({"male":[data_nclo[1]]})
    df_features = pd.DataFrame(data_nclo[2:6].reshape(-1, 1), columns=["age", "dose", "bmi", "crp"])
    df_covariates = pd.DataFrame(data_nclo[6:].reshape(-1, 1), columns=["inducers_3a4", "inhibitors_3a4", "substrates_3a4", "inducers_1a2", "inhibitors_1a2", "substrates_1a2"])
    data_nclo = np.concatenate((df_nclo.tonumpy(), df_features.tonumpy(), df_covariates.tonumpy()), axis=-1).astype('float32')
    data_nclo = mlj.coerce(data_nclo, {"male":OrderedFactor, "age":Continuous, "dose":Continuous, "bmi":Continuous, "crp":Continuous, "inducers_3a4":Continuous, "inhibitors_3a4":Continuous, "substrates_3a4":Continuous, "inducers_1a2":Continuous, "inhibitors_1a2":Continuous, "substrates_1a2":Continuous}).values

    nclo_level_pred = mlj.predict(nclo_model_regressor, data_nclo)

    clo_level_pred = mlj.predict(clo_model_regressor, data_clo)

    clo_level = np.round(clo_level_pred[0], decimals=1)
    clo_level[clo_level < 0] = 0
    nclo_level = np.round(nclo_level_pred[0], decimals=1)[0]
    nclo_level[nclo_level < 0] = 0

    if clo_level > 550:
        clo_group = 1
    else:
        clo_group = 0

    if clo_level > 550 or nclo_level > 270:
        clo_group_adj = 1
    else:
        clo_group_adj = 0

    return clo_group, clo_group_adj, clo_level, nclo_level
