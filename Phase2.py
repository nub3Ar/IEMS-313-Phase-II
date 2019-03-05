from amplpy import AMPL, Environment, DataFrame
import pandas as pd
import math

#####before you run, pip install pandas, pip install amplpy


############    SETUP   ############
training_data= pd.read_csv(open('Training_Dataset.csv'))
validating_data = pd.read_csv(open('Validation_Dataset.csv'))
#dimensions of the data
dt1,dt2 = training_data.shape
dv1,dv2 = validating_data.shape
#column names
col_names_tr = training_data.columns.values
col_names_va = validating_data.columns.values
#x/y variable separation
y_tr = training_data.loc[0::,'Label']
x_tr = training_data.loc[0::,'1'::]
y_va = validating_data.loc[0::,'Label']
x_va = validating_data.loc[0::,'Item'::]



############AMPL#################
ampl = AMPL(Environment('/home/nub3ar/AMPL'))

ampl.read('Phase II.mod')
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

print(y_df)
ampl.setData(x_df)
ampl.setData(y_df)



ampl.solve()
b = ampl.getVariable('b').value()
print(b)
