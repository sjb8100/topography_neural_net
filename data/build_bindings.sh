c++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` bindings.cpp -o utils`python3.5-config --extension-suffix` convert_las_to_matrix.cpp subsample_matrix.cpp read_data.cpp -llas
