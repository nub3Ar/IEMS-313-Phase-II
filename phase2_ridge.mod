param n >=0;
set object := 1 .. 2;
set feature := 1 .. 60;

var a {i in feature};
var b ;
var m {i in object} binary;
var yhat {i in object};
var error_measure {i in object};
var coe_sum;

param x {i in object, j in feature};
param y {j in object};
param tuning := 0.5;

minimize error: sum{i in object} error_measure[i] + tuning * coe_sum;

subject to ridge: (sum{i in feature} a[i]*a[i]) = coe_sum;
subject to scaling1{i in object}: yhat[i] * yhat[i]>= 1;


subject to error_msurACTING{i in object}: error_measure[i] >= 1 - y[i] * yhat[i];
subject to error_msurNONACTING{i in object}: error_measure[i] >= 0;

