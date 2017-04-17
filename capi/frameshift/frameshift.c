/*  Example of wrapping the cos function from math.h using the Numpy-C-API. */

#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>

/*  wrapped cosine function */
static PyObject* frameshift(PyObject* self, PyObject* args)
{

    PyArrayObject *in_array;
    npy_intp s;
    PyObject      *out_array;
    NpyIter *in_iter;
    NpyIter *out_iter;
    NpyIter_IterNextFunc *in_iternext;
    NpyIter_IterNextFunc *out_iternext;
    npy_intp ds;
    npy_intp *idptr;
    npy_intp *odptr;

    /*  parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "iO!", &s, &PyArray_Type, &in_array))
        return NULL;

    /*  construct the output array, like the input array */
    out_array = PyArray_NewLikeArray(in_array, NPY_ANYORDER, NULL, 0);
    if (out_array == NULL)
        return NULL;

    /*  create the iterators */
    //in_iter = NpyIter_New(in_array, NPY_ITER_READONLY, NPY_KEEPORDER,
    //                         NPY_NO_CASTING, NULL);
    //if (in_iter == NULL)
    //    goto fail;

    //out_iter = NpyIter_New((PyArrayObject *)out_array, NPY_ITER_READWRITE,
    //                      NPY_KEEPORDER, NPY_NO_CASTING, NULL);
    //if (out_iter == NULL) {
    //    NpyIter_Deallocate(in_iter);
    //    goto fail;
    //}

    //in_iternext = NpyIter_GetIterNext(in_iter, NULL);
    //out_iternext = NpyIter_GetIterNext(out_iter, NULL);
    //if (in_iternext == NULL || out_iternext == NULL) {
    //    NpyIter_Deallocate(in_iter);
    //    NpyIter_Deallocate(out_iter);
    //    goto fail;
    //}
    //int ** in_dataptr = (int **) NpyIter_GetDataPtrArray(in_iter);
    //int ** out_dataptr = (int **) NpyIter_GetDataPtrArray(out_iter);

    /*  iterate over the arrays */
    //do {
    //    **out_dataptr = **in_dataptr + s;
    //} while(in_iternext(in_iter) && out_iternext(out_iter));
    ds = PyArray_DIM(in_array, 0);
    idptr = PyArray_DATA(in_array)
    odptr = PyArray_DATA(out_array)
    while(ds--) {
            }

    /*  clean up and return the result */
    NpyIter_Deallocate(in_iter);
    NpyIter_Deallocate(out_iter);
    Py_INCREF(out_array);
    return out_array;

    /*  in case bad things happen */
    fail:
        Py_XDECREF(out_array);
        return NULL;
}

/*  define functions in module */
static PyMethodDef FrameMethods[] =
{
     {"frameshift", frameshift, METH_VARARGS,
         "shift frame by vector"},
     {NULL, NULL, 0, NULL}
};

/* module initialization */
PyMODINIT_FUNC
initframeshift(void)
{
     (void) Py_InitModule("frameshift", FrameMethods);
     /* IMPORTANT: this must be called */
     import_array();
}