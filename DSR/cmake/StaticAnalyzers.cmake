# From https://github.com/lefticus/cpp_starter_project by lefticus (Jason Turner)

option(ENABLE_CPPCHECK "Enable static analysis with cppcheck" OFF)
option(ENABLE_CLANG_TIDY "Enable static analysis with clang-tidy" OFF)
if(ENABLE_CPPCHECK)
  find_program(CPPCHECK cppcheck)
  if(CPPCHECK)
    set(CMAKE_CXX_CPPCHECK ${CPPCHECK} --suppress=missingInclude --enable=all
                           --inconclusive -i ${CMAKE_SOURCE_DIR}/imgui/lib)
  else()
    message(SEND_ERROR "cppcheck requested but executable not found")
  endif()
endif()


