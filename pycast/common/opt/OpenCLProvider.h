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

#pragma once
#ifndef PYCAST_COMMON_OPENCLPROVIDER_H
#define PYCAST_COMMON_OPENCLPROVIDER_H

#ifdef __APPLE__
	#include <OpenCL/cl.h>
#elif __unix
	#include <CL/cl.h>
#endif

#include <string.h>
#include <map>

namespace common {

	class OpenCLProvider {
		public:
			static cl_command_queue	get_command_queue();
			static cl_context		get_context();
			static cl_kernel		get_kernel_from_file(char* kernelfile, char* functionname);

		private:
			static bool				initialize();
			static char*			load_program_source(char* kernelfile);

			static cl_command_queue				clCommandQueue;
			static cl_context					clContext;
			static cl_device_id					clDevice;
			static std::map<char*, cl_kernel>	*kernelMap;
	};

}

#endif /* PYCAST_COMMON_OPENCLPROVIDER_H */
