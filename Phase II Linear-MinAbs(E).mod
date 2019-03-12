param n >=0;
set object := 1 .. 104;
set feature := 1 .. 60;

var a {i in feature};
var b ;
var m {i in object} binary;
var yhat {i in object};
var error_measure {i in object};

param x {i in feature, j in object};
param y {j in object};

minimize error: sum{i in object} error_measure[i];

subject to prediction{i in object}: yhat[i] = (sum{j in feature} a[i]*x[i,j]) + b;

subject to scaling1{i in object}: yhat[i] >= (1-m[i]);
subject to scaling2{i in object}: -yhat[i] >= m[i];

subject to error_msurACTING{i in object}: error_measure[i] >= -y[i] * yhat[i];
subject to error_msurNONACTING{i in object}: error_measure[i] >= 0;
