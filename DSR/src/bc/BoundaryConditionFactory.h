#pragma once

#include <memory>
#include <nlohmann/json.hpp>
#include <spdlog/spdlog.h>
#include "BoundaryCondition.h"
#include "exception/UnknownBoundaryCondition.h"
#include "CurrentBiasBoundaryCondition.h"
#include "VoltageBiasBoundaryCondition.h"
#include "../io/ConfigParser.h"

namespace snspd::bc {
  class BoundaryConditionFactory {
    BoundaryConditionFactory() = default;

  public:

    static std::unique_ptr<BoundaryCondition> make(io::ConfigParser &parser) {

      spdlog::debug("Creating boundary condition.");

      // Check if the boundary condition flag is given
      if (!parser.get_json_config()["parameters"].contains("boundaryCondition")) {
        throw UnknownBoundaryCondition();
      }

      auto boundary_condition = parser.get_json_config()["parameters"]["boundaryCondition"].get<std::string>();

      if (boundary_condition == "simple") {
        spdlog::debug("Using current bias current with no circuit.");
        return std::make_unique<BoundaryCondition>(parser.get_params());
      }

      if (boundary_condition == "current") {
        spdlog::debug("Using current bias boundary condition.");
        return std::make_unique<CurrentBiasBoundaryCondition>(parser.get_params());
      }

      if (boundary_condition == "voltage") {
        spdlog::debug("Using voltage bias boundary condition.");
        return std::make_unique<VoltageBiasBoundaryCondition>(parser.get_params());
      }

      throw UnknownBoundaryCondition();
    }
  };
}
