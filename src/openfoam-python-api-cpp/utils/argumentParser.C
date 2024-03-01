#include "argumentParser.H"

arguments::arguments(py::object pyargv11) {
    int argc = 0;
    std::unique_ptr<char*[]> argv;

// convert input list to C/C++ argc/argv
    PyObject* pyargv = pyargv11.ptr();
    if (PySequence_Check(pyargv)) {
        Py_ssize_t sz = PySequence_Size(pyargv);
        argc = int(sz);
        argv = std::unique_ptr<char*[]>{new char*[sz]};
        for (Py_ssize_t i = 0; i < sz; ++i) {
            PyObject* item = PySequence_GetItem(pyargv, i);
            argv[i] = (char*)MyPyText_AsString(item);
            Py_DECREF(item);
            if (!argv[i] || PyErr_Occurred()) {
                argv = nullptr;
                break;
            }
        }
    }

// bail if failed to convert
    if (!argv) {
        std::cerr << "argument is not a sequence of strings" << std::endl;
        throw std::runtime_error("argument is not a sequence of strings");
        argc_ = 0;
        argv_ = nullptr;
    }

    printf("argc: %d\n", argc);
    for (int i = 0; i < argc; i++) {
        printf("argv[%d]: %s\n", i, argv[i]);
    }
// call the closed function with the proper types
    argc_ = argc;
    argv_ = argv.release();
}
