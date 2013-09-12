//Copyright (c) 2012-2013 Christian Schwarz
//
//Permission is hereby granted, free of charge, to any person obtaining
//a copy of this software and associated documentation files (the
//"Software"), to deal in the Software without restriction, including
//without limitation the rights to use, copy, modify, merge, publish,
//distribute, sublicense, and/or sell copies of the Software, and to
//permit persons to whom the Software is furnished to do so, subject to
//the following conditions:
//
//The above copyright notice and this permission notice shall be
//included in all copies or substantial portions of the Software.
//
//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
//EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
//MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
//NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
//LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
//OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
//WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#include "baseerrormeasure.h"

namespace errors {
    namespace baseerrormeasure {
        namespace BaseErrorMeasure {

            PyObject* initialize(PyObject* self, PyObject *originalTimeSeries, PyObject *calculatedTimesSeries)
            {
                if (0 < PySequence_Size(PyObject_GetAttrString(self, "_errorValues"))) {
                    PyErr_SetString(PyExc_StandardError, "An ErrorMeasure can only be initialized once.");
                    return NULL;
                }

                PyObject_CallMethodObjArgs(originalTimeSeries,    PyString_FromString("sort_timeseries"), NULL);
                PyObject_CallMethodObjArgs(calculatedTimesSeries, PyString_FromString("sort_timeseries"), NULL);

                int index = 0;
                PyObject* orgPair;
                PyObject* calcPair;
                PyObject* local_error;

                PyObject* _errorValues = PyList_New(PyObject_Length(originalTimeSeries));
                PyObject* _errorDates = PyList_New(PyObject_Length(originalTimeSeries));
                PyObject* iterator1 = PyObject_GetIter(originalTimeSeries);

                while ((orgPair = PyIter_Next(iterator1))) {   
                    
                    PyObject* iterator2 = PyObject_GetIter(calculatedTimesSeries);
                    
                    while ((calcPair = PyIter_Next(iterator2))) {
                        if (PyFloat_AsDouble(PySequence_GetItem(orgPair, 0)) != PyFloat_AsDouble(PySequence_GetItem(calcPair, 0)))
                            continue;
                        
                        local_error = PyObject_CallMethodObjArgs(self, PyString_FromString("local_error"), 
                                                                       PyList_GetSlice(orgPair, 1, PyList_Size(orgPair)),
                                                                       PyList_GetSlice(calcPair, 1, PyList_Size(calcPair)),
                                                                       NULL
                                                                );
                        
                        //NotImplemented Exception
                        if(!local_error) {
                            PyErr_SetString(PyExc_NotImplementedError, "");
                            return NULL;
                        }

                        PyList_SetItem(_errorValues, index, local_error);
                        PyList_SetItem(_errorDates, index, PySequence_GetItem(orgPair, 0));
                        ++index;

                        Py_DECREF(calcPair);
                    }

                    Py_DECREF(iterator2);
                    Py_DECREF(orgPair);
                }

                Py_DECREF(iterator1);

                //Cut off trailing zeroes
                _errorValues = PyList_GetSlice(_errorValues, 0, index);
                _errorDates = PyList_GetSlice(_errorDates, 0, index);
                                
                //return False, if the error cannot be calculated
                double _minimalErrorCalculationPercentage = PyFloat_AsDouble(PyObject_GetAttrString(self, "_minimalErrorCalculationPercentage"));
                
                if(PyList_Size(_errorValues) < (_minimalErrorCalculationPercentage * PyObject_Length(originalTimeSeries)))
                    Py_RETURN_FALSE;

                PyObject_SetAttrString(self, "_errorValues", _errorValues);
                PyObject_SetAttrString(self, "_errorDates", _errorDates);
                Py_RETURN_TRUE;
            }

        }
    }
}
