int *i_simple;
char *c_simple;
float *f_simple;

int i_test = 42;
float f_test = 42.42;
char c_test = 'a';

int *i_assign = &i_test;
float *f_assign = &f_test;
char  *c_assign = &c_test;


int *a, *b, *c, *d = &i_test;
float *e, *f, *g = &f_test;
char *h, *i, *j, *k = &c_test;

int **z =  &a;