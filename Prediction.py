from joblib import load
import pandas as pd

myModel = load('IsCodeModel.joblib')

# nouveau_langage = ['0100', '1101', '0010', '1111']
# nouveau_langage = ['100000','0010001','1111110','010','000010','00','1001','0']
nouveau_langage = ['0']

import DataCreation as dc

data = dc.Traiter_langage(nouveau_langage)
print(data)
data = pd.DataFrame(data)
print(data)
result = myModel.predict(data)
print(result)

percent = myModel.predict_proba(data)
print(percent*100)