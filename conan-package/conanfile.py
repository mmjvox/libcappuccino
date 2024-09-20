from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy, get, apply_conandata_patches, export_conandata_patches, rmdir


class cappuccinoRecipe(ConanFile):
    name = "cappuccino"
    version = "1.0.0"
    package_type = "library"

    # Optional metadata
    license = "Apache 2.0"
    author = " Josh Baldwin (jbaldwin)"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/jbaldwin/libcappuccino"
    description = "C++17 Cache Data Structure Library"
    topics = ("cpp", "cache", "lru", "modern-cpp", "cpp17", "cpp17-library")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "BUILD_EXAMPLES": [True, False], "BUILD_TESTS": [True, False]}
    default_options = {"shared": False, "fPIC": True, "BUILD_EXAMPLES": False, "BUILD_TESTS": False}

    def export_sources(self):
        export_conandata_patches(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.variables["CAPPUCCINO_BUILD_EXAMPLES"] = self.options.BUILD_EXAMPLES
        tc.variables["CAPPUCCINO_BUILD_TESTS"] = self.options.BUILD_TESTS
        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["cappuccino"]

    

    

