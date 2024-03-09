#!/usr/bin/env sh

# Configure CMake
cmake -DCMAKE_BUILD_TYPE=Release \
      -DENABLE_COVERAGE:BOOL=False \
      -DENABLE_CPPCHECK:BOOL=False \
      -DENABLE_IPO:BOOL=True \
      -DENABLE_PCH:BOOL=True \
      -DENABLE_SANITIZER_ADDRESS:BOOL=False \
      -DENABLE_SANITIZER_MEMORY:BOOL=False \
      -DENABLE_SANITIZER_THREAD:BOOL=False \
      -DENABLE_SANITIZER_UNDEFINED_BEHAVIOR:BOOL=False \
      -DENABLE_TESTING:BOOL=False \
      -DWARNINGS_AS_ERRORS:BOOL=False

# Build with CMake
cmake --build .
