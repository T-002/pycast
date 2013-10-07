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
#define __APPLE__
#ifndef __APPLE__
    #include <chrono>
#endif

#include "matrix.h"
#include "OpenCLProvider.h"

namespace common {
    namespace matrix {

        MatrixClass::MatrixClass() {}

        MatrixClass::MatrixClass(int columns, int rows) {
            data = (float*) malloc(sizeof(float) * (columns * rows));
            width = columns;
            height = rows;
            int i = 0;
            int j = 0;
            for(i=0; i < rows; i++) {
                for(j=0; j < columns; j++){
                    data[i * columns + j] = 0.0;
                }
            }
        }

        PyObject*
        MatrixClass::set_value(int col, int row, float value) {
            if (col >= width || row >= height) {
                Py_RETURN_FALSE;
            } else {
                data[row * width + col] = value;
                Py_RETURN_TRUE;
            }
        }

        float
        MatrixClass::get_value(int col, int row) {
            return data[row * width + col];
        }

        namespace Matrix {
            
            void
            copy_matrix(int height, int width, PyObject* matrix, float* matrix_as_list){
                float value;

                int i=0;
                int j=0;
                for(i=0;i<height;i++){
                    for(j=0;j<width;j++){
                        value = (float) PyFloat_AsDouble(PyObject_CallMethodObjArgs(matrix, PyString_FromString("get_value"), PyInt_FromLong(j), PyInt_FromLong(i), NULL));
                        matrix_as_list[i * width + j] = value;
                    }
                }
            }

            PyObject*
            matrix_multiplication(PyObject* self, PyObject* matrix) {

                #ifndef __APPLE__
                    typedef std::chrono::high_resolution_clock Clock;
                    typedef std::chrono::milliseconds milliseconds;
    
                    Clock::time_point start_c = Clock::now();
                #endif

                /******** BEGIN STANDARD CODE ********/
                cl_context    context = OpenCLProvider::get_context();
                if (!context)
                    return NULL;
                    
                
                cl_command_queue commandQueue = OpenCLProvider::get_command_queue();
                if (!commandQueue)
                    return NULL;

                char kernelfile[] = "pycast/common/opt/kernels/matrix_multiplication.cl";
                char kernelfunc[] = "matrix_multiplication";
                
                cl_kernel kernel  = OpenCLProvider::get_kernel_from_file(kernelfile, kernelfunc);
                
                if (!kernel)
                    return NULL;
                /********  END STANDARD CODE  ********/

                int width = (int) PyInt_AsLong(PyObject_CallMethodObjArgs(self, PyString_FromString("get_width"), NULL));
                int number_of_rows = (int) PyInt_AsLong(PyObject_CallMethodObjArgs(self, PyString_FromString("get_height"), NULL));
                int number_of_cols = (int) PyInt_AsLong(PyObject_CallMethodObjArgs(matrix, PyString_FromString("get_width"), NULL));
                int number_of_entries = number_of_rows * number_of_cols;
                int size_A = width * number_of_rows;
                int size_B = number_of_cols * width;

                float* A = (float*) malloc(sizeof(float) * size_A);                     
                copy_matrix(number_of_rows, width, self, A);
                float* B = (float*) malloc(sizeof(float) * size_B);                     
                copy_matrix(width, number_of_cols, matrix, B);
                float* C = (float*) malloc(sizeof(float) * number_of_entries);

                size_t localWorkSize[2] = {8, 8};
                size_t globalWorkSize[2] = {number_of_rows, number_of_cols};

                cl_int err = 0;
                cl_mem input_m1, input_m2, output;
                cl_event GPUExecution;

                clFinish(commandQueue);

                #ifndef __APPLE__
                    Clock::time_point start_create_buffer = Clock::now();
                #endif

                input_m1 = clCreateBuffer(context,  CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR,  sizeof(float) * size_A, A, NULL);
                input_m2 = clCreateBuffer(context,  CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR,  sizeof(float) * size_B, B, NULL);
                output = clCreateBuffer(context, CL_MEM_WRITE_ONLY, sizeof(float) * number_of_entries, NULL, NULL); 

                #ifndef __APPLE__
                    Clock::time_point end_create_buffer = Clock::now();
                    milliseconds ms_create_buffer = std::chrono::duration_cast<milliseconds>(end_create_buffer - start_create_buffer);
                    // printf("Create Buffers: %li ms \n", ms_create_buffer.count());

                    Clock::time_point start_set_kernel = Clock::now();
                #endif

                err  = clSetKernelArg(kernel, 0, sizeof(cl_mem), &input_m1);
                err |= clSetKernelArg(kernel, 1, sizeof(cl_mem), &input_m2);
                err |= clSetKernelArg(kernel, 2, sizeof(cl_mem), &output);
                err |= clSetKernelArg(kernel, 3, sizeof(int), &width);
                err |= clSetKernelArg(kernel, 4, sizeof(int), &number_of_cols);
                assert(err == CL_SUCCESS);

                #ifndef __APPLE__                    
                    Clock::time_point end_set_kernel = Clock::now();
                    milliseconds ms_set_kernel = std::chrono::duration_cast<milliseconds>(end_set_kernel - start_set_kernel);
                    // printf("Set Kernel Args: %li ms \n", ms_set_kernel.count());

                    Clock::time_point start_enqueue = Clock::now();
                #endif

                err = clEnqueueNDRangeKernel(commandQueue, kernel, 2, NULL, globalWorkSize, localWorkSize, 0, NULL, &GPUExecution);
                if (err != CL_SUCCESS) {
                    std::stringstream message;
                    message << "[OpenCLProvider::initialize] Failure in clEnqueueNDRangeKernel   (" << err << ")\n" << std::endl;
                    PyErr_SetString(PyExc_RuntimeError, message.str().c_str());
                    return NULL;
                }

                #ifndef __APPLE__
                    Clock::time_point end_enqueue = Clock::now();
                    milliseconds ms_enqueue = std::chrono::duration_cast<milliseconds>(end_enqueue - start_enqueue);
                    // printf("Enqueue Kernel: %li ms \n", ms_enqueue.count());

                    Clock::time_point start_flush = Clock::now();
                #endif

                clFlush(commandQueue);

                #ifndef __APPLE__
                    Clock::time_point end_flush = Clock::now();
                    milliseconds ms_flush = std::chrono::duration_cast<milliseconds>(end_flush - start_flush);
                    // printf("Flush: %li ms \n", ms_flush.count());

                    Clock::time_point start_read_buffer = Clock::now();
                #endif

                err = clEnqueueReadBuffer(commandQueue, output, CL_TRUE, 0, sizeof(float) * number_of_entries, C, 0, NULL, NULL);
                assert(err == CL_SUCCESS);

                #ifndef __APPLE__
                    Clock::time_point end_read_buffer = Clock::now();
                    milliseconds ms_read_buffer = std::chrono::duration_cast<milliseconds>(end_read_buffer - start_read_buffer);
                    // printf("Read Buffer: %li ms \n", ms_read_buffer.count());

                    Clock::time_point start_finish = Clock::now();
                #endif

                clFinish(commandQueue);

                #ifndef __APPLE__
                    Clock::time_point end_finish = Clock::now();
                    milliseconds ms_finish = std::chrono::duration_cast<milliseconds>(end_finish - start_finish);
                    // printf("Finish: %li ms \n", ms_finish.count());
                #endif

                cl_ulong start, end;
                clGetEventProfilingInfo(GPUExecution, CL_PROFILING_COMMAND_END, sizeof(cl_ulong), &end, NULL);
                clGetEventProfilingInfo(GPUExecution, CL_PROFILING_COMMAND_START, sizeof(cl_ulong), &start, NULL);
                
                #ifndef __APPLE__
                    double elapsedTime = (double)1.0e-9 * (end - start);
                    // printf("Kernel execution time: %f s \n", elapsedTime);
                #endif

                clReleaseMemObject(input_m1);
                clReleaseMemObject(input_m2);
                clReleaseMemObject(output);

                PyObject* result_matrix = PyList_New(number_of_entries);
                int i;
                for(i=0; i<number_of_entries; i++){
                    PyList_SetItem(result_matrix, i, PyFloat_FromDouble(C[i]));
                }

                PyObject* result = PyObject_CallMethodObjArgs(self, PyString_FromString("get_matrix_from_list"), PyInt_FromLong(number_of_rows), PyInt_FromLong(number_of_cols), result_matrix, NULL);

                free(A);
                free(B);
                free(C);

                #ifndef __APPLE__
                    Clock::time_point end_c = Clock::now();
                    milliseconds ms_c = std::chrono::duration_cast<milliseconds>(end_c - start_c);
                    // printf("C Programm: %li ms \n", ms_c.count());
                #endif

                return result;
            }
        }
    }
}
