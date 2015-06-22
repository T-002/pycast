//Copyright (c) 2012-2015 Christian Schwarz
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

#include "timeseries.h"
#include "OpenCLProvider.h"

namespace common {
	namespace timeseries {
		namespace TimeSeries {
			
			PyObject*
			_check_normalization(PyObject* self) {

				/******** BEGIN STANDARD CODE ********/
				cl_context    context = OpenCLProvider::get_context();
				if (!context)
					return NULL;
					
				
				cl_command_queue commandQueue = OpenCLProvider::get_command_queue();
				if (!commandQueue)
					return NULL;

				char kernelfile[] = "pycast/common/opt/kernels/_check_normalization.cl";
				char kernelfunc[] = "_check_normalization";
				
				cl_kernel kernel  = OpenCLProvider::get_kernel_from_file(kernelfile, kernelfunc);
				
				if (!kernel)
					return NULL;
				/********  END STANDARD CODE  ********/

				int timeseriesLength = PyObject_Length(self);
				double inVals[timeseriesLength];
				
				PyObject* tuple;
				PyObject* timestamp;
				PyObject* iterator = PyObject_GetIter(self);
				int idx = 0;
				
				while ((tuple = PyIter_Next(iterator))) {
					timestamp = PyList_GetItem(tuple, 0);
					inVals[idx] = PyFloat_AsDouble(timestamp);
					++idx;
				}
				
				//TimeSeries with two entries are always normalized
				if (timeseriesLength < 3)
					Py_RETURN_TRUE;

				double normalizedDistance = inVals[1] - inVals[0];

				int outFlag[] = {0};
				
				size_t bufferSize = sizeof(double) * timeseriesLength;

				cl_int err = 0;

				cl_mem inMem, flagMem;
				inMem  = clCreateBuffer(context, CL_MEM_READ_ONLY,  bufferSize, NULL, NULL);
				err    = clEnqueueWriteBuffer(commandQueue, inMem, CL_TRUE, 0, bufferSize, (void*)inVals, 0, NULL, NULL);
				assert(err == CL_SUCCESS);

				clFinish(commandQueue);

				flagMem  = clCreateBuffer(context, CL_MEM_READ_WRITE,  sizeof(outFlag), NULL, NULL);
				err    = clEnqueueWriteBuffer(commandQueue, flagMem, CL_TRUE, 0, sizeof(outFlag), (void*)outFlag, 0, NULL, NULL);
				assert(err == CL_SUCCESS);

				clFinish(commandQueue);
			
				err  = clSetKernelArg(kernel,  0, sizeof(double), (void *)&normalizedDistance);
				err |= clSetKernelArg(kernel,  1, sizeof(cl_mem), (void *)&inMem);
				err |= clSetKernelArg(kernel,  2, sizeof(cl_mem), (void *)&flagMem);
				assert(err == CL_SUCCESS);

				// Run the calculation by enqueuing it and forcing the
				// command queue to complete the task
				size_t global_work_size = timeseriesLength -1;
				err = clEnqueueNDRangeKernel(commandQueue, kernel, 1, NULL, &global_work_size, NULL, 0, NULL, NULL);
				assert(err == CL_SUCCESS);
				
				clFinish(commandQueue);
			
				// Once finished read back the results from the answer
				// array into the results array
				err = clEnqueueReadBuffer(commandQueue, flagMem, CL_TRUE, 0, sizeof(outFlag), outFlag, 0, NULL, NULL);
				
				assert(err == CL_SUCCESS);
				clFinish(commandQueue);

				clReleaseMemObject(inMem);

				// some distance was not equal to the normalizedDistance
				if (outFlag[0] > 0)
					Py_RETURN_FALSE;
				
				Py_RETURN_TRUE;
			}

		}
	}
}
