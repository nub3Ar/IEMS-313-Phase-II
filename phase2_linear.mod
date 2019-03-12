param n >=0;
set object := 1 .. 104;
set data := 0 .. 60;
set feature within data:= 1 .. 60;


var a {i in feature};
var b ;
var m {i in object} binary;
var yhat {i in object};
var error_measure {i in object};

param x {i in object, j in data};


minimize error: sum{i in object} error_measure[i];

subject to prediction{i in object}: yhat[i] = (sum{j in feature} a[j]*x[i,j]) + b;

subject to scaling1{i in object}: yhat[i] >= 1 - 1000000 * m[i] ;
subject to scaling2{i in object}: yhat[i] <= -1 + 1000000 * (1-m[i]) ;


subject to error_msurACTING{i in object}: error_measure[i] >= 1 - x[i,0] * yhat[i];
subject to error_msurNONACTING{i in object}: error_measure[i] >= 0;


