#pragma once

#include <string>
#include <exception>

namespace snspd::bc {
  struct UnknownBoundaryCondition : public std::exception {
    std::string message{"Unknown boundary condition."};

    UnknownBoundaryCondition() = default;

    explicit UnknownBoundaryCondition(std::string t_message):
        message(std::move(t_message)) {

    }

    [[nodiscard]] const char* what() const noexcept override {
      return message.c_str();
    }
  };
}
