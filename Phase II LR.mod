param n >=0;
set object;
set feature;

var a {i in feature};
var b ;
var m {i in object} binary;
var yhat {i in object};
var error_measure {i in object};

param x {i in feature, j in object};
param y {j in object};

minimize error: sum{i in object} (yhat[i]-y[i])^2;

subject to prediction{i in object}: yhat[i] = (sum{j in feature} a[j]*x[j,i]) + b;

subject to scaling1{i in object}: yhat[i] >= (1-m[i]);
subject to scaling2{i in object}: -yhat[i] >= m[i];
