cdef extern from "arrayobject.h":
    ctypedef int intp
    
    ctypedef extern class numpy.ndarray [object PyArrayObject]:
        cdef char* data
        cdef int nd
        cdef intp* dimensions
        cdef intp* strides
        cdef int flags

        
cdef extern from "vector":
    ctypedef struct doubleVec "std::vector<double>":
        void (* push_back)(double elem)
        void (* assign)(double* begin, double* end)
        int (* size)()
    doubleVec doubleVecFactory "std::vector<double>"(double* begin, double* end)
    cdef extern double read_vec(doubleVec)
    
cdef extern from "Minuit2/FCNBase.h":
    ctypedef struct FCNBase "ROOT::Minuit2::FCNBase":
        double Up()
        double call "operator()"(doubleVec*)
        
cdef extern from "Minuit2/MnUserParameters.h":
    ctypedef struct MnUserParameters "ROOT::Minuit2::MnUserParameters":
        void (* Fix)(unsigned int)
        
cdef class UserFunction(FCNBase):
    cdef double Up(self):
        return 1.0
        
    cdef double call(self, doubleVec* x):
        return 1.0
        
