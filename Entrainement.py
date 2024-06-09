from ast import literal_eval
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv('./donnees_entrainement1.csv')

print(df)

# def convert_set_to_numeric(set_str):
#     if pd.isna(set_str):
#         return 0  # ou une autre valeur par défaut
#     try:
#         s = literal_eval(set_str)
#         return sum(int(bit) for bit in s)  # Exemple: convertir {'0', '1'} en 1+0=1
#     except (ValueError, SyntaxError):
#         return 0  # ou gérer l'erreur de conversion autrement

# # Convertir toutes les colonnes nécessaires
# for col in df.columns:
#     if df[col].dtype == 'object':
#         df[col] = df[col].apply(convert_set_to_numeric)

np.random.seed(42)

# print(df)


X = df.iloc[:,1:-1].values
y = df.iloc[:,-1].values 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.25, random_state= 0)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train,y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:')
print(report)





#################
# Importation model

from joblib import dump

dump(model,'IsCodeModel1.joblib')
