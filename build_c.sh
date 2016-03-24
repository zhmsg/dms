file_name = $1
cython $1.py
g++ -fPIC $1.c -o $1.so -shared -I/usr/include/python2.7 -I/usr/lib/python2.7/config