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

// Need to be first import
#include <Python.h>

#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <string>
#include <sstream>

#include "OpenCLProvider.h"

namespace common {

	cl_command_queue			OpenCLProvider::clCommandQueue	= NULL;
	cl_context					OpenCLProvider::clContext		= NULL;
	cl_device_id				OpenCLProvider::clDevice		= NULL;
	std::map<char*, cl_kernel>	*OpenCLProvider::kernelMap		= new std::map<char*, cl_kernel>();

	bool
	OpenCLProvider::initialize() {
		cl_device_id cpu	= NULL;
		cl_device_id gpu	= NULL;
		cl_device_id device = NULL;

		cl_platform_id platform_id = NULL;

		cl_int err = 0;
		
		// obtain list of platforms available
		err = clGetPlatformIDs(1, &platform_id,NULL);
			
		// set a RuntimeError and return if necessary
		if (err != CL_SUCCESS) {
			std::stringstream message;
			message << "[OpenCLProvider::initialize] Failure in clGetPlatformIDs (" << err << ")\n" << std::endl;
			PyErr_SetString(PyExc_RuntimeError, message.str().c_str());
			return false;
		}
	
		// Find the CPU CL device
		err = clGetDeviceIDs(platform_id, CL_DEVICE_TYPE_CPU, 1, &cpu, NULL);
		if (err != CL_SUCCESS) {
			PyErr_SetString(PyExc_RuntimeError, "[OpenCLProvider::initialize] Could not get CPU device running.");
			return false;
		}

		// Find the first GPU
		err = clGetDeviceIDs(platform_id, CL_DEVICE_TYPE_GPU, 1, &gpu, NULL);
		
		// fallback to CPU, if no GPU was found
		if (err != CL_SUCCESS)
			device = cpu;
	
		if (!device && !cpu) {
			PyErr_SetString(PyExc_RuntimeError, "[OpenCLProvider::initialize] Could not get any OpenCL device running.");
			return false;
		}

		char gpuconfig[4096];
		clGetDeviceInfo(gpu, CL_DEVICE_EXTENSIONS, 4096, (void*)&gpuconfig, NULL);
		std::string gpuconfigstr = gpuconfig;

		// use GPU (if found), when double precision is supported, CPU otherwise
		if (NULL == device && (std::string::npos != gpuconfigstr.find("cl_khr_fp64") || std::string::npos != gpuconfigstr.find("cl_amd_fp64")))
			device = gpu;
		else
			device = cpu;


		clContext = clCreateContext(0, 1, &device, NULL, NULL, &err);
		if (err != CL_SUCCESS) {
			PyErr_SetString(PyExc_RuntimeError, "[OpenCLProvider::initialize] Could not create the CL Context.");
			return false;
		}

		clCommandQueue = clCreateCommandQueue(clContext, device, CL_QUEUE_PROFILING_ENABLE, NULL); //0
		clDevice       = device;
		return true;
	}

	cl_command_queue
	OpenCLProvider::get_command_queue() {
		if (!OpenCLProvider::clCommandQueue)
			if (!OpenCLProvider::initialize())
				return NULL;

		return OpenCLProvider::clCommandQueue;
	}

	cl_context
	OpenCLProvider::get_context() {
		if (!OpenCLProvider::clContext)
			if (!OpenCLProvider::initialize())
				return NULL;

		return OpenCLProvider::clContext;
	}

	cl_kernel
	OpenCLProvider::get_kernel_from_file(char* kernelfile, char* functionname) {
		cl_int err = 0;
		cl_program program[1];
		
		// Create new kernel if it does not already exist
		if (kernelMap->find(kernelfile)==kernelMap->end()) {
			char *programSource = OpenCLProvider::load_program_source(kernelfile);
	
			if (!programSource) {
				std::stringstream message;
				message << "[OpenCLProvider::get_kernel_from_file] Could not find kernel file " << kernelfile << "." << std::endl;
				PyErr_SetString(PyExc_RuntimeError, message.str().c_str());
				return NULL;
			}
			
			program[0] = clCreateProgramWithSource(clContext, 1, (const char**)&programSource, NULL, &err);
			
			if (err != CL_SUCCESS) {
				PyErr_SetString(PyExc_RuntimeError, "[OpenCLProvider::get_kernel_from_file] Could not create program from source.");
				return NULL;
			}
			
			err = clBuildProgram(program[0], 0, NULL, NULL, NULL, NULL);
	
			if (err != CL_SUCCESS) {
				// get the OpenCL Log message for the error
				size_t loglen = 0;
				clGetProgramBuildInfo(program[0], clDevice, CL_PROGRAM_BUILD_LOG, 0, NULL, &loglen);
		
				char* logmessage;
				if (!(logmessage = (char*) malloc(loglen * sizeof(char)))) {
					PyErr_SetString(PyExc_RuntimeError, "[OpenCLProvider::get_kernel_from_file] Not enought memory.\n");
					return NULL;
				}
		
				clGetProgramBuildInfo(program[0], clDevice, CL_PROGRAM_BUILD_LOG, loglen, logmessage, NULL);
		
				std::stringstream message;
				message << "[OpenCLProvider::get_kernel_from_file] Could not build program.\n\n" << logmessage << std::endl;
				PyErr_SetString(PyExc_RuntimeError, message.str().c_str());
		
				free(logmessage);
				return NULL;
			}
	
			cl_kernel kernel = clCreateKernel(program[0], functionname, &err);
			if (err != CL_SUCCESS) {
				PyErr_SetString(PyExc_RuntimeError, "[OpenCLProvider::get_kernel_from_file] Could not get the build kernel.");
				return NULL;
			} 
			
			// Now create the kernel "objects" that we want to use in the example file 
			kernelMap->insert(std::pair<char*, cl_kernel>(kernelfile, kernel));
		}
		
		return kernelMap->at(kernelfile);
	}

	char*
	OpenCLProvider::load_program_source(char *kernelfile)
	{ 
		struct stat statbuf;
		char *source; 
	
		FILE *filehandle = fopen(kernelfile, "r");
		if (!filehandle)
			return NULL; 

		stat(kernelfile, &statbuf);
		source = (char *) malloc(statbuf.st_size + 1);
		fread(source, statbuf.st_size, 1, filehandle);
		source[statbuf.st_size] = '\0'; 
		
		return source; 
	} 
}
