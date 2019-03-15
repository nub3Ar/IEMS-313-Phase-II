from amplpy import AMPL, Environment, DataFrame
import pandas as pd
import math

#####before you run, pip install pandas, pip install amplpy, stick with python3

############    SETUP   ############
training_dat = "phase2_training.dat"#input("What's the directory of your training .dat file?")
validating_dir = "Validation_Dataset.csv" #input("What's the directory of your validating set?")
model_dir = "phase2_lasso.mod" #input("What's the directory of your model?")
ampl_dir =  "/home/nub3ar/AMPL" #input("Where is ampl installed on your computer?") #"E:\ampl_mswin64"
validating_data = pd.read_csv(open(validating_dir))
#dimensions of the data
dv1,dv2 = validating_data.shape
print(dv1, dv2)
#column names
col_names_va = validating_data.columns.values
#x/y variable separation
y_va = validating_data.loc[0::,'Label'].values.tolist()
x_va = validating_data.loc[0::,'Item'::]

############AMPL#################
ampl = AMPL(Environment(ampl_dir))

index_list = []
Accuracy_list = []
for index in (range 1:1000)
    ampl.reset()
    tuning = ampl.getParameter("tuning")
    tuning.SetValues(0.00001*index)
    ampl.read(model_dir)
    ampl.readData(training_dat)
    ampl.solve()
    a = ampl.getVariable('a').getValues().toList()
    b = ampl.getVariable('b').value()

    #parsing the coefficients
    a_list = []
    for i in range(0, dv2-2):
        a_list.append(a[i][1])

    #getting the predicted values
    y_value = []
    for i in range (0, dv1):
        x = x_va.iloc[[i]].values.tolist()
        x = x[0][2:]
        y = b
        for j in range(0, dv2-2):
            y += a[j][1]*x[j]
        y_value.append(y)

    #print("training a:", a_list)
    #print("training b:", b)

    diff_list = []
    diff_lasso = []
    correctyes = 0
    correctno = 0
    incorrectyes = 0
    incorrectno = 0

    for i in range (0, dv1):
        diff_list.append(max(0, 1-y_value[i]*y_va[i]))
        diff_lasso.append(max(0, 1-y_value[i]*y_va[i]+0.0013*sum(map(abs, a_list))))
        if y_va[i] == 1:
            if y_value[i] > 0:
                correctyes += 1
            else:
                incorrectno += 1
        else:
            if y_value[i] <= 0:
                correctno += 1
            else:
                incorrectyes += 1

    max_diff_err = max(diff_list)
    total_diff_err = sum(diff_list)
    lasso_err = sum(diff_lasso)
    ridge_err = total_diff_err+0.0082*sum(number*number for number in a_list)               ###need to change the tuning parameter 
    print(sum(map(abs, a_list)))
    Accuracy = (correctyes+correctno)/(correctyes+correctno+incorrectno+incorrectyes)
    #print("All error measures are calculated, please disregard the ones irrelevant with the method used")
    #print("False Positive:", incorrectyes/104)
    #print("False Negative:", incorrectno/104)
    #print("Accuracy:", Accuracy)
    #print("Misclassification Rate:", 1-Accuracy)
    #print("Number of Misclassified items:", (incorrectno+incorrectyes))
    #print("total error:", total_diff_err)
    #print("max error", max_diff_err)
    #print("Lasso Error", lasso_err)
    #print("Ridge Error", ridge_err)
    Accuracy_list.append(Accuracy)
    index_list.append(index)

    print("#######################################")
    print(index, Accuracy)
    print("#######################################")    


print(max(Accuracy_list))


#legacy code used for getting data from excel
'''
ampl.reset()
ampl.read(model_dir)
ampl.readData(testing_dat)
ampl.solve()
a1 = ampl.getVariable('a').getValues().toList()
b1 = ampl.getVariable('b').value()
print("testing a:", a1)
print("testing b:", b1)
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
