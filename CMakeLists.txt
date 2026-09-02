cmake_minimum_required(VERSION 3.8)
project(bagwis_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rosidl_default_generators REQUIRED)

find_package(std_msgs REQUIRED)
find_package(geographic_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)

# ---------------------------------------------------------------------------
# Messages and services (SRS-00 SS4)
# ---------------------------------------------------------------------------

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/AnalyticsAssumptions.msg"
  "msg/FinalMetrics.msg"
  "msg/FlightParams.msg"
  "msg/GeoDetection.msg"
  "msg/NdviResult.msg"
  "msg/ObstructionCluster.msg"
  "msg/SafetyAlert.msg"
  "msg/SystemHealth.msg"
  "srv/GetMissionState.srv"
  "srv/StartMission.srv"
  "srv/StopMission.srv"
  DEPENDENCIES std_msgs geographic_msgs builtin_interfaces
)

# ---------------------------------------------------------------------------
# Topic-name constants (FR-IF-03)
#
# topics.hpp / topics.py / topics.ts are generated from topics/registry.yaml by
# scripts/generate.py and committed to git, because bagwis-web builds with
# Next.js and has no colcon to generate them with. The build only VERIFIES the
# committed output -- it never writes into the source tree. A mismatch here
# means the checkout is inconsistent, and failing the build is the point.
# ---------------------------------------------------------------------------

find_package(Python3 REQUIRED COMPONENTS Interpreter)

execute_process(
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate.py"
          --root "${CMAKE_CURRENT_SOURCE_DIR}" --check
  RESULT_VARIABLE _bagwis_generate_result
  OUTPUT_VARIABLE _bagwis_generate_output
  ERROR_VARIABLE _bagwis_generate_error
)
if(NOT _bagwis_generate_result EQUAL 0)
  message(FATAL_ERROR
    "Generated constants are stale.\n"
    "${_bagwis_generate_error}\n"
    "Run: python3 scripts/generate.py")
endif()

# C++: #include <bagwis_interfaces/topics.hpp>
install(DIRECTORY include/ DESTINATION include)
ament_export_include_directories(include)

# Python: from bagwis_interfaces.topics import AI_NDVI
#
# Installed straight INTO the package directory that rosidl generates, so it
# sits beside the generated __init__.py rather than replacing it.
# ament_python_install_package() would clobber that __init__.py and break
# `from bagwis_interfaces.msg import FinalMetrics`.
install(FILES python/topics.py
  DESTINATION "${PYTHON_INSTALL_DIR}/${PROJECT_NAME}"
)

# TypeScript: consumed directly from the submodule working tree by bagwis-web,
# and installed to share/ so it is also reachable from an installed workspace.
install(DIRECTORY ts/ DESTINATION share/${PROJECT_NAME}/ts)

# The canonical registry itself, for the FR-CN-63 startup graph-conformance
# check to read at runtime.
install(FILES topics/registry.yaml DESTINATION share/${PROJECT_NAME}/topics)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # No hand-written C++ or Python source here: copyright headers and cpplint
  # have nothing to say about generated constants and .msg files.
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  set(ament_cmake_uncrustify_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
