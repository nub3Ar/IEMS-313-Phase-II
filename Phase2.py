from amplpy import AMPL, Environment, DataFrame
import pandas as pd
import math

#####before you run, pip install pandas, pip install amplpy


############    SETUP   ############
validating_data = pd.read_csv(open('Validation_Dataset.csv'))
#dimensions of the data
dv1,dv2 = validating_data.shape
print(dv1, dv2)
#column names
col_names_va = validating_data.columns.values
#x/y variable separation
y_va = validating_data.loc[0::,'Label'].values.tolist()
x_va = validating_data.loc[0::,'Item'::]

############AMPL#################

ampl = AMPL(Environment('/home/nub3ar/AMPL'))

ampl.read('phase2_linear.mod')
ampl.readData('phase2.dat')

ampl.solve()
a = ampl.getVariable('a').getValues().toList()
b = ampl.getVariable('b').value()

predictions = []

for i in range (0, dv1):
    x = x_va.iloc[[i]].values.tolist()
    print(x)
    x = x[0][2:]
    y = b
    for i in range(0, dv2-2):
        y += a[i][1]*x[i]
    if y >= 0:
        predictions.append(1)
    elif y< 0:
        predictions.append(-1)
    else:
        print("error has occured")

correctyes = 0
correctno = 0
incorrectyes = 0
incorrectno = 0

print(len(predictions))
print(len(y_va))
for i in range (0, dv1):
    print(y_va[i], predictions[i])
    if y_va[i] == 1:
        if predictions[i] == 1:
            correctyes += 1
        else:
            incorrectno += 1
    else:
        if predictions[i] == -1:
            correctno += 1
        else:
            incorrectyes += 1

print(correctyes, correctno, incorrectyes, incorrectno)
print("Accuracy:", (correctyes+correctno)/(correctyes+correctno+incorrectno+incorrectyes))






#legacy code used for getting data from excel
'''
ampl.getSet('feature').setValues(range(0,60))
ampl.getSet('object').setValues(range(0,104))

x_dat = []
for i in range(0,60):
    x_dat.append(x_tr[x_tr.columns[i]].values.tolist())
y_dat = []
for i in range(0,104):
    y_dat.append(y_tr[i])
x_df = DataFrame(('feature', 'object'), 'x')
x_df.setValues({
    (feature, object): x_dat[i][j]
    for i, feature in enumerate(range(0,60))
    for j, object in enumerate(range(0,104))
})
y_df = DataFrame(('object'), 'y')
y_df.setValues({
        object: y_dat[i]
        for i, object in enumerate(range(0,104))
})

ampl.setData(x_df)
ampl.setData(y_df)
'''
