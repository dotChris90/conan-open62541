from conans import ConanFile, CMake, tools


class Open62541Conan(ConanFile):
    name = "open62541"
    version = "1.0.1"
    license = "MPLv2"
    description = "Open62541 is an open source and free implementation of OPC UA (OPC Unified Architecture) written in the common subset of the C99 and C++98 languages."
    topics = ("OPC UA", "Ua")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/open62541/open62541.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("open62541/CMakeLists.txt", "project(open62541)",
                              '''project(open62541)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        if self.options.shared:
            cmake.define('BUILD_SHARED_LIBS','ON')
        else:
            pass
        cmake.configure(source_folder="open62541")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="open62541")
        self.copy("*open62541.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", excludes="*foo.a", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

