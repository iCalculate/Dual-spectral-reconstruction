# Based on https://github.com/lefticus/cpp_starter_project by lefticus (Jason Turner)

macro(run_conan)
    # Download automatically, you can also just copy the conan.cmake file
    if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
        message(
                STATUS
                "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
        file(DOWNLOAD "https://github.com/conan-io/cmake-conan/raw/v0.15/conan.cmake"
                "${CMAKE_BINARY_DIR}/conan.cmake")
    endif()

    include(${CMAKE_BINARY_DIR}/conan.cmake)

    conan_add_remote(NAME bincrafters URL https://api.bintray.com/conan/bincrafters/public-conan)

    conan_cmake_run(
            CONANFILE conanfile.txt
            SETTINGS compiler.cppstd=17 # Set the cppstd version to 17. Needed by h5pp.
            BASIC_SETUP
            CMAKE_TARGETS # individual targets to link to
            BUILD
            missing)
endmacro()
