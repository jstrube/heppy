cdef extern from "numpy/arrayobject.h":

# Types
    ctypedef int npy_intp
# Classes
    ctypedef extern class numpy.dtype [object PyArray_Descr]:
        cdef int type_num, elsize, alignment
        cdef char type, kind, byteorder, hasobject
        cdef object fields, typeobj

    ctypedef extern class numpy.ndarray [object PyArrayObject]:
        cdef char *data
        cdef int nd
        cdef npy_intp *dimensions
        cdef npy_intp *strides
        cdef object base
        cdef dtype descr
        cdef int flags

# The NumPy initialization funtion
    void import_array() 

